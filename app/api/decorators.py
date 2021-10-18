from flask import request, jsonify
from functools import wraps

from .errors import InvalidAPIUsage, InvalidFilterParams, IncorrectVideoFormat



"""
    Almost like an Architect - makes decorations
"""
def decorator_maker(func):
    def param_decorator(fn=None, does_return=None, req_c_type=None, req_type=None, arg=None, session=None):
        def deco(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                result = func(does_return, req_c_type, req_type, arg, session)
                if does_return:
                    return fn(result)
                return fn(*args, **kwargs)
            return wrapper
        if callable(fn): return deco(fn)
        return deco
    return param_decorator



"""
    Checks if user input is not out of bounds, and also Content-Type
"""
def wrap_param_check(does_return, req_c_type, req_type, arg, session):
    check_content_type(req_c_type)
    return check_correct_filter_params(session)

def check_content_type(req_c_type):
    if not request.content_type.startswith(req_c_type):
        raise InvalidAPIUsage(f'Content-Type should be of type: {req_c_type}', 400)

def check_correct_filter_params(session):
    if request.data:
        data = request.get_json()
        f_params = data['filter_params']
        if 'filter_params' not in data:
            raise InvalidFilterParams(1)
        elif 'type' not in f_params:
            raise InvalidFilterParams(1)
        if 'download' in request.url:
            if 'fps' not in data:
                raise InvalidFilterParams(1)
        if 'max_f' in f_params and 'min_f' in f_params:
            max_fr = session['video_frame_count']
            min_f_raw = f_params['min_f']
            max_f_raw = f_params['max_f']

            if min_f_raw == "": min_f_raw = 0
            if max_f_raw == "": max_f_raw = max_fr

            min_f = _check_for_req_type(int, min_f_raw, 4)
            max_f = _check_for_req_type(int, max_f_raw, 4)
            a = check_bounds(min_f_raw, max_fr)
            b = check_bounds(max_f_raw, max_fr)
            return sorted([a, b])


def _check_for_req_type(req_type, val, ex):
    try: 
        req_type(val)
    except Exception:
        raise InvalidFilterParams(ex)
    return val

parameter_check = decorator_maker(wrap_param_check)



"""
    Checks if user input is not out of bounds, and also Content-Type
"""
def wrap_url_arg_check(does_return, req_c_type, req_type, arg, session):
    check_arg_urls(req_type, arg)
    frame_idx = request.view_args[arg]
    return check_bounds(frame_idx, session['video_frame_count'])


def check_arg_urls(req_type, arg):
    try:
        req_type(request.view_args[arg])
    except ValueError:
        raise InvalidAPIUsage(f'Content-Type should be of type: {req_type.__name__}', 400)

def check_bounds(frame_idx, max_frames):
    f_max = int(max_frames)
    f_idx = int(frame_idx)
    if f_idx > f_max:
        f_idx = f_max-50
    elif f_idx < 1:
        f_idx = 1
    return f_idx

url_arg_check = decorator_maker(wrap_url_arg_check)



"""
    Checks Video Metadata
"""
def wrap_metadata_check(does_return, req_c_type, req_type, arg, session):
    check_metadata(req_type)

def check_metadata(req_type):
    byteStream = request.files['file']
    vid_type = byteStream.__dict__['headers'].get('Content-Type')
    if vid_type != req_type:
        raise IncorrectVideoFormat(1)

metadata_check = decorator_maker(wrap_metadata_check)



"""
    Excpetion Handler for non-Endpoints
"""
def exception_handler(fn=None, ex=None, type=None, pas=False):
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                fn(*args, **kwargs)
            except Exception:
                if not pas:
                    raise ex(type)
                pass
            return fn(*args, **kwargs)
        return wrapper
    if callable(fn): return deco(fn)
    return deco
