"""
Generate hotel booking channel data for Austrian Hotels dataset.
Created by Claude Code, 2026-01-30
"""

import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Read hotels data
hotels = pd.read_csv('modified/hotels_modified.csv')

# Define booking channels with base commission rates
channels = {
    'Direct': {'base_commission': 0.0, 'base_pct': 33},
    'Booking.com': {'base_commission': 0.15, 'base_pct': 30},
    'Expedia': {'base_commission': 0.18, 'base_pct': 18},
    'HRS': {'base_commission': 0.12, 'base_pct': 10},
    'Travel Agent': {'base_commission': 0.10, 'base_pct': 9}
}

booking_data = []

for _, hotel in hotels.iterrows():
    hotel_id = hotel['hotel_id']
    star_rating = hotel['star_rating']
    hotel_name = hotel['hotel_name'].lower()

    # Adjust percentages based on hotel characteristics
    pcts = {}

    # 5-star hotels: more direct bookings and travel agents
    # 3-star hotels: more OTA reliance
    star_modifier = (star_rating - 4) * 8  # -8 for 3-star, 0 for 4-star, +8 for 5-star

    pcts['Direct'] = channels['Direct']['base_pct'] + star_modifier + np.random.randint(-5, 6)
    pcts['Travel Agent'] = channels['Travel Agent']['base_pct'] + (star_modifier // 2) + np.random.randint(-3, 4)

    # Boutique hotels get some Airbnb-style bookings via HRS (corporate travel)
    if 'boutique' in hotel_name or 'budget' in hotel_name:
        pcts['HRS'] = channels['HRS']['base_pct'] + np.random.randint(0, 8)
    else:
        pcts['HRS'] = channels['HRS']['base_pct'] + np.random.randint(-3, 4)

    # OTAs take the rest, with Booking.com dominant
    remaining = 100 - pcts['Direct'] - pcts['Travel Agent'] - pcts['HRS']
    booking_share = np.random.uniform(0.55, 0.70)  # Booking.com gets 55-70% of OTA
    pcts['Booking.com'] = int(remaining * booking_share)
    pcts['Expedia'] = remaining - pcts['Booking.com']

    # Ensure all positive and sum to 100
    pcts = {k: max(2, v) for k, v in pcts.items()}
    total = sum(pcts.values())
    pcts = {k: round(v / total * 100, 1) for k, v in pcts.items()}

    # Adjust to sum to exactly 100
    diff = 100 - sum(pcts.values())
    pcts['Booking.com'] = round(pcts['Booking.com'] + diff, 1)

    # Add rows for each channel
    for channel, pct in pcts.items():
        # Commission varies slightly by hotel negotiating power (size/stars)
        base_comm = channels[channel]['base_commission']
        if base_comm > 0:
            # Larger/fancier hotels negotiate better rates
            negotiation_power = (hotel['rooms'] / 200) * 0.02 + (star_rating - 3) * 0.01
            commission = base_comm - negotiation_power + np.random.uniform(-0.01, 0.01)
            commission = round(max(0.05, min(base_comm + 0.03, commission)), 3)
        else:
            commission = 0.0

        booking_data.append({
            'hotel_id': hotel_id,
            'channel': channel,
            'pct_bookings': pct,
            'avg_commission': commission
        })

# Create DataFrame
df = pd.DataFrame(booking_data)

# Sort by hotel_id and channel
df = df.sort_values(['hotel_id', 'channel']).reset_index(drop=True)

# Save to CSV
df.to_csv('modified/hotel_bookings.csv', index=False)

print(f"Generated {len(df)} rows for {len(hotels)} hotels")
print(f"\nSample data:")
print(df.head(15))
print(f"\nBooking channel summary:")
print(df.groupby('channel')['pct_bookings'].describe().round(1))
