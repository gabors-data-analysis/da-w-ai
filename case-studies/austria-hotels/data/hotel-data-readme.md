# Austrian Hotels Dataset

## Info
This dataset contains realistic data on hotels across Austria. 

* This dataset was generated programmatically with the `generate_austrian_hotels_data.R` script to ensure realistic relationships between variables while maintaining privacy.
  * The scipt was writen by Claude AI, Sonnet 3.7, 2025-03-15, and reviwed and approved by Gabor 2025-03-17
* The dataset consists of multiple related tables that can be combined.
* The data patterns are based on typical hotel industry metrics but do not represent actual hotels.


## Dataset Overview

The dataset includes hotels across Austrian cities with data on occupancy, pricing, tourism statistics, and economic indicators.

### Files

All files are located in the `data/raw/` directory:
  
  | File | Description | Rows | Key Columns |
  |------|-------------|------|------------|
  | `hotels.csv` | Basic hotel information | 200 | `hotel_id` (PK) |
  | `cities.csv` | City information | 10 | `city` (PK) |
  | `monthly_occupancy.csv` | Monthly hotel performance metrics | ~3,800 | `hotel_id`, `month`, `year` |
  | `city_tourism.csv` | Monthly tourism statistics by city | 240 | `city`, `month`, `year` |
  | `economic_indicators.csv` | Monthly economic indicators | 24 | `month`, `year` |
  | `reviews.csv` | Hotel guest reviews | ~1,700 | `review_id` (PK), `hotel_id` (FK) |
  | `amenities.csv` | List of possible hotel amenities | 10 | `amenity_id` (PK) |
  | `hotel_amenities.csv` | Hotel-amenity relationships | ~1,000 | `hotel_id`, `amenity_id` |
  
  ## Schema Details
  
  ### hotels.csv
  Information about individual hotels.

| Column | Type | Description |
  |--------|------|-------------|
  | `hotel_id` | integer | Primary key |
  | `hotel_name` | character | Hotel name |
  | `city` | character | City where hotel is located |
  | `star_rating` | integer | Hotel quality rating (3-5 stars) |
  | `rooms` | integer | Number of rooms in the hotel |
  | `year_built` | integer | Year the hotel was built |
  
  ### cities.csv
  Information about Austrian cities.

| Column | Type | Description |
  |--------|------|-------------|
  | `city` | character | City name (primary key) |
  | `province` | character | Austrian province |
  | `population` | integer | City population |
  | `tourism_rank` | integer | Tourism popularity rank (1 = highest) |
  
  ### monthly_occupancy.csv
  Monthly hotel performance metrics.

| Column | Type | Description |
  |--------|------|-------------|
  | `hotel_id` | integer | Foreign key to hotels.csv |
  | `month` | integer | Month (1-12) |
  | `year` | integer | Year (2023-2024) |
  | `occupancy_rate` | numeric | Percentage of rooms occupied (0.0-1.0) |
  | `avg_daily_rate` | numeric | Average price per night in EUR |
  | `revenue_per_room` | numeric | Revenue per available room (RevPAR) |
  
  ### city_tourism.csv
  Monthly tourism statistics for each city.

| Column | Type | Description |
  |--------|------|-------------|
  | `city` | character | City name |
  | `month` | integer | Month (1-12) |
  | `year` | integer | Year (2023-2024) |
  | `tourist_arrivals` | integer | Number of tourists arriving |
  | `event_days` | integer | Number of event days in the month |
  | `avg_stay_length` | numeric | Average length of stay in days |
  
  ### economic_indicators.csv
  Monthly economic indicators for Austria.

| Column | Type | Description |
  |--------|------|-------------|
  | `month` | integer | Month (1-12) |
  | `year` | integer | Year (2023-2024) |
  | `inflation_rate` | numeric | Monthly inflation rate (decimal) |
  | `unemployment` | numeric | Unemployment rate (decimal) |
  | `consumer_confidence` | numeric | Consumer confidence index |
  
  ### reviews.csv
  Hotel guest reviews.

| Column | Type | Description |
  |--------|------|-------------|
  | `review_id` | integer | Primary key |
  | `hotel_id` | integer | Foreign key to hotels.csv |
  | `rating` | numeric | Rating (1.0-5.0) |
  | `review_date` | date | Date of the review |
  
  ### amenities.csv
  List of possible hotel amenities.

| Column | Type | Description |
  |--------|------|-------------|
  | `amenity_id` | integer | Primary key |
  | `amenity_name` | character | Name of the amenity |
  
  ### hotel_amenities.csv
  Many-to-many relationship between hotels and amenities.

| Column | Type | Description |
  |--------|------|-------------|
  | `hotel_id` | integer | Foreign key to hotels.csv |
  | `amenity_id` | integer | Foreign key to amenities.csv |
  

 
