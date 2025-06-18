--Team Points per Season (join constructor_standings, races, constructors)--
create view cur_team_points as(
select
    c.constructorid,
    c.name,
    r.raceid,
    r.date,
    cs.points,
    cs.position
from event.datathon_2025_team_zeta.constructors as c
join event.datathon_2025_team_zeta.constructor_standings as cs
on c.constructorid = cs.constructorid
join event.datathon_2025_team_zeta.races as r
on cs.raceid = r.raceid
);
--Driver Points per Season (join driver_standings, races, drivers)--
create view cur_driver_points as (
select
    d.driverid,
    r.raceid,
    d.forename,
    d.surname,
    d.dob,
    ds.points,
    ds.position,
    r.date
from event.datathon_2025_team_zeta.driver_standings as ds
join event.datathon_2025_team_zeta.races as r
on ds.raceid = r.raceid
join event.datathon_2025_team_zeta.drivers as d
on ds.driverid = d.driverid
);
--Race Results with Team and Driver Info (join results, races, constructors, drivers)--
create view cur_race_reults as (
select 
    d.driverid,
    ra.raceid,
    c.constructorid,
    d.forename,
    d.surname,
    c.name,
    re.position,
    re.points,
    ra.date
from event.datathon_2025_team_zeta.results as re
join event.datathon_2025_team_zeta.races as ra
on re.raceid = ra.raceid
join event.datathon_2025_team_zeta.drivers as d
on re.driverid = d.driverid
join event.datathon_2025_team_zeta.constructors as c
on re.constructorid = c.constructorid
);
--Pit Stops (join pit_stops, races, drivers)--
create view cur_pit_stop_metrics as (
select
    d.driverid,
    r.raceid,
    d.forename,
    d.surname,
    r.date,
    ps.stop,
    ps.milliseconds,
    ps.lap
from event.datathon_2025_team_zeta.races as r
join event.datathon_2025_team_zeta.pit_stops as ps
on r.raceid = ps.raceid
join event.datathon_2025_team_zeta.drivers as d
on ps.driverid = d.driverid
);
