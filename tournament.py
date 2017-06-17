#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()

        return db, cursor
    except:
        print("Could not connect with database %s" % database_name)


def deleteMatches():
    """Remove all the match records from the database."""
    DB, c = connect()
    c.execute("TRUNCATE matches;")
    DB.commit()
    DB.close()

    return True


def deletePlayers():
    """Remove all the player records from the database."""
    DB, c = connect()
    c.execute("TRUNCATE players CASCADE;")
    DB.commit()
    DB.close()

    return True


def countPlayers():
    """Returns the number of players currently registered."""
    DB, c = connect()
    c.execute("SELECT count(*) FROM players;")
    numPlayers = c.fetchone()
    DB.close()

    return numPlayers[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB, c = connect()
    query = "INSERT INTO players(name) VALUES (%s)"
    data = (name, )
    c.execute(query, data)
    DB.commit()
    DB.close()

    return True


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, c = connect()
    c.execute(
            "SELECT id_player, name, " +
            "COUNT(M1.winner) as wins, COUNT(M1.winner)+COUNT(M2.loser) " +
            "FROM players LEFT OUTER JOIN matches M1 " +
            "ON id_player = M1.winner " +
            "LEFT JOIN matches M2 ON id_player = M2.loser " +
            "group by id_player ORDER BY wins;")

    players = c.fetchall()
    DB.close()

    return players


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB, c = connect()
    query = "INSERT INTO matches(winner, loser) VALUES (%s, %s);"
    data = (winner, loser)
    c.execute(query, data)
    DB.commit()
    DB.close()

    return True


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    players = playerStandings()
    matchList = []
    it = iter(players)
    for p1, p2 in zip(it, it):
        matchList.append((p1[0], p1[1], p2[0], p2[1]))

    return matchList
