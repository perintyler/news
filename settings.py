from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# set api keys from .env file
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')

TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_SECRET_KEY = os.getenv('TWITTER_SECRET_KEY')
key_word = 'Trump'


source = 'msnbc'
#source = source_ids[0] if datetime.today().day % 2 == 0 else source_ids[1]

# Python stdlib imports
from zipfile import ZipFile, ZIP_DEFLATED, BadZipfile

# package imports
from openpyxl.shared.exc import OpenModeError, InvalidFileException
from openpyxl.shared.ooxml import ARC_SHARED_STRINGS, ARC_CORE, ARC_APP, \
        ARC_WORKBOOK, PACKAGE_WORKSHEETS, ARC_STYLE
from openpyxl.workbook import Workbook
from openpyxl.reader.strings import read_string_table
from openpyxl.reader.style import read_style_table
from openpyxl.reader.workbook import read_sheets_titles, read_named_ranges, \
        read_properties_core, get_sheet_ids
from openpyxl.reader.worksheet importread_worksheet
from openpyxl.reader.iter_worksheet import unpack_worksheet
import openpyxl

def load_subclass(filename, use_iterators = False):
    if isinstance(filename, file):
        # fileobject must have been opened with 'rb' flag
        # it is required by zipfile
        if 'b' not in filename.mode:
            raise OpenModeError("File-object must be opened in binary mode")

    try:
        archive = ZipFile(filename, 'r', ZIP_DEFLATED)
    except (BadZipfile, RuntimeError, IOError, ValueError), e:
        raise InvalidFileException(unicode(e))
    wb = Subclass()

    if use_iterators:
        wb._set_optimized_read()

    try:
        openpysx.reader.excel._load_workbook(wb, archive, filename, use_iterators)
    except KeyError, e:
        raise InvalidFileException(unicode(e))
    finally:
        archive.close()
    return wb
