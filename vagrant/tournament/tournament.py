#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    cnn = psycopg2.connect("dbname=tournament")
    # cnn.autocommit = True
    return cnn


def deleteMatches():
    """Remove all the match records from the database."""
    cnn = connect()
    c = cnn.cursor()
    c.execute("delete from matches")
    cnn.commit()
    cnn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    cnn = connect()
    c = cnn.cursor()
    c.execute("delete from matches")
    c.execute("delete from players")
    cnn.commit()
    cnn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    cnn = connect()
    c = cnn.cursor()
    c.execute("select count(name) from players")
    results = c.fetchall()[0][0]
    cnn.close()
    return results


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    cnn = connect()
    c = cnn.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    cnn.commit()
    cnn.close()


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
    cnn = connect()
    c = cnn.cursor()
    # coalesce() function is used when a record is not exist,
    # and pick a default value for that record
    c.execute("""select id,name,coalesce(wins,0),coalesce(matches,0) 
                    from players left join matches 
                    on players.id=matches.player 
                    order by wins desc;""")

    results = c.fetchall()
    cnn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    cnn = connect()
    c = cnn.cursor()
    # when player wins get 1 score
    c.execute("""insert into matches
                (player, wins, matches)values (%d,%d,%d)""" %
              (winner, 1, 1))
    cnn.commit()
    # if player did not win, get 0
    c.execute("""insert into matches 
            (player, wins, matches) values (%d,%d,%d)""" %
              (loser, 0, 1))
    cnn.commit()
    cnn.close()


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

# the following lines are used for testing in this file
if __name__ == '__main__':
    print swissPairings()
