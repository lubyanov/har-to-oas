import json
import logging


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
            tuple (dict, bool): HAR formatted data and status
        """
        result, success = {}, False

        try:
            with open(path) as f:
                result = json.load(f)
                success = True
        except (IOError, OSError, ValueError) as err:
            logger.critical(f'Error cause while {path!r} parsing cause: {err}')

        return (result, success)
