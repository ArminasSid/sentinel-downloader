import argparse
from datetime import datetime


def int_range(min, max):
    """Returns a function handle of argument 'type' for argsparse"""

    def integer_range_checker(arg):
        try:
            # Check if argument is integer
            value = int(arg)
        except ValueError:
            raise argparse.ArgumentTypeError('must be an integer value!')

        if max < value or min > value:
            raise argparse.ArgumentTypeError(f'must be in range [{str(min)}:{str(max)}]')

        return value
    # Return function handle to checking function
    return integer_range_checker


def date_range(min: datetime, max: datetime = None):
    """Returns a function handle of argument 'type' for argsparse"""
    
    def datetime_range_checker(arg):
        try:
            # Check if argument is valid datetime
            value = datetime.strptime(arg, '%Y-%m-%d')
        except ValueError:
            raise argparse.ArgumentTypeError('must be an datetime value!')

        if min > value:
            raise argparse.ArgumentTypeError(f'must be in greater than {str(min)}')
        
        if max != None and max < value:
            raise argparse.ArgumentTypeError(f'must be in less than {str(max)}')
        return value
    return datetime_range_checker


