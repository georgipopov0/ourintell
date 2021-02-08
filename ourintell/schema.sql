create database threat_data;
use threat_data;

create table RecordedEvents(
	eventId varchar(256) primary key not null unique,
    eventdata varchar(2047)
);

create table TicketingMethods(
	ticketingMethod varchar(256) not null primary key unique,
    methodDescription varchar(512)  
);

create table TrackableResources(
	resurceName varchar(128) not null primary key unique
);

create table Users(
	userId int primary key not null auto_increment,
	userName varchar(512) not null unique,
    password varchar(1024) not null,
    email varchar(254)
);

drop table Subscriptions;
create table Subscriptions(
	subscriptionId int not null auto_increment unique primary key,
    trackedResource varchar(128),
    ticketingMethod varchar(256),
    ticketignAdress varchar(256),
    
    foreign key(trackedResource) references TrackableResources(resurceName),
    foreign key(ticketingMethod) references TicketingMethods(ticketingMethod)
);

create table UserSubscriptions(
	userId int,
    subscriptionId int,
    
    foreign key(userId) references Users(userId),
	foreign key(subscriptionId) references Subscriptions(subscriptionId)
);

create table reportedEvents(
    eventId varchar(256),  
	subscriptionId int,
    
	foreign key(eventId) references RecordedEvents(eventId),
    foreign key(subscriptionId) references Subscriptions(subscriptionId)
)


