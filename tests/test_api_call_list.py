from pytest import raises
from models.api_calls import ApiCallItem, ApiCallDetail, ApiCallList
from utils import build_api_call_item


def test_merge_is_works():
    sequence = ApiCallList()

    # items with a same url (host+path), but different details and indices
    item1 = build_api_call_item(idx=1, details=[('get', 200)], host='host', path='path')
    item2 = build_api_call_item(idx=2, details=[('post', 201)], host='host', path='path')

    merged_obj = sequence._merge(item1, item2)
    expected_obj = ApiCallItem(
        indices=(1,2),
        host='host',
        path='path',
        details=frozenset({
            ApiCallDetail(method='get', status=200),
            ApiCallDetail(method='post', status=201)
        })
    )

    assert merged_obj == expected_obj
    assert merged_obj != item1
    assert merged_obj != item2

    # items with a same url (host+path) and details, but different indices
    item1 = build_api_call_item(idx=1, details=[('get', 200)], host='host', path='path')
    item2 = build_api_call_item(idx=2, details=[('get', 200)], host='host', path='path')

    merged_obj = sequence._merge(item1, item2)
    expected_obj = ApiCallItem(
        indices=(1,2),
        host='host',
        path='path',
        details=frozenset({
            ApiCallDetail(method='get', status=200)
        })
    )

    assert merged_obj == expected_obj
    assert merged_obj != item1
    assert merged_obj != item2


def test_merge_is_raises_type_exception():
    sequence = ApiCallList()
    item = build_api_call_item(idx=1, details=[('get', 200)], host='host', path='path')

    with raises(TypeError):
        sequence._merge(None, None)

    with raises(TypeError):
        sequence._merge(item, None)

    with raises(TypeError):
        sequence._merge(None, item)

    sequence._merge(item, item)


def test_merge_is_raises_value_exception():
    sequence = ApiCallList()

    item1 = build_api_call_item(idx=1, details=[('get', 200)], host='host', path='path') # original
    item2 = build_api_call_item(idx=2, details=[('get', 200)], host='host_', path='path') # different host
    item3 = build_api_call_item(idx=2, details=[('get', 200)], host='host', path='path_') # different path
    item4 = build_api_call_item(idx=2, details=[('get', 200)], host='host_', path='path_') # different both

    with raises(ValueError):
        sequence._merge(item1, item2)

    with raises(ValueError):
        sequence._merge(item1, item3)

    with raises(ValueError):
        sequence._merge(item1, item4)

    sequence._merge(item1, item1)


def test_append_is_works():
    pass


def test_create_from_list_is_works():

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

    # all items with a same url (host+path), but all with different details and indices
    item1 = build_api_call_item(idx=1, details=[('get', 200)], host='host', path='path')
    item2 = build_api_call_item(idx=2, details=[('post', 201)], host='host', path='path')
    item3 = build_api_call_item(idx=3, details=[('get', 304)], host='host', path='path')

    _list = ApiCallList().create_from_list([item1, item2, item3]) # returns one object

    assert len(_list) == 1
    assert len(_list) != 2
    assert len(_list) != 3