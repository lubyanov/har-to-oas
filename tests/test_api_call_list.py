from models.api_calls import ApiCallItem, ApiCallDetail, ApiCallList


def get_api_call_item(idx=1, host='host', path='path', details=[('get', 200)]):
    _details = [ApiCallDetail(method=m, status=s) for m, s in details]
    item = ApiCallItem(
        indices=(idx,),
        host=host,
        path=path,
        details=frozenset(_details)
    )

    return item

def set_up():
    pass    


def test_merge_is_ok():
    assert True


def test_create_from_list_is_ok():
    item1 = get_api_call_item(idx=1, details=[('get', 200)])
    item2 = get_api_call_item(idx=2, details=[('post', 201)])

    _list = ApiCallList()
    _list.create_from_list([item1, item2])

    assert len(_list) == 1

    obj = _list[0]

    assert obj.indices == (1,2)

    assert len(obj.details) == 2

    assert ApiCallDetail(method='get', status=200) in obj.details
    assert ApiCallDetail(method='post', status=201) in obj.details