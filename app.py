import os
from har.reader import HarReader
from har.parser import HarParser
from oas.writer import OasWriter
from oas.processor import OasProcessor


if __name__ == '__main__':

    har_parser = HarParser(
        HarReader().read_from_file(os.getenv('HAR_TO_OAS_FILE_PATH'))
    )

    api_calls = har_parser.parse()

    oas_processor = OasProcessor(api_calls)

    oas_data = oas_processor.process_dict()

    OasWriter(oas_data).write()
