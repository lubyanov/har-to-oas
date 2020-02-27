from __future__ import annotations
from typing import Tuple, Set, List, NoReturn
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
    """
    Collections of ApiCallItem

    Allows to store objects with same key (host + path), but different details
    (as HTTP method and status represented in ApiCallDetail) object and allows
    to merge same objects into one appending details

    Attributes:
        _items (list): stores ApiCallItem
        _indices (dict): pairs of ApiCallItem key and it's index in _items
    """

    _items = []
    _indices = {}

    def __getitem__(self, i):
        return self._items[i]

    def __len__(self):
        return len(self._items)

    def _reset_stores(self):
        """ Clear data in stores """
        del self._items[:]
        self._indices.clear()

    def _merge(self, x: ApiCallItem, y: ApiCallItem) -> ApiCallItem:
        """
        Merges two objects with same url to one and with all ApiCallDetail

        Method gets two objects with same url and join object's indices into
        one tuple and join different ApiCallDetail (different method, status)
        without duplicates

        Args:
            x: ApiCallItem - object to merge
            y: ApiCallItem - another object to merge

        Raises:
            TypeError: raises if args are not ApiCallItem instances
            ValueError: raises if objects has different urls

        Returns:
            ApiCallItem: merged object with same url and all details
        """
        if not isinstance(x, ApiCallItem) or not isinstance(y, ApiCallItem):
            raise TypeError('Method accepts only ApiCallItem objects')

        if x.host + x.path != y.host + y.path:
            raise ValueError('Object\'s urls aren\'t identical')

        return ApiCallItem(
            indices=x.indices + y.indices,
            host=x.host,
            path=x.path,
            details=x.details | y.details
        )

    def create_from_list(self, items: List[ApiCallItem]) -> ApiCallList:
        """
        Create collection from given items

        Methods reset stores if they are exist and append
        items into collection according 'append' logic

        Args:
            items: List[ApiCallItem] - list of separate ApiCallItems

        Returns:
            ApiCallList: return self as a result
        """
        self._reset_stores()
        for item in items:
            self.append(item)

        return self

    def append(self, item: ApiCallItem) -> NoReturn:
        """
        Appends item to collection

        Method checks if there's other object with the same url
        exists in collection and depends on it merge objects and
        append to collection or just append to collection

        Args:
            item: ApiCallItem - item to append collection

        Raises:
            TypeError: raises if item if not ApiCallItem instnance

        Returns:
            None
        """
        if isinstance(item, ApiCallItem):
            key = item.host + item.path
            if key in self._indices:
                stored = self._items[self._indices[key]]
                self._items[self._indices[key]] = self._merge(stored, item)
            else:
                self._items.append(item)
                self._indices[key] = len(self._items) - 1
        else:
            raise TypeError('ApiCallItem must be passed')
