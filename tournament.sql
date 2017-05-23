-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP VIEW IF EXISTS wins_matches;
DROP VIEW IF EXISTS losses;
DROP VIEW IF EXISTS wins;

DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches;

CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE matches (
  winner INTEGER REFERENCES players(id),
  loser INTEGER REFERENCES players(id),
  PRIMARY KEY (winner, loser)
);

CREATE VIEW wins AS
  SELECT id, COUNT(winner) AS wins
  FROM players
  LEFT JOIN matches ON players.id = matches.winner
  GROUP BY id;

CREATE VIEW losses AS
  SELECT id, COUNT(winner) AS losses
  FROM players
  LEFT JOIN matches ON players.id = matches.loser
  GROUP BY id;

CREATE VIEW wins_matches AS
  SELECT wins.id, wins, wins+losses AS matches
  FROM wins, losses
  WHERE wins.id = losses.id;

CREATE VIEW standings AS
  SELECT players.id, name, wins, matches
  FROM players, wins_matches
  WHERE players.id = wins_matches.id
  ORDER BY wins DESC;
