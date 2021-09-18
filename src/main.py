import argparse
from sentinelsat import SentinelAPIError
from getpass import getpass
from sentsat_connector.sentinelsat_wrap import Sentinel

def parse_arguments():
    parser = argparse.ArgumentParser(description='Scihub')
    
    required = parser.add_argument_group("Required arguments")
    required.add_argument("-u", "--username", type=str,
                        help='Your scihub account username.', required=True)
    required.add_argument('-p', '--password', action='store_true', dest='password', 
                        help='Your scihub account password.', required=True)

    args = parser.parse_args()
    if args.password:
        args.password = getpass() 
    return args


if __name__=='__main__':
    args = parse_arguments()

    try:
        sentsat = Sentinel(args.username, args.password)
    
    except Exception as e:
        print(e)

