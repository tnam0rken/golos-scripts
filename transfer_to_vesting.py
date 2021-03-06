#!/usr/bin/env python

import sys
import json
import argparse
import logging
import yaml
import traceback
from golos import Steem

log = logging.getLogger(__name__)

def main():

    parser = argparse.ArgumentParser(
            description='transfer GOLOS to GOLOS POWER',
            epilog='Report bugs to: https://github.com/bitfag/golos-scripts/issues')
    parser.add_argument('-d', '--debug', action='store_true',
        help='enable debug output'),
    parser.add_argument('--broadcast', action='store_true', default=False,
            help='broadcast transactions'),
    parser.add_argument('-c', '--config', default='./common.yml',
            help='specify custom path for config file')
    parser.add_argument('f',
            help='from'),
    parser.add_argument('to',
            help='to'),
    parser.add_argument('amount',
            help='amount'),
    args = parser.parse_args()

    # create logger
    if args.debug == True:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    # parse config
    with open(args.config, 'r') as ymlfile:
        conf = yaml.load(ymlfile)


    # initialize steem instance
    log.debug('broadcast: %s', args.broadcast)
    # toggle args.broadcast
    b = not args.broadcast
    golos = Steem(nodes=conf['nodes_old'], no_broadcast=b, keys=conf['keys'])

    golos.transfer_to_vesting(args.amount, to=args.to, account=args.f)

if __name__ == '__main__':
    main()
