from copy import deepcopy

from models.api_calls import ApiCallList
from oas.templates import server_template, oas_template

from vars import (
    OAS_PATHS,
    OAS_RESPONSES,
    OAS_CONTENT,
    HTTP_APPLICATION_JSON,
    OAS_SCHEMA
)


class OasProcessor():
    """
    OasProcessor process data to OAS format
    """

    def __init__(self, items: ApiCallList):
        self._items = items

    def process_dict(self) -> dict:
        """
        Gets ApiCallList items and process to OAS format

        Returns:
            dict: data in OAS format
        """
        oas = deepcopy(oas_template)
        paths = oas.get(OAS_PATHS)
        for item in self._items:
            paths.setdefault(item.path, [])
            detail = {}
            for d in item.details:
                method = detail.setdefault(d.method, {})
                responses = method.setdefault(OAS_RESPONSES, [])
                status = {
                    d.status: {
                        OAS_CONTENT: {
                            HTTP_APPLICATION_JSON: {
                                OAS_SCHEMA: {}
                            }
                        }
                    }
                }
                responses.append(status)
            paths[item.path].append(detail)

        return oas
