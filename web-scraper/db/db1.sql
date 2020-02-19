create table race (
  id integer primary key,
  date text not null,
  city text not null,
  year integer not null
);

create table bibNumber (
  id integer primary key,
  number integer not null,
  year integer not null
);

create table route (
  id integer primary key,
  raceId integer not null,
  distance integer not null,
  category text not null,
  foreign key(raceId) references race(id)
);

create table raceResult (
  id integer primary key,
  bibNumberId integer not null,
  raceId integer not null,
  routeId integer not null,
  time text,
  checkpointTime1 text,
  checkpointTime2 text,
  checkpointTime3 text,
  checkpointTime4 text,
  checkpointTime5 text,
  DNS boolean default false,
  DNF boolean default false,
  foreign key(bibNumberId) references bibNumber(id),
  foreign key(routeId) references route(id),
  foreign key(raceId) references race(id)
);

insert into race(date,city,year) values ('2019-04-14','Rybnik',2019);
insert into route(raceId,distance,category) values (1,28,'Hobby');
