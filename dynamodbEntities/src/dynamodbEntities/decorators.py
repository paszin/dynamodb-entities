
import functools


def add_convert_param(lookup, keyword="convert"):
    """
    extend the parameters with a kewword paramater "convert",
    when set to True, the response will be converted to the Entity class
    Important: your function must have **kwargs as the last parameter
    """

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            resp = func(*args, **kwargs)
            singleItem = bool(resp.get("Item", False))
            if kwargs.get(keyword):
                et_name = lookup.values()[0].__et_name
                newResp = [lookup[item[et_name]](
                    **item) for item in resp.get("Items", [resp.get("Item")])]
                return newResp[0] if singleItem else newResp
            return resp
        return wrapper
    return actual_decorator
