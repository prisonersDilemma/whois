#!/usr/bin/env python3.6
__doc__ = """\
At least a temporary solution for making queries on the database.
"""
__date__ = '2017-12-12'
__version__ = (0,0,1)

from argparse import ArgumentParser

#from database import select_fields_from
from .database import select_fields_from
from yyyymmdd import daterange, FungableDate, yyyymmdd


query_parser = ArgumentParser(prog='query',
    description='Query the database.')


def _parse_args(args=None):

    query_parser.add_argument('--field', '-f', type=str,
        help='database field to target')

    query_parser.add_argument('--number', '-n', type=int, metavar='N', default=10,
        help='number of top results to filter')

    # default has to be today + 1
    query_parser.add_argument('--date-range', '-r', metavar='YYYY-MM-DD',
        action='append', nargs='?',
        help='date(s) to filter database records by, given in YYYY-MM-DD format')

    args = query_parser.parse_args() if args is None else query_parser.parse_args(args)

    if args.date_range is None:
        d = FungableDate()
        d.day += 1
        args.date_range = [yyyymmdd(year=d.year, month=d.month, day=d.day)]

    return args


def n_results_by_date(field, date, n=10, part=False):
    """Return a list of *n* 2-tuples of totals (field-value, total)
    filtered from the database by *field* whose TIMESTAMP contains *date*.
    """
    counter  = {}

    # results are n-tuples depending on len of fs, which is always going to
    # be 1 in this case.  "trgt='TIMESTAMP'" b/c we are filtering by date!
    for result in select_fields_from(fs=(field,), trgt='TIMESTAMP', s=date, part=part):
    #                                ^^ fs expects tuple
        name = result[0]
        if name in counter:
            counter[name] += 1 # increment
        else:
            counter[name] = 1 # add to dict

    top_n = []
    while len(top_n) < n:
        # Get largest value in the dict.
        _max = max(v for k,v in counter.items())
        # Find its key.
        k = [k for k,v in counter.items() if v is _max][0]
        # Remove it from the dict and add the item to the list.
        top_n.append((k, counter.pop(k)))
        # Repeat.

    return top_n


def n_results_by_daterange(*args, **kwargs):
    """Return a list of *n* 2-tuples of totals (field-value, total)
    filtered from the database by *field* whose TIMESTAMP is within *date(s)*.
    """
    # dates may be a single date, a tuple of (start, stop), or a
    # 3-tuple of (start, stop, step), or given as kwargs.

    #print(args)
    #print(kwargs)
    #return

    n = kwargs.pop('number') if kwargs.get('number') else 10
    field = kwargs.pop('field') if kwargs.get('field') else 'ASN'
    part = kwargs.pop('part') if kwargs.get('part') else False

    top_n = []
    counter = {}

    #print(*args)
    #print(*kwargs)
    #return

    for date in daterange(*args, **kwargs): # kwargs: start, stop, step
        print('date', date)
        for result in select_fields_from(fs=(field,), trgt='TIMESTAMP',
                                         s=date, part=part):
            name = result[0]
            if name in counter:
                counter[name] += 1 # increment
            else:
                counter[name] = 1 # add to dict

    while len(top_n) < n:
        # Get largest value in the dict.
        _max = max(v for k,v in counter.items())
        # Find its key.
        k = [k for k,v in counter.items() if v is _max][0]
        # Remove it from the dict and add the item to the list.
        top_n.append((k, counter.pop(k)))
        # Repeat.

    return top_n


def main(args=None):
    args = _parse_args() if args is None else _parse_args(args)
    #print(args)
    kwargs = vars(args)
    args = kwargs.pop('date_range')
    n_results_by_daterange(*args, **kwargs)


if __name__ == '__main__':
    main(_parse_args())



    #results = n_results_by_date(
    #    field='COUNTRY',
    #    date='2017-12-09',
    #    n=10,
    #    part=True,
    #)

    #results = n_results_by_daterange(
    #    '2017-12-09',
    #    '2017-12-10',
    #    #start='2017-12-09',
    #    #stop='2017-12-10',
    #    field='COUNTRY',
    #    n=10,
    #    part=True,
    #)
    #print(results)
