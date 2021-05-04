from django.http import JsonResponse


class HttpCode():
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500


def result(code = HttpCode.ok, message = "", data = None, kwargs = None):
    json_dict = {'code': code, "message": message, "data": data}
    # 判断kwargs时候存在，如果kwargs存在且为字典类型，并且其关键字也存在，就可以将kwargs更新进入jsnon_data
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)


def ok():
    return result()


def paramserror(message="", data=None):
    return result(code=HttpCode.paramserror,message=message, data=data)


def unauth(message="", data=None):
    return result(code = HttpCode.unauth, message = message, data = data)


def servererror(message="", data=None):
    return result(code=HttpCode.servererror, message=message, data=data)