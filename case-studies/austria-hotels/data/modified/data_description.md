# Dataset Description

> Auto-generated on 2026-02-23

## Overview
- **Number of tables**: 9
- **Location**: `data/modified/`

This dataset describes the Austrian hotel industry. It covers 169 hotel records across ~12 cities, with supporting tables for guest reviews, monthly occupancy and revenue, booking channel breakdowns, amenities, city-level tourism statistics, and national economic indicators. The data spans 2023-2024.

The relational structure centers on a **hotels** table linked outward to bookings, occupancy, reviews, and amenities — with city-level and time-period dimensions connecting to tourism and macroeconomic context.

---

## Table: hotels_modified
- **File**: hotels_modified.csv
- **Rows**: 169 | **Columns**: 6

### Variables
| Column | Type | Missing | Unique | Description |
|--------|------|---------|--------|-------------|
| hotel_id | int64 | 0 | 166 | Hotel identifier — **not fully unique** (3 duplicate IDs: 201, 202, 203) |
| city | string | 0 | 12 | City where the hotel is located |
| hotel_name | string | 0 | 91 | Name of the hotel (not unique — several names repeat across cities) |
| star_rating | int64 | 0 | 3 | Star rating (3, 4, or 5 stars) |
| rooms | int64 | 0 | 111 | Number of rooms in the hotel |
| year_built | int64 | 0 | 90 | Year the hotel was built |

### Summary Statistics
| Column | Min | Max | Mean | Median | SD |
|--------|-----|-----|------|--------|----|
| hotel_id | 1 | 203 | 103.5 | 105.0 | 59.1 |
| star_rating | 3 | 5 | 4.0 | 4.0 | 0.8 |
| rooms | 32 | 230 | 138.0 | 139.0 | 59.9 |
| year_built | 1901 | 2019 | 1961.8 | 1960.0 | 34.2 |

### Data Quality Notes
- **Duplicate primary key**: `hotel_id` has 166 unique values in 169 rows. IDs 201, 202, 203 each appear twice — this breaks referential integrity if used as a PK.
- **Phantom cities**: `city` contains 3 fictitious values ("Phantom Town", "Ghost Village", "Imaginary City") that do not appear in the cities table — likely intentional for teaching/exercise purposes.
- Some real Austrian cities in this table (Innsbruck, Kitzbuhel, Bad Gastein) are also missing from the cities lookup table.

---

## Table: cities_modified
- **File**: cities_modified.csv
- **Rows**: 10 | **Columns**: 4

### Variables
| Column | Type | Missing | Unique | Description |
|--------|------|---------|--------|-------------|
| city | string | 0 | 10 | City name — serves as the primary key |
| province | string | 0 | 6 | Austrian province (Bundesland) the city belongs to |
| population | int64 | 0 | 9 | City population |
| tourism_rank | int64 | 0 | 10 | Ranking by tourism importance |

### Summary Statistics
| Column | Min | Max | Mean | Median | SD |
|--------|-----|-----|------|--------|----|
| population | 800 | 1,900,000 | 261,430 | 7,500 | 587,050 |
| tourism_rank | 1 | 122 | 39.1 | 7.0 | 54.8 |

### Data Quality Notes
- Small reference table (10 cities). Covers only a subset of cities in the hotels table — 6 of 12 hotel cities match.
- Population is highly skewed (Vienna at 1.9M dominates).

---

## Table: amenities
- **File**: amenities.csv
- **Rows**: 10 | **Columns**: 2

### Variables
| Column | Type | Missing | Unique | Description |
|--------|------|---------|--------|-------------|
| amenity_id | int64 | 0 | 10 | Amenity identifier (1-10) — primary key |
| amenity_name | string | 0 | 10 | Name of the amenity (Pool, Spa, Gym, Restaurant, Bar, etc.) |

### Data Quality Notes
- Clean lookup table, no issues. All 10 amenity IDs are referenced in hotel_amenities.

---

## Table: hotel_amenities_modified
- **File**: hotel_amenities_modified.csv
- **Rows**: 930 | **Columns**: 2

### Variables
| Column | Type | Missing | Unique | Description |
|--------|------|---------|--------|-------------|
| hotel_id | int64 | 0 | 198 | Foreign key to hotels table |
| amenity_id | int64 | 0 | 10 | Foreign key to amenities table |

### Data Quality Notes
- **Junction table** (many-to-many link between hotels and amenities).
- Contains 198 unique hotel_ids but the hotels table only has 166 unique IDs — **37 hotel_ids are orphans** (not in hotels). This means some amenity assignments point to non-existent hotels.
- amenity_id coverage is 100% (all 10 amenities referenced).

---

## Table: hotel_bookings
- **File**: hotel_bookings.csv
- **Rows**: 845 | **Columns**: 4

### Variables
| Column | Type | Missing | Unique | Description |
|--------|------|---------|--------|-------------|
| hotel_id | int64 | 0 | 166 | Foreign key to hotels table |
| channel | string | 0 | 5 | Booking channel (Booking.com, Direct, Expedia, HRS, Travel Agent) |
| pct_bookings | float64 | 0 | 46 | Percentage of bookings via this channel |
| avg_commission | float64 | 0 | 130 | Average commission rate for this channel |

### Summary Statistics
| Column | Min | Max | Mean | Median | SD |
|--------|-----|-----|------|--------|----|
| pct_bookings | 2.0 | 48.0 | 20.0 | 18.0 | 11.0 |
| avg_commission | 0.0 | 0.184 | 0.091 | 0.098 | 0.054 |

### Data Quality Notes
- 5 channels x ~169 hotels = ~845 rows — each hotel has one row per channel.
- hotel_id coverage is 100% (all match the hotels table).
- Direct bookings likely have avg_commission = 0.

---

## Table: monthly_occupancy_modified
- **File**: monthly_occupancy_modified.csv
- **Rows**: 3,053 | **Columns**: 6

### Variables
| Column | Type | Missing | Unique | Description |
|--------|------|---------|--------|-------------|
| hotel_id | int64 | 0 | 160 | Foreign key to hotels table |
| month | int64 | 0 | 12 | Calendar month (1-12) |
| year | int64 | 0 | 2 | Year (2023 or 2024) |
| occupancy_rate | float64 | 0 | 26 | Monthly occupancy rate (proportion, 0.67-0.98) |
| avg_daily_rate | int64 | 0 | 231 | Average daily room rate in EUR |
| revenue_per_room | int64 | 0 | 243 | Revenue per available room (RevPAR) in EUR |

### Summary Statistics
| Column | Min | Max | Mean | Median | SD |
|--------|-----|-----|------|--------|----|
| occupancy_rate | 0.67 | 0.98 | 0.855 | 0.82 | 0.093 |
| avg_daily_rate | 87 | 328 | 218.7 | 214.0 | 52.0 |
| revenue_per_room | 60 | 321 | 189.9 | 186.0 | 59.6 |

### Data Quality Notes
- 160 unique hotel_ids, but **29 are orphans** (not in hotels table). Only 131 match.
- 24 month-year periods (Jan 2023 through Dec 2024).
- Structure is hotel x month x year panel data.

---

## Table: reviews_modified
- **File**: reviews_modified.csv
- **Rows**: 1,262 | **Columns**: 4

### Variables
| Column | Type | Missing | Unique | Description |
|--------|------|---------|--------|-------------|
| review_id | int64 | 0 | 1,262 | Unique review identifier — primary key |
| hotel_id | int64 | 0 | 177 | Foreign key to hotels table |
| rating | float64 | 0 | 28 | Review rating (2.0-4.9 scale) |
| review_date | string | 0 | 607 | Date of review (YYYY-MM-DD format, stored as string) |

### Summary Statistics
| Column | Min | Max | Mean | Median | SD |
|--------|-----|-----|------|--------|----|
| rating | 2.0 | 4.9 | 3.57 | 3.6 | 0.50 |

### Data Quality Notes
- `review_date` is stored as a string, not a date type — needs parsing for time-series analysis.
- 177 unique hotel_ids, but **34 are orphans** (not in hotels table). Only 143 match.
- review_id is fully unique — clean primary key.

---

## Table: city_tourism_modified
- **File**: city_tourism_modified.csv
- **Rows**: 220 | **Columns**: 6

### Variables
| Column | Type | Missing | Unique | Description |
|--------|------|---------|--------|-------------|
| city | string | 0 | 10 | City name — foreign key to cities table |
| month | int64 | 0 | 12 | Calendar month (1-12) |
| year | int64 | 0 | 2 | Year (2023 or 2024) |
| tourist_arrivals | int64 | 0 | 216 | Number of tourist arrivals in the city that month |
| event_days | int64 | 0 | 15 | Number of event/festival days in the city that month |
| avg_stay_length | float64 | 0 | 16 | Average length of tourist stay (days) |

### Summary Statistics
| Column | Min | Max | Mean | Median | SD |
|--------|-----|-----|------|--------|----|
| tourist_arrivals | 151 | 2,961,841 | 247,268 | 33,186 | 571,551 |
| event_days | 5 | 19 | 9.8 | 10.0 | 3.4 |
| avg_stay_length | 2.3 | 3.8 | 3.0 | 3.0 | 0.35 |

### Data Quality Notes
- 10 cities x ~22 month/year periods = 220 rows (city-month panel).
- 3 cities (Innsbruck, Kitzbuhel, Bad Gastein) are not in the cities lookup table — only 7/10 match.
- tourist_arrivals is extremely skewed (Vienna dominates).

---

## Table: economic_indicators
- **File**: economic_indicators.csv
- **Rows**: 24 | **Columns**: 5

### Variables
| Column | Type | Missing | Unique | Description |
|--------|------|---------|--------|-------------|
| month | int64 | 0 | 12 | Calendar month (1-12) |
| year | int64 | 0 | 2 | Year (2023 or 2024) |
| inflation_rate | float64 | 0 | 22 | Monthly inflation rate (proportion, ~1.6-2.5%) |
| unemployment | float64 | 0 | 22 | Monthly unemployment rate (proportion, ~3.8-5.1%) |
| consumer_confidence | float64 | 0 | 20 | Consumer confidence index (base ~100) |

### Summary Statistics
| Column | Min | Max | Mean | Median | SD |
|--------|-----|-----|------|--------|----|
| inflation_rate | 0.016 | 0.025 | 0.021 | 0.021 | 0.003 |
| unemployment | 0.038 | 0.051 | 0.042 | 0.042 | 0.004 |
| consumer_confidence | 100.3 | 106.0 | 102.4 | 102.4 | 1.6 |

### Data Quality Notes
- Clean national-level time series. 24 rows = 12 months x 2 years. No missing values.
- Joins to other tables on (month, year) — all 24 periods are shared with occupancy and tourism.

---

## Relationships

| From Table | Column | To Table | Column | Coverage | Notes |
|-----------|--------|----------|--------|----------|-------|
| hotels_modified | city | cities_modified | city | 50% (6/12 cities) | 3 fictitious cities + 3 real cities missing from lookup |
| hotel_amenities_modified | hotel_id | hotels_modified | hotel_id | 81.3% (161/198) | 37 orphan hotel_ids |
| hotel_amenities_modified | amenity_id | amenities | amenity_id | 100% | Clean |
| hotel_bookings | hotel_id | hotels_modified | hotel_id | 100% | Clean |
| monthly_occupancy_modified | hotel_id | hotels_modified | hotel_id | 81.9% (131/160) | 29 orphan hotel_ids |
| monthly_occupancy_modified | (month, year) | economic_indicators | (month, year) | 100% | Clean |
| monthly_occupancy_modified | (month, year) | city_tourism_modified | (month, year) | 100% | Via hotels.city to link hotel-level to city-level |
| reviews_modified | hotel_id | hotels_modified | hotel_id | 80.8% (143/177) | 34 orphan hotel_ids |
| city_tourism_modified | city | cities_modified | city | 70% (7/10) | 3 cities missing from lookup |
| economic_indicators | (month, year) | city_tourism_modified | (month, year) | 100% | National-level context for city-level tourism |

## Data Quality Summary

1. **Duplicate primary key in hotels**: `hotel_id` values 201, 202, 203 each appear twice in hotels_modified. This is the central table — duplicates here cascade into ambiguous joins.

2. **Widespread orphan hotel_ids**: Three tables (hotel_amenities, monthly_occupancy, reviews) reference hotel_ids not present in the hotels table. Around 19-20% of FK values are orphans in each. This likely reflects hotels that were removed from the hotels table but left in child tables.

3. **Incomplete city lookup**: The cities_modified table covers only a subset of cities. Three fictitious city names ("Phantom Town", "Ghost Village", "Imaginary City") appear in hotels — these are likely planted data quality issues for a teaching exercise.

4. **Date stored as string**: `review_date` in reviews_modified is stored as a string column, not a proper date.

5. **No issues**: hotel_bookings and economic_indicators are clean — full join coverage, no missing values, no duplicates.

6. **Teaching dataset**: The pattern of deliberate imperfections (phantom cities, orphan keys, duplicated IDs) suggests this is a dataset designed for data wrangling exercises.
