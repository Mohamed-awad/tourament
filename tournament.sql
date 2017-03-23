-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE TABLE players ( id int serial primary key,
                     name text not null
                     );

CREATE TABLE matches ( id int serial primary key,
                     winner_id int references players(id),
                     loser_id int references players(id)
                     );

CREATE TABLE players_standings ( id int primary key references players(id),
                     name text references players(name),
                     wins int set default 0,
                     matches int set default 0
                     );



