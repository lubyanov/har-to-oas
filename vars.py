import os


"""
HAR fields
"""

HAR_LOG = 'log'
HAR_URL = 'url'
HAR_HEADER_NAME = 'name'
HAR_HEADER_VALUE = 'value'
HAR_HTTP_METHOD = 'method'
HAR_HTTP_STATUS = 'status'
HAR_HTTP_REQUEST = 'request'
HAR_HEADERS = 'headers'
HAR_ENTRIES = 'entries'
HAR_RESPONSE = 'response'


"""
OAS fields
"""

OAS_PATHS = 'paths'
OAS_RESPONSES = 'responses'
OAS_CONTENT = 'content'
OAS_SCHEMA = 'schema'


"""
API METHODS DETECTION fields
"""

HTTP_CONTENT_TYPE = 'content-type'
HTTP_APPLICATION_JSON = 'application/json'

API_RESPONSE_HEADERS_NAME = HTTP_CONTENT_TYPE
API_RESPONSE_HEADERS_VALUES = [HTTP_APPLICATION_JSON]


"""
READER fields
"""

HAR_TO_OAS_FILE_PATH = os.getenv('HAR_TO_OAS_FILE_PATH')


"""
WRITER fields
"""

OAS_OUTPUT_FILE_PATH = os.getenv('OAS_OUTPUT_FILE_PATH', 'output.local')
