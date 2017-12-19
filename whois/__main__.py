#!/usr/bin/env python3.6
__date__ = '2017-11-15'
__version__ = (0,2,0)

from logging import basicConfig, getLevelName, getLogger
from re import sub
from os import getcwd #testing
from os import mkdir, sys
from os.path import basename, exists, expanduser, join
from subprocess import run
from . import PKGPATH # Python free module-level variable, available to __init__.
from . import argparser
from . import database
from . import nacat
from . import targets
from . import query
import offset
import tail
import yyyymmdd


if __name__ == '__main__':

    opts = argparser.parse_args()
    #print(opts)
    #if opts.query: # list of args
    #    query.main(opts.query)
    #sys.exit(0)


    # Configure and Initialize the logger.
    LOGFILE = f'{argparser.WHOISHOME}/{__package__}.log'
    basicConfig(filename=LOGFILE,
                level=20, # INFO; defines the root logging level
                format='[%(name)s] %(levelname)s: %(asctime)s: %(message)s',
                datefmt='%I:%M:%S%p',
                filemode='w') # Overwrite existing logs.

    logger = getLogger('main') #__name__
    logger.setLevel(opts.logging_level) # str -> int
    logger.debug(f'"logging_level": {getLevelName(logger.level)} ({logger.level})')

    #===============================================================================
    # Check options.
    #print(opts)
    # Print as mult. columns.
    # Indent each option=value when writing to the log, to make it easier to read.
    #logopts = ''.join((_.join(['  ', '\n']) for _ in str(opts).splitlines())).rstrip('\n') # strip the last newline.
    #numopts = len(opts)
    #columns = table.ceildiv(numopts, 3)
    #print(numopts)
    #print(columns)
    #logger.debug(f'`{__package__}` running with options:\n{logopts}')
    #print(f'log_file: {opts.log_file}')
    #print(f'date: {opts.date}')
    #print(f'nlines: {opts.nlines}, type: {type(opts.nlines)}')
    #print(f'bufsz: {opts.bufsz}, type: {type(opts.bufsz)}')
    #print(f'Logging level: {opts.logging_level}')
    #print(f'Logging level: {logger.level}')
    #===============================================================================
    #
    #===============================================================================
    # Main program logic.
    #===============================================================================

    #if opts.cmd
    # Handle queries, or do parsing.
    #query.n_results_by_daterange()


    # Assemble targets dict from the Splunk log.
    trgts = targets.gettargets(opts.log_file, opts.date, opts.nlines, opts.bufsz, opts.newline)
    logger.info(f'trgts found: {len(trgts)}') # done in gettargets


    # Assemble targets query from the dict and call nacat.
    output = nacat.nacat( opts.hostname, opts.port, nacat.join_msg(*trgts))
    logger.debug(f'`nacat` returned with an output string of len: {len(output)}')


    # Ignore the first line in the output, which is a header. Not all lines
    # will have all elements. Parse the lines. Normalize the data elements.
    # Remove duplicates (automatically done by dict.update). Add them to trgts.
    output_lines = output.splitlines()


    # If no output, quit. We probably couldn't connect or tried to query 0 IPs,
    # since we got nothing in return, so exit and try again later (for now).
    try:
       header_line  = output_lines[0]
       logger.debug(f'presumed header line in the output from `nacat`: {header_line}')
    except IndexError:
       sys.stderr.write(f'Trouble connecting to {opts.hostname}. Try again later.\n')
       sys.exit(-1)


    # Format necessary output, and combine the data with the IP & timestamp found
    # in gettargets.
    for line in output_lines[1:]: # Skip the first line; the header.
        try:
            asn, ipaddr, name_cntry = line.split('|')
            asn = asn.strip()
            ipaddr = ipaddr.strip()
            name_cntry = name_cntry.strip()
            #name_cntry = sub(r'(, |,)', ' - ', name_cntry) # squeeze?
            try:
                name, cntry = name_cntry.rsplit(',', 1)
                name = sub(r'(, |,)', ' - ', name)
                name = name.lstrip() # remove a space on the left
                cntry = cntry.lstrip(' ') # removes a leading whitespace
            except ValueError:
                logger.warning(f'Exception raised parsing `nacat` output for '
                               f'secondary values "name", "cntry":\n{line}\n'
                               'Resorting to defaults.')
                name = name_cntry if name_cntry else 'NULL'
                cntry = 'NULL'

            trgts[ipaddr].update({'ASN': f'AS{asn}', 'name': name, 'country': cntry}) # 'country': cntry})

        except ValueError:
            logger.warning(f'Exception raised parsing `nacat` output for primary '
                           'values "asn", "ipaddr", "name_cntry":\n{line}\n'
                           'This item will not be updated in the database.')


    # Daily List. Data is changed daily (overwritten). Format data. Append to csv.
    # No header, with following format: name - country,ASN,ipaddr,timestamp
    logger.debug(f'Writing {len(trgts)} lines to daily list file: {opts.list_file}')

    lines = []
    for trgt in trgts:
        line = (trgts[trgt]['name'], #.lstrip(), # a space on the left... should be taken care of during parsing.
                trgts[trgt]['country'],
                trgts[trgt]['ASN'],
                trgt,
                trgts[trgt]['timestamp'])

        lines.append(line)

    # Sort the lines by timestamp (earliest first). Each line is a list of strings.
    lines.sort(key=lambda x: x[-1])

    with open(opts.list_file, mode='w') as f:
        # Convert each line (list) to a comma-separated string, ended with a newline.
        [f.write(','.join(line) + '\n') for line in lines]


    # If no '.db' extension, append.
    opts.database_file = opts.database_file if opts.database_file.endswith('.db') \
                            else ''.join([opts.database_file, '.db'])
    if not exists(opts.database_file):
        database.create_database(opts.database_file)
        logger.info(f'database: {opts.database_file} created.')


    # Only create the table if we have data; make KEYS dynamically gotten from data.
    KEYS = ['ASN', 'IPADDR', 'NAME', 'COUNTRY', 'TIMESTAMP']
    # Create a table (and the database), only if they do not exist.
    database.create_table(opts.database_file, KEYS, opts.table_name)


    # Compose and insert the records (rows) into the database table.
    logger.info(f'inserting {len(trgts)} records into table: {opts.table_name}')
    for trgt in trgts:
        # Send in values as a tuple; prevents SQL injection.
        VALUES = (trgts[trgt]['ASN'],
                  trgt, # IP
                  trgts[trgt]['name'],
                  trgts[trgt]['country'],
                  trgts[trgt]['timestamp'])
        #logger.debug(f'inserting values: {VALUES}')
        database.insert_record(opts.database_file, VALUES, opts.table_name)


    #===============================================================================
    # Temporary fix for making a copy of daily-list to other admin's home.
    ADMIN = 'ec2-user'
    ADMIN_HOME = f'/home/{ADMIN}'
    LIST_FILE_NAME = basename(opts.list_file)
    ADMIN_LIST = f'{ADMIN_HOME}/{LIST_FILE_NAME}'
    run([ 'sudo', 'cp', opts.list_file, ADMIN_LIST, ])
    run([ 'sudo', 'chown', ADMIN, ADMIN_LIST, ])
    run([ 'sudo', 'chgrp', ADMIN, ADMIN_LIST, ])
    #===============================================================================


    # Notify user of latest results.
    num_new_targets = len(trgts)
    print(f'{num_new_targets} targets written to {opts.list_file}.')
    print(f'{num_new_targets} added to the database: {opts.database_file}.')
    sys.exit(0)
