#!/usr/bin/env python3


## From standard libraries
from os import fdopen as os_fdopen
from os import remove as os_remove
from os.path import exists as path_exists
from os.path import join as path_join
from os.path import basename, dirname
from shutil import copyfile
from tempfile import mkstemp

## From third-party libraries
from PyPDF2 import PdfFileWriter
from PyPDF2 import PdfFileReader

## From internal libraries
from inject_javascript.lib import notice, error


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


class Inject_JavaScript(object):
    """Injects some JavaScript into the PDF."""

    def __init__(self, clobber = False, escape = False, verbose = 0):
        self.clobber = clobber
        self.escape = escape
        self.verbose = verbose

    def return_pdf_data(self, pdf_path = None):
        if pdf_path is None:
            error('no "pdf_path" defined')

        ## Setup output data object and load source PDF data
        writable_pdf_data = PdfFileWriter()
        with open(pdf_path, 'rb') as fb:
            # source_pdf_data = PdfFileReader(open(pdf_path, 'rb'))
            source_pdf_data = PdfFileReader(fb)

        ## Load source PDF into output object
        for i in xrange(source_pdf_data.getNumPages()):
            writable_pdf_data.addPage(source_pdf_data.getPage(i))

        if self.verbose > 0:
            notice('finished loading data into output object from: {0}'.format(pdf_path))

        ## Return output object to calling process
        return writable_pdf_data

    def return_js_data(self, js_path = None):
        if js_path is None:
            error('no "js_path" defined')

        # Loads JavaScript file into memory
        with open(js_path, 'r') as fb:
            js_data = fb.read()

        # Add more replace lines if neaded, so far new lines have been the difficult characters
        if self.escape is True:
            js_data = js_data.replace('\\', '\\\\')
            message = 'escaped special characters prior to returning JavaScript data from: '
        else:
            message = 'finished loading JavaScript data from: '

        if self.verbose > 0:
            notice(message + js_path)

        return js_data

    def save_combined_data(self, pdf_data = None, js_data = None, pdf_path = None, save_path = None):
        ## See: https://security.openstack.org/guidelines/dg_using-temporary-files-securely.html
        ##  for where the following is inspired from
        fd, tmp_path = mkstemp()
        try:
            ## Write to a tempfile, note 'b' is there to avoid warnings during write process
            with os_fdopen(fd, 'wb') as tmp:
                pdf_data.addJS(js_data)
                pdf_data.write(tmp)

            ## Figure out where to save the temp file for the calling process
            if self.clobber is True:
                save_path = pdf_path
                copyfile(tmp_path, save_path)
                message = 'overwrote exsisting: '
            else:
                if save_path is None:
                    save_path = path_join(dirname(tmp_path), basename(pdf_path))
                copyfile(tmp_path, save_path)
                message = 'enhanced file path: '

        finally:
            ## Clean up and return saved file path or throw error messages about failures
            if path_exists(tmp_path) is True:
                os_remove(tmp_path)
            else:
                error('Unable to remove temp path: {0}'.format(tmp_path))

            if path_exists(save_path) is True:
                if self.verbose > 0:
                    notice(message + save_path)
                return save_path
            else:
                error('Unable to make save path: {0}'.format(save_path))

    def inject_pdf_with_javascript(self, pdf_path = None, js_path = None, save_path = None):
        pdf_data = self.return_pdf_data(pdf_path = pdf_path)

        js_data = self.return_js_data(js_path = js_path)

        resulting_path = self.save_combined_data(pdf_data = pdf_data,
                                                 js_data = js_data,
                                                 pdf_path = pdf_path,
                                                 save_path = save_path)

        return resulting_path


if __name__ == '__main__':
    raise Exception('Try importing `Inject_JavaScript` class from a Python script or shell instead')
