from data.repositories.utils import list_tuple_to_dict


class ResponseTotalBaseModel:
    total: int = None

    def __init__(self, total: int):
        self.total = total


class ResponseLimitBaseModel:
    limit: int = None

    def __init__(self, limit: int):
        self.limit = limit


class ResponseDataBaseModel:
    data: list_tuple_to_dict(list, dict) = None

    def __init__(self, data: list_tuple_to_dict(list, dict)):
        self.data = data


class ResponseModel(
    ResponseTotalBaseModel, ResponseLimitBaseModel, ResponseDataBaseModel
):
    def __init__(self, total: int, limit: int, data: list_tuple_to_dict(list, dict)):
        ResponseTotalBaseModel.__init__(self, total)
        ResponseLimitBaseModel.__init__(self, limit)
        ResponseDataBaseModel.__init__(self, data)
