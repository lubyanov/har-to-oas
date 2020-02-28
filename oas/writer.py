import json
import logging


logger = logging.getLogger(__name__)


class OasWriter():
    """
    OasWriter writes OAS data to different outputs
    """

    def __init__(self, data):
        self._data = data

    def write(self, path: str) -> bool:
        """
        Writes OAS data to json file

        Arguments:
            path (str): path to output file

        Returns:
            bool: True if everything is ok or False overwise
        """
        success = False

        try:
            with open(path, 'w') as f:
                f.write(
                    json.dumps(self._data, indent=4)
                )
                success = True
        except (IOError, OSError, ValueError) as err:
            logger.critical(f'Error cause while {path!r} writing cause: {err}')

        return success
