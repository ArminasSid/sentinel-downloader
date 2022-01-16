import argparse
from getpass import getpass
from sentinelsat import UnauthorizedError
from sentsat_connector.sentinelsat_wrap import Sentinel
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description='Scihub')
    
    required = parser.add_argument_group("Required arguments")
    required.add_argument("-u", "--username", type=str,
                        help='Your scihub account username.', required=True)
    required.add_argument('-p', '--password', action='store_true', dest='password', 
                        help='Your scihub account password.', required=True)
    
    optional = parser.add_argument_group("Optional arguments")
    optional.add_argument('-i', '--input', type=str, default='data.csv', 
                        help='Input file. (Default: data.csv')
    optional.add_argument('-o', '--output', type=str, default='images', 
                        help='Output folder. (Default: images)')


    args = parser.parse_args()
    if args.password:
        args.password = getpass()
        
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    return args


if __name__ == '__main__':
    args = parse_arguments()

    try:
        sentsat = Sentinel(args.username, args.password)
        sentsat.download(sentsat.read_csv(args.input), args.input, args.output)


    except UnauthorizedError as e:
        print("Failed to authorize with SentinelSat.")