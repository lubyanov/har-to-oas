import os
import sys
import logging

from har.reader import HarReader
from har.parser import HarParser
from oas.writer import OasWriter
from oas.processor import OasProcessor


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    path = os.getenv('HAR_TO_OAS_FILE_PATH')

    data_to_parse, read_success = HarReader().read_from_file(path)

    if read_success:
        har_parser = HarParser(data_to_parse)
        api_calls = har_parser.parse()
        oas_processor = OasProcessor(api_calls)
        oas_data = oas_processor.process_dict()
        if OasWriter(oas_data).write():
            logger.info("Converting successfully done!")
        else:
            logger.error(f"Can't write result of convert!")
    else:
        logger.error(f"Can't read data from {path!r}")
