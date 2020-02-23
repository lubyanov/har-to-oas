import json


class HarReader():

    # TODO: docstrins
    """
    
    """

    def read_from_file(self, path: str) -> dict:
        result = {}

        # TODO: 
        # 1. solve with & try/except case
        # 2. solve large json case

        try:
            with open(path) as f:
                result = json.load(f)
        except:
            print(f'Error cause while {path!r} parsing')

        return result