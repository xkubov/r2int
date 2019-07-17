#!/usr/bin/env python3

import argparse
import os
import shutil
import sys

import r2pipe

def print_error_and_die(*msg):
    print('Error:', *msg)
    sys.exit(1)


def parse_args(args):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        help='The input file.')

    parser.add_argument('-o', '--output',
                        dest='output',
                        metavar='FILE',
                        help='Output file (default: file.c). All but the last component must exist.')

    parser.add_argument('-s', '--select',
                        dest='selected_addr',
                        help='Decompile only the function selected by the given address (any address inside function). Examples: 0x1000, 4096.')

    return parser.parse_args(args)


def check_args(args):
    if not args.file or not os.path.exists(args.file):
        print_error_and_die('Specified input file does not exist:', args.file)
    args.file_dir = os.path.dirname(args.file)

    if not args.output:
        args.output = args.file + '.c'

    args.output_dir = os.path.dirname(args.output)
    if not os.path.exists(args.output_dir):
        print_error_and_die('Output directory does not exist:', args.output_dir)


def main():
    args = parse_args(sys.argv[1:])
    check_args(args)

    if args.file_dir != args.output_dir:
        shutil.copy(args.file, args.output_dir)
#        args.file = os.path.join(args.output_dir, os.path.basename(args.file))

    r2 = r2pipe.open(args.file)
    r2.cmd('aaa')

    if args.selected_addr:
        r2.cmd('s ' + args.selected_addr)

    else:
        r2.cmd('s sym.main')
        r2.cmd('s main')

    out = r2.cmd('#!pipe r2retdec -p')

    r2.quit()

    with open(args.output, "w") as f:
        f.write(out)

    return 0


if __name__ == "__main__":
    main()
