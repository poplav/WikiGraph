use WikiGraph;
drop table wikiGraph;

create table wikiGraph(source varchar(255),destination varchar(255));
create index index_source ON wikiGraph (source);
create index index_destination ON wikiGraph (destination);
alter ignore table wikiGraph add unique index uniqueRowIndex(source, destination);

insert into wikiGraph values("sourceTest1", "destinationTest1");
insert into wikiGraph values("sourceTest1", "destinationTest2");
insert into wikiGraph values("sourceTest1", "destinationTest3");
insert into wikiGraph values("sourceTest2", "destinationTest3");
insert into wikiGraph values("sourceTest3", "destinationTest3");
insert into wikiGraph values("sourceTest4", "destinationTest3");
insert into wikiGraph values("United_States", "United_States");

/* delete from wikiGraph where source = "sourceTest"; */

select * from wikiGraph;

select count(*) from wikiGraph;

/* Get the size in MB of the table wikiGraph */
SELECT table_name AS "wikiGraph",
round(((data_length + index_length) / 1024 / 1024), 2) "Size in MB"
FROM information_schema.TABLES
WHERE table_schema = "WikiGraph"
 AND table_name = "wikiGraph";