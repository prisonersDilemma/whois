#===============================================================================
# TODO

* Proper packaging and dependency handling, and remove copies of tail.py,
  bytepos.py, and yyyymmdd.py. For now, just clone/pull them from github
  'https://github.com/prisonersDilemma/py3mods.git'.

* Sample of output missing data:
  NA      | 45.249.121.1     | NA

* Get rid of int types in args, because they have no strip method and make a
  special case for whether or not arg values can be quoted (they can't). Just
  take them all in as string and convert them to ints.
  buffer-size, tail-nlines, port all need to be converted

* After setting logging-level to DEBUG in whois.conf, and trying to  then write
  an early log message for the arguments/options __main__ was run with, nothing
  gets written. When I change that logger's priorty to info, it writes to the
  log. So, it seems as though, the arguments aren't taking. I think this is
  because the logger has already set up in config.py. But, I can change this
  later.

* How and when do we call func=set_option if invoked, when we are deleting it?

* May need to get abspath or expanduser of any pathnames.

* USERDIR & log_file need to be defined when run for the first time, or it'll be '~'.
  Get input for were to write user files, and where to store configs when run
  for the first time?

* Add some print statements to keep the user informed.

* Finish tests for tail.py

* Time tail in comparison to reading the whole file and only taking the last
  n items from the list. See ~/bin/python3/timeit_wrapper.py

* Write tests for config.py to test that "cascading options" works correctly.

* Make the targets simple "Namespace" objects, and still keep them in
  the dict by IP?

#===============================================================================
# NOTES

* Pretty sure I ran this earlier having imported the name date, and I used it
  fine and everything passed. Now, since I reorganized my packages, and I
  even made sure to import the subpackage, so that I could show where the
  module was coming from, it tried to run logilter.date.xxx as the `date`
  module from the standard library. The other issue could be that I added the
  parent directory to my PYTHONPATH environment variable, which may be
  creating the conflict. So, I'll try a completely absolute import.

* Actually, I don't even import the `date` module to logfilter anymore, just
  all of its functions. So, I guess it tried using `date` from the stdlib
  as a last resort?

* I removed the directory from my path, am still using an absolute path to
  the function, and am still having the same issue. WTF. So, I guess I'm going
  to have to rename the module.

* I had to change any paths to files used in my tests. For some reason the
  relative paths would no longer work. Probably because I changed the import
  statements in __init__.

* Can set as cron task to run daily.

#===============================================================================
# "MASTER list"
# Add to master list/database: append to the csv file:  name - cntry,asn,ip,timestamp
# These are the columns in the master list. Remember, it's comma-separated.
# So this first part is one column and this column is separated by dashes.
# ....................
# ASN / Name / Country,ASN,IP Address ,Date First Seen,ASN Lookup,IP Address Lookup,Country
#with open(MASTER, mode='a') as m:
#    m.write()
#===============================================================================
