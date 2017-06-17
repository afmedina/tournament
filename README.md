# tournament
Intro to Relational Databases

A Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament. The game tournament uses the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

There are three files: tournament.sql, tournament.py, and tournament_test.py.

The file tournament.sql represents the database schema, in the form of SQL create table commands.

The file tournament.py represents the functions to operate the tournament database.

Finally, the file tournament_test.py contains unit tests that tests the functionsin tournament.py. You can run the tests from the command line, using the command:

python3 tournament_test.py.
