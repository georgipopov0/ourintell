create database threat_data;
use threat_data;

create table RecordedEvents(
	eventId varchar(256) primary key not null unique,
    eventdata varchar(2047)
);

drop table TicketingMethods;
create table TicketingMethods(
	ticketingMethod varchar(16) not null primary key unique,
    methodDescription varchar(32)  
);
drop table TrackableResources;

drop table Users;
create table TrackableResources(
	resurceName varchar(16) not null primary key unique
);

create table Users(
	userId int primary key not null auto_increment,
	userName varchar(32) not null unique,
    password char(60) not null,
    email varchar(120)
);

drop table Subscriptions;
create table Subscriptions(
	subscriptionId int not null auto_increment unique primary key,
    trackedResource varchar(128),
    ticketingMethod varchar(16),
    ticketignAdress varchar(128),
    
    foreign key(trackedResource) references TrackableResources(resurceName),
    foreign key(ticketingMethod) references TicketingMethods(ticketingMethod)
);

drop table userSubscriptions;
create table UserSubscriptions(
	userId int,
    subscriptionId int,
    
    foreign key(userId) references Users(userId),
	foreign key(subscriptionId) references Subscriptions(subscriptionId)
);

drop table reportedEvents;
create table reportedEvents(
    eventId varchar(256),  
	subscriptionId int,
    
	foreign key(eventId) references RecordedEvents(eventId),
    foreign key(subscriptionId) references Subscriptions(subscriptionId)
)


