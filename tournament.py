#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.excute("delete from matches")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.excute("delete from players")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.excute("select count(*) from players")
    DB.close()

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.excute("insert into players (name) values(%s)",(name,))
    DB.commit()
    DB.close()


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
    DB = connect()
    c = DB.cursor()
    c.excute("select * from players_standings order by wins desc")
    players = [{'id': str(row[0]), 'name': str(row[1]), 'wins': str(row[2]), 
    'matches': str(row[3])} for row in DB]
    DB.close()
    return players


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.excute("insert into matches (winner_id,loser_id) values(%s)",(winner,loser,))
    DB.commit()
    DB.close()
 
 
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

    DB = connect()
    c = DB.cursor()
    c.excute("select * from players_standings order by wins desc")
    
    players = [{'id': str(row[0]), 'name': str(row[1]), 'wins': str(row[2]), 
    'matches': str(row[3])} for row in DB]
    num_of_players = len(players)
    players_of_next_round = []
    i = 0
    t = {}
    for x in xrange(0,num_of_players-1):
        if i % 2 == 0:
            t.append('id1':str(players[x]['id']))
            t.append('name1':str(players[x]['name']))
            i += 1
        else :
            t.append('id2':str(players[x]['id']))
            t.append('name2':str(players[x]['name']))
            i += 1
            players_of_next_round.append(t)
            t = {}
    DB.close()
    return players_of_next_round


