-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c vagrant
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament


CREATE TABLE players ( id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    winner INTEGER REFERENCES players(id),
    loser INTEGER REFERENCES players(id)
);

-- the following lines is for testing
insert into players (name) values ('joe1');
insert into players (name) values ('joe2');
insert into players (name) values ('joe3');
insert into players (name) values ('joe4');
insert into players (name) values ('joe5');
insert into players (name) values ('joe6');
insert into players (name) values ('joe7');
insert into players (name) values ('joe8');

insert into matches (winner, loser) values (3,4);
insert into matches (winner, loser) values (2,5);
insert into matches (winner, loser) values (1,6);
insert into matches (winner, loser) values (3,8);
insert into matches (winner, loser) values (4,3);
insert into matches (winner, loser) values (5,2);
insert into matches (winner, loser) values (6,1);
insert into matches (winner, loser) values (7,8);

