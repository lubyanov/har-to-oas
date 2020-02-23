from collections import namedtuple
from urllib.parse import urlparse
from models.api_calls import ApiCallItem, ApiCallDetail, ApiCallList
from typing import List

from vars import (
    API_RESPONSE_HEADERS_NAME, 
    API_RESPONSE_HEADERS_VALUES, 
    REQUEST,
    RESPONSE, 
    HEADERS,
    METHOD,
    STATUS,
    URL,
    NAME,
    VALUE,
    LOG,
    ENTRIES
)


class HarValidator():

    def _is_data_valid(self) -> bool:
        return True

    def _is_api_method(self, header: dict) -> bool:
        result = False
        if (header.get(NAME).lower() == API_RESPONSE_HEADERS_NAME and
            header.get(VALUE) in API_RESPONSE_HEADERS_VALUES):
            
            result = True

        return result

    def _is_entry_is_api_call(self, entry: dict) -> bool:
        result = False
        for header in entry.get(RESPONSE).get(HEADERS):
            if self._is_api_method(header):
                result = True

        return result


class HarEntryParserMixin():

    def _get_host(self, parsed_url):
        return '.'.join(parsed_url.netloc.split('.')[-2:])

    def _get_host_and_path(self, entry):
        HostPath = namedtuple('HostPath', ['host', 'path'])
        url = entry.get(REQUEST).get(URL)
        parsed_url = urlparse(url)
        host = self._get_host(parsed_url)

        return HostPath(host=host, path=parsed_url.path)

    def _get_method(self, entry):
        return entry.get(REQUEST).get(METHOD).lower()

    def _get_status(self, entry):
        return entry.get(RESPONSE).get(STATUS) 


class HarParser(HarValidator, HarEntryParserMixin):

    def __init__(self, data: dict):
        if not data:
            raise ValueError
        self._data = data

    def parse(self) -> ApiCallList:
        items = self._get_api_call_item_list()
        ac_list = self._get_api_call_list(items)

        return ac_list

    def _get_api_call_list(self, items: List[ApiCallItem]) -> ApiCallList:
        ac_list = ApiCallList()
        for item in items:
            ac_list.append(item)
        
        return ac_list

    def _get_api_call_item_list(self) -> List[ApiCallItem]:
        result = []
        if self._is_data_valid():
            entries = self._data.get(LOG).get(ENTRIES)
            for i in range(len(entries)):
                if self._is_entry_is_api_call(entries[i]):
                    host_and_path = self._get_host_and_path(entries[i])
                    detail = ApiCallDetail(
                        method=self._get_method(entries[i]),
                        status=self._get_status(entries[i])
                    )
                    api_call = ApiCallItem(
                        indices=(i,),
                        host=host_and_path.host,
                        path=host_and_path.path,
                        details=frozenset({detail})
                    )
                    result.append(api_call)
        else:
            raise ValueError

        return result