#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # db.autocommit = True

    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error in function connect()")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    # cursor.execute("delete from matches")
    cursor.execute("truncate matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    # cursor.execute("delete from matches")
    # cursor.execute("delete from players")
    cursor.execute("truncate matches")
    cursor.execute("truncate players cascade")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    cursor.execute("select count(name) from players")
    results = cursor.fetchone()[0]
    db.close()
    return results


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    query = "insert into players (name) values (%s)"
    params = (name,)
    cursor.execute(query, params)
    db.commit()
    db.close()


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
    db, cursor = connect()
    # coalesce() function is used when a record is not exist,
    # and pick a default value for that record

    query = """
        select playermatches.id,
               playermatches.name,
               coalesce(winners.wins, 0) as wins,
               playermatches.matches
        from
            (select players.id as id,
                    players.name as name,
                    count(matches.id) as matches
             from players
             left join matches
             on players.id=matches.winner or players.id=matches.loser
             group by players.id) as playermatches
        left join
            (select winner as winnerid,
                    count(winner) as wins
             from matches group by winner) as winners
        on playermatches.id=winners.winnerid
        order by wins desc, matches desc
    """

    cursor.execute(query)
    results = cursor.fetchall()

    db.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    query = "insert into matches (winner, loser) values (%s, %s);"
    params = (winner, loser)
    cursor.execute(query, params)
    db.commit()
    db.close()


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
    standings = playerStandings()
    results = []
    index = 1
    tmp = []
    # loop all standings, because of they are ordered and even
    # number players, so every time pick tow of them as a pair
    for standing in standings:
        tmp.append((standing[0], standing[1]))
        if index % 2 == 0:
            results.append((tmp[0][0], tmp[0][1], tmp[1][0], tmp[1][1]))
            tmp = []
        index += 1
    return results
