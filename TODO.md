# TODO:
* Add keyword arg for --date for "yesterday"

* Fix if table doesn't exist, make it. If the script runs and errors out,
  the database gets created, but not the table. And when re-run, it expects
  the table to be created (I guess because the database file exists) and fails
  when trying to insert the records.

* Some values for COUNTRY and TIMESTAMP appear to be misaligned in the database.
  Not sure if this is real or just screwed displaying of the output. Note: this
  was observed querying the database from the sqlite3 shell via tmux via the
  server.

* Make sure hanging space on left of NAME doesn't return to daily-list.csv after
  change I made.

* Use the sort method for daily-list before inserting to database, too.

* Why doesn't cmd='query' when sub-command is used?
