import json
import logging
from typing import NoReturn
from vars import OUTPUT


logger = logging.getLogger(__name__)


class OasWriter():
    """
    OasWriter writes OAS data to different outputs
    """

    def __init__(self, data):
        self._data = data

    def write(self) -> NoReturn:
        """ Writes OAS data to json file """

        try:
            with open(OUTPUT, 'w') as f:
                f.write(
                    json.dumps(self._data, indent=4)
                )
        except:
            logger.critical(f'Error cause while {OUTPUT!r} writing')
