-- Create Schema

create schema zomata;

use zomata;

-- Create customer Table

create table customer(
	customer_id bigint NOT NULL auto_increment,
	name varchar(50) NOT NULL,
	email varchar(50),
	phone varchar(15) NOT NULL,
	location varchar(50) NOT NULL,
	signup_date date NOT NULL,
	is_premium boolean DEFAULT FALSE,
	preferred_cuisine varchar(50) DEFAULT NULL,
	total_orders int DEFAULT 0,
	average_rating decimal(3,1) DEFAULT 0.0,
	PRIMARY KEY(customer_id)
);

-- Create restaurant table

create table restaurant(
	restaurant_id bigint NOT NULL auto_increment,
    name varchar(50) NOT NULL,
    cuisine_type varchar(50) NOT NULL,
    location varchar(50) NOT NULL,
    owner_name varchar(50),
    average_delivery_time_min int NOT NULL,
    contact_number varchar(15) NOT NULL,
    rating decimal(3,1) DEFAULT 0.0,
    total_orders int DEFAULT 0,
    is_active boolean DEFAULT TRUE,
    PRIMARY KEY(restaurant_id)
);

-- Create order table

create table orders(
	order_id bigint NOT NULL auto_increment,
    customer_id bigint NOT NULL,
    restaurant_id bigint NOT NULL,
    order_date datetime NOT NULL,
    delivery_time datetime,
    status varchar(15) NOT NULL,
    total_amount decimal(10,2) NOT NULL,
    payment_mode varchar(20) NOT NULL,
    discount_applied decimal(10,2) DEFAULT 0.0,
    feedback_rating decimal(3,1) DEFAULT 0.0,
    PRIMARY KEY(order_id),
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY(restaurant_id) REFERENCES restaurant(restaurant_id)
);

-- Create delivery person table

create table delivery_person(
	delivery_person_id bigint NOT NULL auto_increment,
    name varchar(50) NOT NULL,
    contact_number varchar(15) NOT NULL,
    total_deliveries int DEFAULT 0,
    average_rating decimal(3,1) DEFAULT 0.0,
    location varchar(50),
    PRIMARY KEY(delivery_person_id)
);

-- Create delivery table

create table delivery(
	delivery_id bigint NOT NULL auto_increment,
    order_id bigint NOT NULL,
    delivery_person_id bigint NOT NULL,
    delivery_status varchar(20) NOT NULL,
    distance_in_km decimal(3,1),
    delivery_time_min int NOT NULL,
    estimated_time_min int NOT NULL,
    delivery_fee decimal(10,2) DEFAULT 0.0,
    vehicle_type varchar(10) NOT NULL,
    PRIMARY KEY(delivery_id),
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(delivery_person_id) REFERENCES delivery_person(delivery_person_id)
);
