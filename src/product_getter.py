import argparse
from datetime import datetime
from getpass import getpass
from sentinelsat import UnauthorizedError
from sentsat_connector.sentinelsat_wrap import Sentinel
from argument_validation import date_range, int_range


def date_validation(begin: datetime, end: datetime):
    if begin > end:
        raise ValueError(f'Begin date is greater than end date!')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Scihub')
    
    required = parser.add_argument_group("Required arguments")
    required.add_argument("-u", "--username", type=str,
                        help='Your scihub account username.', required=True)
    required.add_argument('-p', '--password', action='store_true', dest='password', 
                        help='Your scihub account password.', required=True)
    
    optional = parser.add_argument_group("Optional arguments")
    optional.add_argument('-t', '--tiles', type=str, default='src/tiles_lit.txt',
                        help='File containing tiles. (Default: tiles_lit.txt)')
    optional.add_argument('-s', '--start', type=date_range(min=datetime(year=2016, month=1, day=1)), default=datetime.strptime('2018-06-01', '%Y-%m-%d'),
                        help='Start of sensing data. (Default: 2018-06-01)')
    optional.add_argument('-e', '--end', type=date_range(min=datetime(year=2016, month=1, day=1)), default=datetime.strptime('2018-06-30', '%Y-%m-%d'),
                        help='End of sensing data. (Default: 2018-06-30)')
    optional.add_argument('-c', '--cloud', type=int_range(min=0, max=100), default=10,
                        help='Maximum cloud cover in percent. (Default: 10)')
    optional.add_argument('-o', '--output', type=str, default='output.csv', 
                        help='Output file. (Default: output.csv)')


    args = parser.parse_args()

    date_validation(begin=args.start, end=args.end)

    if args.password:
        args.password = getpass()
        
    return args


def get_tile_list(filepath: str):
    tiles = []
    f = open(filepath, "r")
    for line in f.readlines():
        tiles.append(line.strip())
    return tiles

if __name__=='__main__':
    args = parse_arguments()

    try:
        tiles = get_tile_list(args.tiles)

        sentsat = Sentinel(args.username, args.password)
        image_data = sentsat.find_data(args.start, args.end, args.cloud, tiles)
        sentsat.to_csv(image_data, args.output)

    except UnauthorizedError as e:
        print("Failed to authorize with SentinelSat.")
    except Exception as e:
        print(e)

