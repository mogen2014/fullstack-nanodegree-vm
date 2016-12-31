-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP TABLE IF EXISTS players, matches;


CREATE TABLE players ( id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE matches ( player integer references players(id),
						wins integer default 0,
						matches integer default 0);

-- the following line is for testing
-- insert into players (name) values ('joe1');
-- insert into players (name) values ('joe2');
-- insert into players (name) values ('joe3');
-- insert into players (name) values ('joe4');
-- insert into players (name) values ('joe5');
-- insert into players (name) values ('joe6');
-- insert into players (name) values ('joe7');
-- insert into players (name) values ('joe8');

-- insert into matches (player, wins, matches) values (1,3,3);
-- insert into matches (player, wins, matches) values (2,1,2);
-- insert into matches (player, wins, matches) values (3,1,3);
-- insert into matches (player, wins, matches) values (4,2,4);
-- insert into matches (player, wins, matches) values (5,4,2);
-- insert into matches (player, wins, matches) values (6,2,2);
-- insert into matches (player, wins, matches) values (7,1,1);
-- insert into matches (player, wins, matches) values (8,1,1);

