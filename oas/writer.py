import json
from copy import deepcopy
from vars import PATHS, RESPONSES, CONTENT, APPLICATION_JSON, SCHEMA, OUTPUT


server_template = {
    'url': '',
    'description': ''
}

oas_template = {
    'openapi': '3.0.2',
    'info': {
        'title': '',
        'description': '',
        'version': ''
    },
    'servers': [],
    'paths': {}
}


class OasWriter():

    def __init__(self, items):
        self._items = items
        self._performed = None

    def write(self) -> None:
        if not self._performed:
            self._perform_dict()

        with open(OUTPUT, 'w') as f:
            f.write(
                json.dumps(self._performed, indent=4, sort_keys=False)
            )

    def _perform_dict(self):
        oas = deepcopy(oas_template)
        paths = oas.get(PATHS)
        for item in self._items:
            paths.setdefault(item.path, [])
            detail = {}
            for d in item.details:
                method = detail.setdefault(d.method, {})
                responses = method.setdefault(RESPONSES, [])
                status = {
                    d.status: {
                        CONTENT: {
                            APPLICATION_JSON: {
                                SCHEMA: {}
                            }
                        }
                    }
                }
                responses.append(status)
            paths[item.path].append(detail)

        self._performed = oas