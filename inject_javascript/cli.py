#!/usr/bin/env python3


from argparse import ArgumentParser
from os.path import basename
from sys import argv
from time import sleep

from inject_javascript.lib import Inject_JavaScript
from watch_path import Watch_Path


__license__ = """
Inject JavaScript within PDF document body
Copyright (C) 2020 S0AndS0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


def js_updated_callback(**kwargs):
    """
    Function called by `Watch_File` when JavaScript modified time changes
    """
    # time_stamp = kwargs['time_stamp']
    return kwargs['injector'].inject_pdf_with_javascript(pdf_path = kwargs['pdf_path'],
                                                         js_path = kwargs['file_path'],
                                                         save_path = kwargs['save_path'])


arg_parser = ArgumentParser(
    prog = basename(argv[0]),
    usage = '%(prog)s --pdf "/tmp/boring.pdf" --js "/dir/script.js"',
    epilog = 'For more projects see: https://github.com/S0AndS0')

arg_parser.add_argument('--pdf-path', '--pdf',
                        help = 'Out path to save PDF',
                        required = True)

arg_parser.add_argument('--js-path', '--js',
                        help = 'JavaScript to inject into downloaded PDF',
                        required = True)

arg_parser.add_argument('--save-path',
                        help = 'Optional path to save enhanced PDF to, ignored if clobber is True',
                        required = True)

arg_parser.add_argument('--escape',
                        help = 'Prevent replacing/escaping of specific character combos',
                        action = 'store_true',
                        default = False)

arg_parser.add_argument('--clobber',
                        help = 'Overwrite preexisting/input PDF',
                        action = 'store_true',
                        default = False)

arg_parser.add_argument('--watch',
                        help = 'Watch JavaScript file for changes',
                        action = 'store_true',
                        default = False)

arg_parser.add_argument('--verbose', '-v',
                        help = 'Loudness of this script',
                        action = 'count')

verbose = arg_parser.parse_known_args()[0].verbose
args = vars(arg_parser.parse_args())


def main():
    injector = Inject_JavaScript(clobber = args.get('clobber'),
                                 escape = args.get('escape'),
                                 verbose = verbose)

    injected = injector.inject_pdf_with_javascript(pdf_path = args.get('pdf_path'),
                                                   js_path = args.get('js_path'),
                                                   save_path = args.get('save_path'))

    if verbose > 0:
        print('Enhanced file maybe found at: {0}'.format(injected))

    if args.get('watch') is True:
        path_watcher = Watch_Path(file_path = args.get('js_path'),
                                  callback = js_updated_callback,
                                  injector = injector,
                                  pdf_path = args.get('pdf_path'),
                                  save_path = args.get('save_path'))

        for callback_results in path_watcher:
            if verbose > 0:
                print("Updated file enhancments at: {}".format(callback_results))
            sleep(1)
