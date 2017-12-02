In order to initialize the logger, it needs to open a file. Currently, the
logger is being initialized in __init__.py, which is before the arguments
are parsed from the config ('.whois.conf'), and the command-line.

It's our first time running...
    assume defaults
    read conf if exists
    parse cli args

Before collapsing the 3 dicts, and before creating any files, we need to know
where we can write, which can be given us on the cli. If not, we can write to
the defaults. If the args were in conf, that would mean they created the file,
and are using it.


Check cli-args for if user-dir diffs from defaults. If so, use that, and create
the directory there, and write our files there.

If user-dir doesn't exist, it's our first time running, regardless of what it is.


#===============================================================================
# options.py
#
# DEFAULTS
# set[-option] cmd writes the options/values to the config file, making changes
# "permanent". Command-line args have the highest precedence (so they get
# applied last), and override any defaults or config file settings:
# defaults < config file < command-line args
#
# Add an option to display all defaults, or, optionally, of a [given] option?
#
#
# Set some defaults in the config. Also try changing some of the script-dependent
# variables (--logging-file, --config-file, etc).
#===============================================================================
# argparse notes:
#
# %(prog)s format specifier for program name, can be used in help strings.
#
# dest puts the name of the invoking subparser in the Namespace as cmd.
#
# Assign attributes to an already existing object, with the namespace='',
# option to parse_args.
#
# parse_known_args() won't error if unknown args. Returns a 2-tuple, with the
# Namespace, and the remaining in a list.
#
# Automatically opens the arg as a file with the requested
# mode, buffer size, encodings, and error handling, and
# understands '-' as stdin & stdout.
#argsparse.FileType,
#argsparse.ArgumentDefaultsHelpFormatter # (prints default values in help)
#
#
# This is never even gotten to. It automatically invokes its own help when
# help is passed, even when add_help=False
#===============================================================================
# Misc code:
#print(f'CONFIGDIR: {CONFIGDIR}')
#print(f'CONFIGFILE: {CONFIGFILE}')
#print(f'LOGNAME: {LOGNAME}')
#print(f'LOGFILE: {LOGFILE}')
#print(f'LOGLEVELS: {LOGLEVELS}')
#print(f'LOG_LEVEL: {LOG_LEVEL}')
#print(f'SCRIPTHOME: {SCRIPTHOME}')
#print(f'SCRIPTNAME: {SCRIPTNAME}')
#print(f'USERHOME: {USERHOME}')
#
#if not args.cmd: opts = set_option.parse_args()
#print(f'args: {args}\n')
#print(f'opts: {opts}\n')
# Merge args & opts; opts first, b/c they're more long-term.
#args = dict(**vars(opts))
#args.update(**vars(_args))
#
#print(f'CONFIGS: {CONFIGS}\n')
#print(f'ARGS+CONFIGS: {ARGS}\n')
#print(f'ARGS+args: {ARGS}\n')
#for k,v in ARGS.items():
#    print(k,v)
#
# Create my own help.
#if args.help:
#    print('Printing my help.')
#    parser.print_usage()
#    parser.print_help()
#    parser.exit(0)
#===============================================================================






#===============================================================================
# Tail will tail the whole file. But we will break the loop when we find
# a date before our target date. Dates after our target date may be
# possible, however.

# When we find a date that is before the target date, we should finish the
# batch of lines we are currently processing, because we could have requested
# more lines (default is 100) than there are targets found. So, if the current
# day has only say 5 new entries, and the prior day, our target, has 40 entries
# (these are the targets we are expecting to get back), then tailing 100 lines
# will return the last 100 lines of the file, in order. So, the first 55
# entries are all going to be before our target date, and we are going to
# process them first.
#
# It is also conceivable that testing only the day is not enough. Consider a
# sample that has the following:
# '2017-02-28'
# '2017-11-10'
# '2017-11-11'
# and we want only the targets for yesteray, and want to quit when we find a
# date prior to that. This can never happen, and unless we are more specific
# about the particular date, we will process them all (and possibly return
# them all).
#
# It seems that, if the bufsz is too small, I may get back only a partial line,
# which may not contain a date. So it thinks we found the header or something
# else, and quits.
#
#
#
# Somehow I'm iterating twice

# Gettind different results when nlines=2 vs nlines=100. In the latter case,
# an IP was messed up.
# With bufsz=256, it quits after one iter?

# It's like the first chunk is not all the lines, and the next chunk, which
# is supposed to be just the remaining lines is all of them.

# And if a line isn't in full, say 1 or 2 numbers gets stripped from the IP,
# it'll become a unique key and get added to the dict, so long as the date
# is right.

# I need a way of either ensuring the integrity of the lines, or rejecting
# invalid IP patterns. Even checking the pattern isn't a guarantee, since:
# 192.168.1.1 != 92.168.1.1, even if the two may be from the same entry.
#
# Regardless, I need to make sure that broken lines are caught and joined.

# But for now, why the hell am I not getting only the remainder on the second
# iteration?

# Tail handled the chunks fine.


# When I request a bufsz that is too small, then, on the second iteration, it
# appears that I'm not getting what remains in the file, but the whole file.
