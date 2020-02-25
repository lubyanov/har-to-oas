from models.api_calls import ApiCallItem, ApiCallDetail, ApiCallList
from utils import build_api_call_item


def test_merge_is_ok():
    assert True


def test_create_from_list_is_ok():

    _list = ApiCallList().create_from_list([]) # returns also empty collection
    
    assert len(_list) == 0

    # items with a same url (host+path), but different details and indices
    item1 = build_api_call_item(idx=1, details=[('get', 200)], host='host', path='path')
    item2 = build_api_call_item(idx=2, details=[('post', 201)], host='host', path='path')

    _list = ApiCallList().create_from_list([item1, item2]) # returns one object with merged details

    assert len(_list) == 1
    assert len(_list) != 2
    assert len(_list[0].details) == 2
    assert len(_list[0].indices) == 2

    # items with a different urls (host+path)
    item1 = build_api_call_item(idx=1, details=[('get', 200)], host='host1', path='path')
    item2 = build_api_call_item(idx=2, details=[('get', 200)], host='host2', path='path')

    _list = ApiCallList().create_from_list([item1, item2]) # returns two objects

    assert len(_list) == 2
    assert len(_list) != 1

    # two items with a same url (host+path), but different details and indices 
    # and one with with different url
    item1 = build_api_call_item(idx=1, details=[('get', 200)], host='host', path='path')
    item2 = build_api_call_item(idx=2, details=[('post', 201)], host='host', path='path')
    item3 = build_api_call_item(idx=3, details=[('get', 200)], host='host_', path='path')

    _list = ApiCallList().create_from_list([item1, item2, item3]) # returns two objects

    assert len(_list) == 2
    assert len(_list) != 1
    assert len(_list) != 3