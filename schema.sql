Table roles {
    id INT [pk, increment]
    role_name VARCHAR(50)
}

Table users {
    id INT [pk, increment]
    username VARCHAR(50)
    email VARCHAR(100)
    password VARCHAR(255)
    role_id INT
}

Ref: users.role_id > roles.id

Table manufacturers {
    id INT [pk, increment]
    name VARCHAR(100)
    country VARCHAR(100)
}

Table models {
    id INT [pk, increment]
    name VARCHAR(100)
    manufacturer_id INT
}

Table cars {
    id INT [pk, increment]
    model_id INT
    year INT
    color VARCHAR(50)
    vin VARCHAR(17)
    -- Add other 42 fields here
}

Ref: models.manufacturer_id > manufacturers.id
Ref: cars.model_id > models.id

Table listing_years {
  id int [pk, increment]
  year year [unique]
}

Table makes {
  id int [pk, increment]
  name varchar(50) [unique]
}

Table models {
  id int [pk, increment]
  make_id int [not null, ref: > makes.id]
  name varchar(50)
  
  indexes {
    (make_id, name) [unique]
  }
}

Table trims {
  id int [pk, increment]
  model_id int [not null, ref: > models.id]
  name varchar(50)
  description text
  
  indexes {
    (model_id, name) [unique]
  }
}

Table manufacturing_years {
  id int [pk, increment]
  year year [unique]
}

Table colors {
  id int [pk, increment]
  name varchar(50) [unique]
  color_type enum('Exterior', 'Interior')
}

Table body_types {
  id int [pk, increment]
  name varchar(50) [unique]
}

Table doors {
  id int [pk, increment]
  number_of_doors int [unique]
}

Table seats {
  id int [pk, increment]
  number_of_seats int [unique]
}

Table engine_types {
  id int [pk, increment]
  name varchar(50) [unique]
}

Table engines {
  id int [pk, increment]
  engine_type_id int [not null, ref: > engine_types.id]
  cylinders int
  engine_size_l decimal(3,1)
  horsepower int
}

Table transmissions {
  id int [pk, increment]
  type varchar(50) [unique]
}

Table drive_trains {
  id int [pk, increment]
  type varchar(50) [unique]
}

Table fuel_types {
  id int [pk, increment]
  name varchar(50) [unique]
}

Table title_statuses {
  id int [pk, increment]
  status varchar(50) [unique]
}

Table regions {
  id int [pk, increment]
  name varchar(100) [unique]
}

Table sources {
  id int [pk, increment]
  name varchar(100) [unique]
  source_url varchar(255)
  source_json text
  source_json_url varchar(255)
}

Table vehicles {
  id int [pk, increment]
  listing_year_id int [not null, ref: > listing_years.id]
  make_id int [not null, ref: > makes.id]
  model_id int [not null, ref: > models.id]
  trim_id int [not null, ref: > trims.id]
  manufacture_year_id int [not null, ref: > manufacturing_years.id]
  condition_type enum('New', 'Used')
  base_msrp decimal(10,2)
  price decimal(10,2)
  mileage int
  exterior_color_id int [ref: > colors.id, note: 'References colors where color_type = Exterior']
  interior_color_id int [ref: > colors.id, note: 'References colors where color_type = Interior']
  body_type_id int [ref: > body_types.id]
  door_id int [ref: > doors.id]
  seat_id int [ref: > seats.id]
  engine_id int [ref: > engines.id]
  transmission_id int [ref: > transmissions.id]
  drive_train_id int [ref: > drive_trains.id]
  fuel_type_id int [ref: > fuel_types.id]
  vin varchar(17) [unique, not null]
  torque_ft_lbs int
  torque_rpm int
  epa_combined_mpg decimal(4,1)
  epa_city_mpg decimal(4,1)
  epa_highway_mpg decimal(4,1)
  epa_electric_range_mi decimal(5,1)
  epa_time_to_charge_240v_hr decimal(4,1)
  battery_capacity_kwh decimal(5,1)
  state varchar(50)
  region_id int [ref: > regions.id]
  region_url varchar(255)
  accidents_reported int
  owner_count int
  rental_use boolean
  days_on_market int
  date_captured datetime
  date_added datetime [default: `CURRENT_TIMESTAMP`]
  date_modified datetime [default: `CURRENT_TIMESTAMP`, note: 'Automatically updated on modification in MySQL']

  indexes {
    (vin) [unique]
    (price)
    (date_captured)
  }
}

Table live_scraped_data {
  id int [pk, increment]
  vehicle_id int [not null, ref: > vehicles.id]
  price decimal(10,2)
  mileage int
  msrp decimal(10,2)
  date_captured datetime
  source_id int [not null, ref: > sources.id]

  indexes {
    (source_id)
  }
}

Table historical_data {
  id int [pk, increment]
  vehicle_id int [not null, ref: > vehicles.id]
  price decimal(10,2)
  mileage int
  msrp decimal(10,2)
  date_captured datetime
  source_id int [not null, ref: > sources.id]

  indexes {
    (source_id)
  }
}

Table images {
  id int [pk, increment]
  vehicle_id int [not null, ref: > vehicles.id]
  image_url varchar(255)
}

Table listing_raw_data {
  id int [pk, increment]
  vehicle_id int [not null, ref: > vehicles.id]
  raw_json json
}

Table tags {
  id int [pk, increment]
  name varchar(50) [unique]
}

Table vehicle_tags {
  vehicle_id int [ref: > vehicles.id]
  tag_id int [ref: > tags.id]
  
  indexes {
    (vehicle_id, tag_id) [unique]
  }
}

Table roles {
  id int [pk, increment]
  name varchar(50) [unique]
}

Table users {
  id int [pk, increment]
  username varchar(50) [unique, not null]
  password_hash varchar(255) [not null]
  role_id int [ref: > roles.id]
  created_at datetime [default: `CURRENT_TIMESTAMP`]
}

Table audit_trails {
  id int [pk, increment]
  vehicle_id int [ref: > vehicles.id]
  user_id int [ref: > users.id]
  action varchar(50)
  action_timestamp datetime [default: `CURRENT_TIMESTAMP`]
  ip_address varchar(45)
  
  indexes {
    (vehicle_id)
    (user_id)
  }
}
