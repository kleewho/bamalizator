create table race (
  id integer primary key,
  date text not null,
  city text not null,
  year integer not null,
  UNIQUE(date)
);

create table bibNumber (
  id integer primary key,
  bibNumber integer not null,
  year integer not null,
  UNIQUE(bibNumber,year)
);

create table route (
  id integer primary key,
  raceId integer not null,
  distance integer,
  category text not null,
  foreign key(raceId) references race(id),
  UNIQUE(raceId,category)
);

create table raceResult (
  id integer primary key,
  bibNumberId integer not null,
  routeId integer not null,
  time text,
  checkpointTime1 text,
  checkpointTime2 text,
  checkpointTime3 text,
  checkpointTime4 text,
  checkpointTime5 text,
  DNS boolean default false,
  DNF boolean default false,
  DSQ boolean default false,
  foreign key(bibNumberId) references bibNumber(id),
  foreign key(routeId) references route(id),
  UNIQUE(bibNumberId,routeId)
);

