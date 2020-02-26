from har.reader import HarReader
from har.parser import HarParser
from oas.writer import OasWriter
from oas.processor import OasProcessor


LS_FF = 'sources.local/ls-ff.har'
AMAZON = 'sources.local/amazon.har'


if __name__ == '__main__':

    har_parser = HarParser(
        HarReader().read_from_file(LS_FF)
    )

    api_calls = har_parser.parse()

    oas_processor = OasProcessor(api_calls)

    oas_data = oas_processor.process_dict()

    OasWriter(oas_data).write()
