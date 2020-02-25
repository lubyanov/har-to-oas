from __future__ import annotations
from typing import Tuple, Set, List, NoReturn
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
        self._create_data_containers()

    def __getitem__(self, i):
        if not self._sequence:
            self._set_sequence()

        return self._sequence[i] 

    def __len__(self):
        return len(self._sequence)

    def _create_data_containers(self) -> NoReturn:
        self._sequence = []
        self._data = OrderedDict()

    def _set_sequence(self) -> NoReturn:
        self._sequence = [self._data.get(k) for k in self._data]

    def _merge(self, x: ApiCallItem, y: ApiCallItem) -> ApiCallItem:
        details = set(x.details)
        details.update(y.details) 

        item = ApiCallItem(
            indices=x.indices + y.indices,
            host=x.host,
            path=x.path,
            details=frozenset(details)
        )

        return item

    def create_from_list(self, items: List[ApiCallItem]) -> ApiCallList:
        self._create_data_containers()
        for item in items:
            self.append(item)

        return self

    def append(self, item: ApiCallItem) -> NoReturn:
        if isinstance(item, ApiCallItem):
            key = item.host + item.path
            if key in self._data:
                self._data[key] = self._merge(self._data[key], item)
            else:
                self._data[key] = item
            self._set_sequence()
        else:
            raise TypeError("ApiCallItem must be passed")