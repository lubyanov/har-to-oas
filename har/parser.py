from typing import List, Mapping
from collections import namedtuple
from urllib.parse import urlparse

from models.api_calls import ApiCallItem, ApiCallDetail, ApiCallList

from vars import (
    API_RESPONSE_HEADERS_NAME,
    API_RESPONSE_HEADERS_VALUES,
    HAR_HTTP_REQUEST,
    HAR_RESPONSE,
    HAR_HEADERS,
    HAR_HTTP_METHOD,
    HAR_HTTP_STATUS,
    HAR_URL,
    HAR_HEADER_NAME,
    HAR_HEADER_VALUE,
    HAR_LOG,
    HAR_ENTRIES
)


HostPath = namedtuple('HostPath', ['host', 'path'])


class HarValidator():
    """
    HarValidator helps to validate HAR entry format
    """

    def _is_data_valid(self) -> bool:
        """
        Method validates that data is a valid HAR format dict

        Validation uses json schema validation and as a result guarantee
        that dict fits expected structure and has all necessary fields

        Returns:
            True if data is valid or False if it's not
        """
        # TODO: implement validation

        return True


class HarEntryChecker():
    """
    Checks different HAR entries on belongings to API calls
    """

    def _is_api_method(self, header: Mapping[str, str]) -> bool:
        """
        Checks is HTTP request looks like an API call

        Args:
            header: Mapping[str, str] - HTTP header name and it's value

        Returns:
            True if request is API call or False if it's not
        """
        return (
            header.get(HAR_HEADER_NAME).lower() == API_RESPONSE_HEADERS_NAME
            and header.get(HAR_HEADER_VALUE) in API_RESPONSE_HEADERS_VALUES
        )

    def _is_entry_is_api_call(self, entry: dict) -> bool:
        """
        Checks is given entry looks like API call

        Args:
            entry: dict - HAR format entry

        Returns:
            True if method is API call or False if it's not
        """
        result = False
        for header in entry.get(HAR_RESPONSE).get(HAR_HEADERS):
            if self._is_api_method(header):
                result = True

        return result


class HarEntryParserMixin():
    """
    HarEntryParserMixin helps to parse HAR entry
    """

    def _get_host(self, parsed_url: str) -> str:
        """ Parses url string to get host """
        return '.'.join(parsed_url.netloc.split('.')[-2:])

    def _get_host_and_path(self, entry: dict):
        url = entry.get(HAR_HTTP_REQUEST).get(HAR_URL)
        parsed_url = urlparse(url)
        host = self._get_host(parsed_url)

        return HostPath(host=host, path=parsed_url.path)

    def _get_method(self, entry: dict) -> str:
        """
        Gets http method from given dict

        Assumes that entry already validated

        Args:
            entry: dict - HAR format entry

        Returns:
            str: http method
        """
        return entry.get(HAR_HTTP_REQUEST, {}).get(HAR_HTTP_METHOD, '').lower()

    def _get_status(self, entry: dict) -> str:
        """
        Gets http status from given dict

        Assumes that entry already validated

        Args:
            entry: dict - HAR format entry

        Returns:
            str: http status
        """
        return entry.get(HAR_RESPONSE, {}).get(HAR_HTTP_STATUS, '')


class HarParser(HarValidator, HarEntryChecker, HarEntryParserMixin):
    """
    HarParser class helps to convert data to special ApiCallList object

    Class gets dictionary represented in HAR format to convert to special
    data-transfer object, which has better structure to next processing
    """

    def __init__(self, data: dict):
        """
        Initializes object with HAR data

        Args:
            data: dictionary object with HAR data

        Raises:
            ValueError: raises if data is empty or not dict object
        """
        if not data or not isinstance(data, dict):
            raise ValueError('Data to parse is empty or not dict')
        self._data = data

    def parse(self) -> ApiCallList:
        """
        Parses inner HAR data to ApiCallList data structure

        Returns:
            ApiCallList - collection of HAR items
        """
        items = self._get_api_call_item_list()

        return ApiCallList().create_from_list(items)

    def _get_api_call_item_from_entry(self, idx: int, entry: dict) -> ApiCallItem:
        if entry and isinstance(entry, dict):
            host_and_path = self._get_host_and_path(entry)
            detail = ApiCallDetail(
                method=self._get_method(entry),
                status=self._get_status(entry)
            )
            api_call = ApiCallItem(
                indices=(idx,),
                host=host_and_path.host,
                path=host_and_path.path,
                details=frozenset({detail})
            )
        else:
            raise ValueError('Entry to parse is emtpy or not dict')

        return api_call

    def _get_api_call_item_list(self) -> List[ApiCallItem]:
        """
        Gets HAR entries and convert to list of separate ApiCallItem collection

        Raises:
            ValueError - raises if data is not valid HAR data

        Returns:
            list: - list of separate ApiCallItem
        """
        if not self._is_data_valid():
            raise ValueError('Invalid HAR format')

        result = []
        entries = self._data.get(HAR_LOG).get(HAR_ENTRIES)
        for idx, entry in enumerate(entries):
            if self._is_entry_is_api_call(entry):
                result.append(
                    self._get_api_call_item_from_entry(idx, entry)
                )
            

        return result
