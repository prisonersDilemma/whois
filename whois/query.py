#!/usr/bin/env python3.6
__doc__ = """\
At least a temporary solution for making queries on the database.
"""
__date__ = '2017-12-12'
__version__ = (0,0,1)

from argparse import ArgumentParser

#from database import select_fields_from
#from whois.database import select_fields_from
from .database import select_fields_from
import yyyymmdd # daterange, tomorrow,


query_parser = ArgumentParser(prog='query',
    description='Query the database.')


def _parse_args(args=None):

    query_parser.add_argument('--date', '-d',
        type=str,
        default=yyyymmdd.yesterday(),
        help='single date to query')

    # default is tomorrow, as daterange upperbound is not inclusive.
    # default can't be set here, or args will be appended to.
    query_parser.add_argument('--date-range', '-r',
        metavar='YYYY-MM-DD',
        action='append',
        nargs='?',
        help='date(s) to filter database records by, given in YYYY-MM-DD format')

    query_parser.add_argument('--field', '-f',
        default='ASN',
        choices=['ASN', 'IPADDR', 'NAME', 'COUNTRY', 'TIMESTAMP'],
        type=str,
        help='database field to target')

    query_parser.add_argument('--number', '-n',
        type=int,
        metavar='N',
        default=10,
        help='number of top results to filter')

    args = query_parser.parse_args(args) if args else query_parser.parse_args()


    #if args.date_range is None:
    #    args.date_range = [yyyymmdd.tomorrow()]

    return args


def n_results_by_date(*args, **kwargs): # field, date, n=10, part=False
    """Return a list of *n* 2-tuples of totals (field-value, total)
    filtered from the database by *field* whose TIMESTAMP contains *date*."""

    #print('fs={fs}, trgt={trgt}, s={s}'.format(
    #    fs=(kwargs.get('field'), ),
    #    trgt='TIMESTAMP',
    #    s=kwargs.get('date_range')[-1],)
    #)

    top_n = []
    counter  = {}

    # results are n-tuples depending on len of fs, which is always going to
    # be 1 in this case.  "trgt='TIMESTAMP'" b/c we are filtering by date!

    results = select_fields_from(
        fs=(kwargs.get('field'), ), # expects tuple
        trgt='TIMESTAMP',
        #s=kwargs.get('date_range')[-1],
        s=kwargs.get('date'),
        part=True
    )
    #print(len(results))

    for result in results:
        name = result[0]
        if name in counter:
            counter[name] += 1 # increment
        else:
            counter[name] = 1 # add to dict

    while len(top_n) < kwargs.get('number'):
        _max = max(v for k,v in counter.items()) # Get largest value in the dict.
        k = [k for k,v in counter.items() if v is _max][0] # Find its key.
        top_n.append((k, counter.pop(k))) # Remove it from the dict and add the item to the list.

    return top_n


def n_results_by_daterange(*args, **kwargs):
    """Return a list of *n* 2-tuples of totals (field-value, total)
    filtered from the database by *field* whose TIMESTAMP is within *date(s)*."""
    # dates may be a single date, a tuple of (start, stop), or a
    # 3-tuple of (start, stop, step), or given as kwargs.

    top_n = []
    counter = {}

    date_range = kwargs.get('date_range')
    field = (kwargs.get('field'), ) # expects tuple
    number = kwargs.get('number')

    for date in yyyymmdd.daterange(*date_range): # args [start, stop]
        print('date', date)

        for result in select_fields_from(fs=field, trgt='TIMESTAMP', s=date, part=True):
            name = result[0]
            if name in counter: counter[name] += 1 # increment
            else: counter[name] = 1 # add to dict

    while len(top_n) < number:
        _max = max(v for k,v in counter.items()) # Get largest value in the dict.
        k = [k for k,v in counter.items() if v is _max][0] # Find its key.
        top_n.append((k, counter.pop(k))) # Remove it from the dict and add the item to the list.

    return top_n


def main(args):

    args = vars(args)

    if args.get('date_range'):
        results = n_results_by_daterange(**args)
    else:
        results = n_results_by_date(**args)

    #print(results)

    # write out file as: field-date-range-pivot-table.csv
    fname = '_'.join([
        '_-_'.join(args['date_range']),
        f'top-{str(args["number"])}',
        f'by-{args["field"].lower()}',
    ])

    fname += '.csv'
    fpath = '/home/ec2-user/pivot-tables/'
    fpath += fname

    #print(fpath, end='\n\n')
    for k in results:
        print(','.join(()))

    with open(fpath, mode='w') as f:
        for k in results:
            f.write(','.join((str(_) for _ in k)) + '\n')


if __name__ == '__main__':
    #main(_parse_args())

    results = n_results_by_date(
        field='COUNTRY',
        date='2017-12-13', # 09
        number=10,
        part=True,
    )

    print(results)
