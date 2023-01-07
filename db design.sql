-- ! This file is for tables and indices declaration.
-- ! For query statements, please refer to comments in './LineBot/db.py'

create table record (
    siteid      smallint,
    aqi         smallint check (aqi >= 0),
    status      smallint check (status >= 1 and status <= 6),
    so2         numeric(4, 1) check (so2 >= 0),
    co          numeric(5, 2) check (co >= 0),
    o3          numeric(4, 1) check (o3 >= 0),
    o3_8hr      numeric(4, 1) check (o3_8hr >= 0),
    pm10        smallint check (pm10 >= 0),
    pm2_5       smallint check (pm2_5 >= 0),
    no2         numeric(4, 1) check (no2 >= 0),
    nox         numeric(4, 1) check (nox >= 0),
    no          numeric(4, 1) check (no >= 0),
    wind_speed  numeric(4, 1) check (wind_speed >= 0 and wind_speed <= 360),
    wind_direc  smallint check (wind),
    publishtime timestamp,
    co_8hr      numeric(4, 1) check (co_8hr >= 0),
    pm2_5_avg   smallint check (pm2_5_avg >= 0),
    pm10_avg    smallint check (pm10_avg >= 0),
    so2_avg     smallint check (so2_avg >= 0),

    primary key (siteid, publishtime),
    foreign key (siteid) references site
)

create table site (
    siteid      smallint,
    sitename    varchar(10),
    county      varchar(5),
    longitude   numeric(7, 4) check (longitude >= 0 and longitude <= 180),
    latitude    numeric(6, 4) check (latitude >= 0 and latitude <= 90),
    primary key (siteid)
)

create table user_ (
    userid char(33),
    lastsiteid smallint,
    primary key (userid),
    foreign key (lastsiteid) references site
)

create table schedule (
    userid char(33),
    siteid smallint,
    time_ smallint check (time_ >= 0 and time_ <= 23),
    primary key (userid, siteid, time_),
    foreign key (userid) references user_,
    foreign key (siteid) references site
)

create index index_record_publishtime on record (publishtime);
create index index_user_userid on user_ (userid);