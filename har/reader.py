import sys
import json
import logging


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class HarReader():
    """
    HarReader gets HAR data from different sources
    """

    def read_from_file(self, path: str) -> dict:
        """
        Reads data from json file

        Args:
            path: str - path to json file

        Returns:
            dict: HAR formatted data
        """
        result = {}
        try:
            with open(path) as f:
                result = json.load(f)
        except:
            logger.critical(f'Error cause while {path!r} parsing')

        return result