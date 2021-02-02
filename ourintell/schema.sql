drop database threat_data;
create database threat_data;
use threat_data;

create table RecordedEvents(
	eventId varchar(256) primary key not null unique,
    eventdata varchar(2047)
);

create table TicketingMethods(
	methodId int not null primary key unique auto_increment,
	ticketingMethod varchar(256) not  null,
    methodDescription varchar(512)  
);

create table roles(
	roleID int not null primary key unique auto_increment,
    roleName varchar(64),
    canView bool,
    canEdit bool
);

create table TrackableResources(
	resurceName varchar(128) not null primary key unique,
    dataType varchar(64) not null,
    onEventTriger bool not null
);

create table Organisations(
	organisationId int primary key not null auto_increment,
	organisationName varchar(512) not null unique,
    credentials varchar(1024) not null,
    email varchar(254) not null
);

create table Users(
	userId int primary key not null auto_increment,
	userName varchar(512) not null unique,
    credentials varchar(1024) not null,
    email varchar(254),
    organisationId int,
    foreign key(organisationId) references Organisations(organisationId)
);

create table Subscriptions(
	subscriptionId int not null auto_increment unique primary key,
    trackedResource varchar(128),
    ticketingMethodId int,
    ticketignAdress varchar(256),
    ticketFrequency int not null,
    enrollmentDate date not null,
    expiryDate date,
    price float4 not null,
    
    foreign key(trackedResource) references TrackableResources(resurceName),
    foreign key(ticketingMethodId) references TicketingMethods(methodId)
);

create table UserRoles(
	roleId int,
    userId int,
    
	foreign key(roleId) references Roles(roleId),
    foreign key(userId) references Users(userId)
);

create table UserSubscriptions(
	userId int,
    subscriptionId int,
    
    foreign key(userId) references Users(userId),
	foreign key(subscriptionId) references Subscriptions(subscriptionId)
);




