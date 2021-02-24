-- drop database threat_data;
create database threat_data;
use threat_data;

create table recorded_events(
	Id varchar(256) primary key not null unique,
    event_data varchar(2047)
);

create table ticketing_methods(
	method varchar(16) not null primary key unique
);

create table trackable_resource_types(
	resource_type varchar(16) not null primary key unique
);

create table users(
	Id int primary key not null auto_increment,
	username varchar(32) not null unique,
    password char(60) not null,
    email varchar(120),
    is_verified boolean
);


create table subscriptions(
    Id int not null auto_increment unique primary key,
    userId int not null,
    tracked_resource varchar(64) not null,
    tracked_resource_type varchar(16) not null,
    ticketing_method varchar(16) not null,
    ticketing_address varchar(128) not null,
    is_verified bool not null,
    
    
    foreign key(tracked_resource_type) references trackable_resource_types(resource_type),
    foreign key(ticketing_method) references ticketing_methods(method),
    foreign key(userId) references users(id)
);

insert into users(username, password, email, is_verified) value('admin','admin','admin',1);
insert into ticketing_methods value('email');
insert into trackable_resource_types value('network');
insert into ticketing_methods value('discord');
insert into trackable_resource_types value('url');
insert into subscriptions(userId, tracked_resource_type, ticketing_method, ticketing_address, tracked_resource, is_verified) value(1, 'network', 'email', 'spas', '0.0.0.0/8', false);

-- drop table recorded_events;
-- drop table sentTickets;
-- drop table usersubscriptions;
-- drop table subscriptions;
-- drop table users;
-- drop table ticketing_methods;
-- drop table tackable_resource_types;