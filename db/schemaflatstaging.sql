1. Reference Tables (Lookup Tables)
CREATE TABLE listing_years (
  id SERIAL PRIMARY KEY,
  year INT UNIQUE
);

CREATE TABLE makes (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE,
  code VARCHAR(5) UNIQUE
);

CREATE TABLE models (
  id SERIAL PRIMARY KEY,
  make_id INT NOT NULL REFERENCES makes(id),
  name VARCHAR(50),
  code VARCHAR(5) UNIQUE,
  UNIQUE (make_id, name)
);

CREATE TABLE trims (
  id SERIAL PRIMARY KEY,
  model_id INT NOT NULL REFERENCES models(id),
  name VARCHAR(50),
  description TEXT,
  UNIQUE (model_id, name)
);

CREATE TABLE manufacturing_years (
  id SERIAL PRIMARY KEY,
  year INT UNIQUE
);

CREATE TABLE colors (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE,
  color_type VARCHAR(20) CHECK (color_type IN ('Exterior', 'Interior'))
);

CREATE TABLE body_types (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE
);

CREATE TABLE doors (
  id SERIAL PRIMARY KEY,
  number_of_doors INT UNIQUE
);

CREATE TABLE seats (
  id SERIAL PRIMARY KEY,
  number_of_seats INT UNIQUE
);

CREATE TABLE engine_types (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE
);

CREATE TABLE engines (
  id SERIAL PRIMARY KEY,
  engine_type_id INT NOT NULL REFERENCES engine_types(id),
  cylinders INT,
  engine_size_l DECIMAL(3,1),
  horsepower INT
);

CREATE TABLE transmissions (
  id SERIAL PRIMARY KEY,
  type VARCHAR(50) UNIQUE
);

CREATE TABLE drive_trains (
  id SERIAL PRIMARY KEY,
  type VARCHAR(50) UNIQUE
);

CREATE TABLE fuel_types (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE
);

CREATE TABLE title_statuses (
  id SERIAL PRIMARY KEY,
  status VARCHAR(50) UNIQUE
);

CREATE TABLE conditions (
  id SERIAL PRIMARY KEY,
  type VARCHAR(50) UNIQUE
);

CREATE TABLE regions (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE
);

CREATE TABLE locations (
  id SERIAL PRIMARY KEY,
  state_name VARCHAR(50),
  city VARCHAR(100),
  county VARCHAR(100),
  zipcode VARCHAR(20),
  region VARCHAR(100)
);



2. Metrics Tables

CREATE TABLE epa_metrics (
  id SERIAL PRIMARY KEY,
  epa_combined_mpg DECIMAL(4,1),
  epa_city_mpg DECIMAL(4,1),
  epa_highway_mpg DECIMAL(4,1),
  epa_electric_range_mi DECIMAL(5,1),
  epa_time_to_charge_240v_hr DECIMAL(4,1),
  battery_capacity_kwh DECIMAL(5,1)
);

CREATE TABLE torque (
  id SERIAL PRIMARY KEY,
  torque_ft_lbs INT,
  torque_rpm INT
);


3. Core Vehicle Tables

CREATE TABLE base_vehicles (
  id SERIAL PRIMARY KEY,
  make_id INT NOT NULL REFERENCES makes(id),
  model_id INT NOT NULL REFERENCES models(id),
  trim_id INT NOT NULL REFERENCES trims(id),
  manufacture_year_id INT NOT NULL REFERENCES manufacturing_years(id),
  exterior_color_id INT REFERENCES colors(id),
  interior_color_id INT REFERENCES colors(id),
  body_type_id INT REFERENCES body_types(id),
  door_id INT REFERENCES doors(id),
  seat_id INT REFERENCES seats(id),
  engine_id INT REFERENCES engines(id),
  transmission_id INT REFERENCES transmissions(id),
  drive_train_id INT REFERENCES drive_trains(id),
  fuel_type_id INT REFERENCES fuel_types(id),
  fuel_tank_capacity_gal DECIMAL(4,2),
  epa_metrics_id INT REFERENCES epa_metrics(id),
  torque_id INT REFERENCES torque(id)
);

CREATE TABLE vehicles (
  id SERIAL PRIMARY KEY,
  base_vehicle_id INT NOT NULL REFERENCES base_vehicles(id),
  location_id INT NOT NULL REFERENCES locations(id),
  listing_year_id INT NOT NULL REFERENCES listing_years(id),
  vin VARCHAR(17) UNIQUE,
  price DECIMAL(10,2),
  msrp DECIMAL(10,2),
  mileage INT,
  title_status_id INT REFERENCES title_statuses(id),
  condition_id INT REFERENCES conditions(id),
  days_on_market INT,
  date_captured TIMESTAMP,
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

 4. Additional Vehicle Data Tables
CREATE TABLE vehicle_colors (
  id SERIAL PRIMARY KEY,
  vehicle_id INT NOT NULL REFERENCES vehicles(id),
  color_id INT NOT NULL REFERENCES colors(id),
  color_type VARCHAR(20) CHECK (color_type IN ('Interior', 'Exterior'))
);


 5. Historical & Live Data Tables
CREATE TABLE live_scraped_data (
  id SERIAL PRIMARY KEY,
  vehicle_id INT NOT NULL REFERENCES vehicles(id),
  listing_year_id INT NOT NULL REFERENCES listing_years(id),
  price DECIMAL(10,2),
  mileage INT,
  msrp DECIMAL(10,2),
  date_captured TIMESTAMP,
  source_id INT NOT NULL REFERENCES sources(id)
);

CREATE TABLE historical_data (
  id SERIAL PRIMARY KEY,
  vehicle_id INT NOT NULL REFERENCES vehicles(id),
  listing_year_id INT NOT NULL REFERENCES listing_years(id),
  price DECIMAL(10,2),
  mileage INT,
  msrp DECIMAL(10,2),
  date_captured TIMESTAMP,
  date_archived TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  source_id INT NOT NULL REFERENCES sources(id)
);


6.Sources Table
CREATE TABLE sources (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE,
  source_url VARCHAR(255),
  source_json TEXT,
  source_json_url VARCHAR(255),
  image_url VARCHAR(255)
);

7. Images and Raw Listings
CREATE TABLE images (
  id SERIAL PRIMARY KEY,
  vehicle_id INT NOT NULL REFERENCES vehicles(id),
  image_url VARCHAR(255)
);

CREATE TABLE listing_raw_data (
  id SERIAL PRIMARY KEY,
  vehicle_id INT NOT NULL REFERENCES vehicles(id),
  raw_json JSON
);


8. Tagging and Categorization
CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE
);

CREATE TABLE vehicle_tags (
  vehicle_id INT REFERENCES vehicles(id),
  tag_id INT REFERENCES tags(id),
  PRIMARY KEY (vehicle_id, tag_id)
);


9. User Management and Audit Trail

CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role_id INT REFERENCES roles(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_trails (
  id SERIAL PRIMARY KEY,
  vehicle_id INT REFERENCES vehicles(id),
  user_id INT REFERENCES users(id),
  action VARCHAR(50),
  action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ip_address VARCHAR(45)
);

10. Index Recommendations (Optional);
CREATE INDEX idx_vehicle_price ON vehicles(price);
CREATE INDEX idx_vehicle_date_captured ON vehicles(date_captured);





