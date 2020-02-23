import json
from copy import deepcopy
from vars import PATHS, RESPONSES, CONTENT, APPLICATION_JSON, SCHEMA

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

        with open('out', 'w') as f:
            f.write(
                json.dumps(self._performed, indent=4, sort_keys=False)
            )

    def _perform_dict(self):
        oas = deepcopy(oas_template)
        paths = oas.get(PATHS)
        for item in self._items:
            paths.setdefault(item.path, [])
            for detail in item.details:
                obj = dict()
                obj \
                    .setdefault(detail.method, {}) \
                    .setdefault(RESPONSES, {}) \
                    .setdefault(detail.status, {}) \
                    .setdefault(CONTENT, {}) \
                    .setdefault(APPLICATION_JSON, {SCHEMA: {}}) 
                paths[item.path].append(obj)

        self._performed = oas

    def show(self) -> None:
        if not self._performed:
            self._perform_dict()
        print(json.dumps(self._performed, indent=4, sort_keys=False))

        