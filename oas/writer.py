import json
import logging

from vars import OAS_OUTPUT_FILE_PATH


logger = logging.getLogger(__name__)


class OasWriter():
    """
    OasWriter writes OAS data to different outputs
    """

    def __init__(self, data):
        self._data = data

    def write(self) -> bool:
        """
        Writes OAS data to json file

        Returns:
            bool: True if everything is ok or False overwise
        """
        success = False

        try:
            with open(OAS_OUTPUT_FILE_PATH, 'w') as f:
                f.write(
                    json.dumps(self._data, indent=4)
                )
                success = True
        except (IOError, OSError, ValueError) as err:
            logger.critical(f'Error cause while {OAS_OUTPUT_FILE_PATH!r} writing cause: {err}')

        return success
