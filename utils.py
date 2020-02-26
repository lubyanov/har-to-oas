from typing import List, Tuple
from models.api_calls import ApiCallDetail, ApiCallItem


def build_api_call_item(idx: int, host: str, path: str,
                        details: List[Tuple[str, int]]) -> ApiCallItem:

    return ApiCallItem(
        indices=(idx,),
        host=host,
        path=path,
        details=frozenset(
            [ApiCallDetail(method=m, status=s) for m, s in details]
        )
    )
