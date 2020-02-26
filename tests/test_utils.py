from utils import build_api_call_item
from models.api_calls import ApiCallItem, ApiCallDetail


def test_build_api_call_item_returns_expected_object():
    kwargs = {
        'idx': 1,
        'host': 'host',
        'path': 'path',
        'details': [
            ('get', 200)
        ]
    }

    built_obj = build_api_call_item(**kwargs)

    details = [ApiCallDetail(method=m, status=s) for m, s in kwargs.get('details')]

    expected_obj = ApiCallItem(
        indices=(kwargs.get('idx'),),
        host=kwargs.get('host'),
        path=kwargs.get('path'),
        details=frozenset(details)
    )

    wrong_host = ApiCallItem(
        indices=(kwargs.get('idx'),),
        host='host_',   # wrong host
        path=kwargs.get('path'),
        details=frozenset(details)
    )

    wrong_path = ApiCallItem(
        indices=(kwargs.get('idx'),),
        host=kwargs.get('host'),
        path='path_',  # wrong path
        details=frozenset(details)
    )

    wrong_indices = ApiCallItem(
        indices=(2,),  # wrong indices
        host=kwargs.get('host'),
        path=kwargs.get('path'),
        details=frozenset(details)
    )

    wrong_details = ApiCallItem(
        indices=(kwargs.get('idx'),),
        host=kwargs.get('host'),
        path=kwargs.get('path'),
        details=frozenset([ApiCallDetail(method='get', status=201)])  # wrong detail
    )

    wrong_details_length = ApiCallItem(
        indices=(kwargs.get('idx'),),
        host=kwargs.get('host'),
        path=kwargs.get('path'),
        details=frozenset(
            details + [ApiCallDetail(method='get', status=201)]  # extra detail
        )
    )

    assert built_obj == expected_obj
    assert built_obj != wrong_host
    assert built_obj != wrong_path
    assert built_obj != wrong_indices
    assert built_obj != wrong_details
    assert built_obj != wrong_details_length
