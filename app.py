import sys
import logging

from har.reader import HarReader
from har.parser import HarParser
from oas.writer import OasWriter
from oas.processor import OasProcessor

from vars import HAR_TO_OAS_FILE_PATH


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    if not HAR_TO_OAS_FILE_PATH:
        logger.error(f"Variable 'HAR_TO_OAS_FILE_PATH' must be set")
        exit(1)

    data_to_parse, read_success = HarReader().read_from_file(HAR_TO_OAS_FILE_PATH)

    if not read_success:
        logger.error(f"Can't read data from {HAR_TO_OAS_FILE_PATH!r}")
        exit(1)

    har_parser = HarParser(data_to_parse)
    api_calls = har_parser.parse()
    oas_processor = OasProcessor(api_calls)
    oas_data = oas_processor.process_dict()

    write_success = OasWriter(oas_data).write()

    if not write_success:
        logger.error(f"Can't write result of convert")
        exit(1)

    logger.info("Converting successfully done")
    exit(0)