#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


class MyDB(object):
    """Handles connecting to a DB, executing a query, and closing the connection gracefully.
    """
    _db_connection = None
    _db_cur = None

    def __init__(self):
        self._db_connection = connect()
        self._db_cur = self._db_connection.cursor()

    def query(self, query, params=None):
        return self._db_cur.execute(query, params)

    def cursor(self):
        return self._db_cur

    def commit(self):
        self._db_connection.commit()

    def __del__(self):
        self._db_connection.close()


def deleteMatches():
    """Remove all the match records from the database."""
    db = MyDB()
    db.query("DELETE FROM matches;")
    db.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    db = MyDB()
    db.query("DELETE FROM players;")
    db.commit()


def countPlayers():
    """Returns the number of players currently registered."""
    db = MyDB()
    db.query("SELECT COUNT(*) from players;")

    row = db._db_cur.fetchone()

    return row[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = MyDB()
    db.query("INSERT INTO players (name) VALUES (%s);", (name,))
    db.commit()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = MyDB()
    db.query("select players.id, name, wins, matches from players, wins_matches where players.id = wins_matches.id order by wins desc;")
    return db.cursor().fetchall()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = MyDB()
    db.query("insert into matches (winner, loser) values (%s, %s);", (winner, loser))
    db.commit()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player' name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    n = len(standings)

    pairings = list()

    for i in range(0, n, 2):
        first = standings[i]
        second = standings[i + 1]

        pairings.append((first[0], first[1], second[0], second[1]))

    return pairings
