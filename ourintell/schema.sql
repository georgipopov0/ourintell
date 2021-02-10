create database threat_data;
use threat_data;

create table RecordedEvents(
	Id varchar(256) primary key not null unique,
    eventdata varchar(2047)
);

create table TicketingMethods(
	ticketingMethod varchar(16) not null primary key unique,
    methodDescription varchar(32)  
);

create table TrackableResources(
	resurceName varchar(16) not null primary key unique
);

create table Users(
	Id int primary key not null auto_increment,
	userName varchar(32) not null unique,
    password char(60) not null,
    email varchar(120),
    is_verified boolean
);


create table Subscriptions(
    Id int not null auto_increment unique primary key,
    trackedResource varchar(128) not null,
    ticketingMethod varchar(16) not null,
    ticketedAddress varchar(128) not null,
    
    foreign key(trackedResource) references TrackableResources(resurceName),
    foreign key(ticketingMethod) references TicketingMethods(ticketingMethod)
);


create table UserSubscriptions(
	userId int not null,
    subscriptionId int not null,
    
    foreign key(userId) references Users(userId),
	foreign key(subscriptionId) references Subscriptions(subscriptionId)
);

create table sentTickets(
    eventId varchar(256) not null,
	subscriptionId int not null,
    
	foreign key(eventId) references RecordedEvents(eventId),
    foreign key(subscriptionId) references Subscriptions(subscriptionId)
);

drop table sntTickets;
drop table userSubscriptions;
drop table Subscriptions;
drop table Users;
drop table TicketingMethods;
drop table TrackableResources;