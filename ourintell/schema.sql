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
	resourceName varchar(16) not null primary key unique
);

create table Users(
	Id int primary key not null auto_increment,
	userName varchar(32) not null unique,
    password char(60) not null,
    email varchar(120),
    is_verified boolean
);


create table subscriptions(
    Id int not null auto_increment unique primary key,
    userId int not null,
    trackedResource varchar(64) not null,
    trackedResourceType varchar(16) not null,
    ticketingMethod varchar(16) not null,
    ticketingAddress varchar(128) not null,
    
    
    foreign key(trackedResourceType) references TrackableResources(resourceName),
    foreign key(ticketingMethod) references TicketingMethods(ticketingMethod),
    foreign key(userId) references Users(id)
);

create table sentTickets(
    eventId varchar(256) not null,
	subscriptionId int not null,
    
	foreign key(eventId) references RecordedEvents(eventId),
    foreign key(subscriptionId) references Subscriptions(Id)
);

insert into ticketingmethods value('email',null);
insert into trackableresources value('network');
insert into ticketingmethods value('discord',null);
insert into trackableresources value('url');
insert into subscriptions(userId, trackedResourceType, ticketingMethod, ticketingAddress, trackedResource) value(1, 'network', 'email', 'spas', '0.0.0.0/8');

drop table sentTickets;
drop table userSubscriptions;
drop table Subscriptions;
drop table Users;
drop table TicketingMethods;
drop table TrackableResources;