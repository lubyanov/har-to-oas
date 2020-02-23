from typing import Tuple, Set
from collections import OrderedDict
from dataclasses import dataclass


@dataclass(frozen=True)
class ApiCallDetail():
    method: str
    status: int


@dataclass(frozen=True)
class ApiCallItem():
    indices: Tuple[int]
    host: str
    path: str
    details: Set[ApiCallDetail]


class ApiCallList():

    def __init__(self):
        self._sequence = []
        self._data = OrderedDict()

    def __getitem__(self, i):
        if not self._sequence:
            self._set_sequence()

        return self._sequence[i] 

    def _set_sequence(self):
        self._sequence = [ self._data.get(k) for k in self._data ]

    def _merge(self, x: ApiCallItem, y: ApiCallItem) -> ApiCallItem:
        details = set(x.details)
        details.update(y.details) 

        return ApiCallItem(
            indices=x.indices + y.indices,
            host=x.host,
            path=x.path,
            details=frozenset(details)
        )

    def append(self, item: ApiCallItem) -> None:
        if isinstance(item, ApiCallItem):
            key = item.host + item.path
            if key in self._data:
                self._data[key] = self._merge(self._data[key], item)
            else:
                self._data[key] = item
            self._set_sequence()
        else:
            raise TypeError("ApiCallItem must be passed")