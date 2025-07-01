SQL Staging;



CREATE TABLE vehicle_flat_staging (
  id SERIAL PRIMARY KEY,

  vin VARCHAR(17) UNIQUE NULL,
  make VARCHAR(50),
  model VARCHAR(50),
  trim_name  TEXT,
  trim_description TEXT,

  manufacturing_year INT,
  listing_year INT,

  condition_type VARCHAR(20),
  base_msrp DECIMAL(10,2),
  price DECIMAL(10,2),
  mileage INT,

  exterior_color VARCHAR(50),
  interior_color VARCHAR(50),

  body_type VARCHAR(50),
  doors INT,
  seats INT,

  engine_type VARCHAR(50),
  engine_cylinders INT,
  engine_size_l DECIMAL(3,1),
  horsepower INT,
  torque_ft_lbs INT,
  torque_rpm INT,

  transmission VARCHAR(50),
  drive_train VARCHAR(50),
  fuel_type VARCHAR(50),
  fuel_tank_capacity_gal DECIMAL(4,1),

  epa_combined_mpg DECIMAL(4,1),
  epa_city_mpg DECIMAL(4,1),
  epa_highway_mpg DECIMAL(4,1),
  epa_electric_range_mi DECIMAL(5,1),
  epa_charge_time_hr DECIMAL(4,1),
  battery_capacity_kwh DECIMAL(5,1),

  region VARCHAR(100),
  state_name VARCHAR(50),
  city VARCHAR(100),
  county VARCHAR(100),
  zipcode VARCHAR(20),


  accidents_reported INT,
  owner_count INT,
  rental_use BOOLEAN,

  date_captured TIMESTAMP,
  date_added TIMESTAMP,
  date_modified TIMESTAMP,
  days_on_market INT,

  source_name VARCHAR(100),
  source_url TEXT,
  image_url TEXT,
  source_json TEXT,
  source_id INT
);


