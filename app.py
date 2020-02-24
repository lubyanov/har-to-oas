import json
from har.reader import HarReader
from har.parser import HarParser
from oas.writer import OasWriter


LS_FF = 'sources.local/ls-ff.har'
AMAZON = 'sources.local/amazon.har'


if __name__ == '__main__':
    
    parser = HarParser(
        HarReader().read_from_file(LS_FF)
    )

    api_calls = parser.parse()

    OasWriter(api_calls).write()