-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE public.players (
    name text NOT NULL,
    id_player serial NOT NULL,
    PRIMARY KEY (id_player)
);


CREATE TABLE public.matches (
    winner integer REFERENCES players(id_player),
    loser integer REFERENCES players(id_player),
    id_match serial NOT NULL,
    PRIMARY KEY (id_match)
);


