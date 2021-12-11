import asyncio
import functools
import json
import os
import warnings
from collections import namedtuple
from urllib.parse import urlparse, unquote, parse_qs

import requests
from logzero import logger as log
# from redis import UnixDomainSocketConnection
# from redis._compat import iteritems
# from redis.connection import URL_QUERY_ARGUMENT_PARSERS

def to_int(s, _default=0):
    try:
        return int(s)
    except Exception as e:
        return _default


def get_path(d, key_path, default_val=None):
    paths = key_path.split('.')
    try:
        for k in paths:
            if isinstance(d, list) and to_int(k, -1) >= 0:
                d = d[to_int(k)]
            else:
                d = d[k]

        return d
    except KeyError:
        return default_val
    except TypeError:
        return default_val


def singleton(a_class):
    def on_call(*args, **kwargs):
        if on_call.instance is None:
            on_call.instance = a_class(*args, **kwargs)
        return on_call.instance

    on_call.instance = None
    return on_call


async def async_exec(f):
    return await asyncio.get_running_loop().run_in_executor(None, f)


def run_in_executor(f):
    return asyncio.get_running_loop().run_in_executor(None, f)


def convert_dict_to_json(data: dict):
    return namedtuple(
        "X", data.keys()
    )(*tuple(map(lambda x: x if not isinstance(x, dict) else convert_dict_to_json(x), data.values())))


def safe_capture_error(e):
    try:
        log.debug('Sentry captured exception: ')
        log.debug(e)
    except Exception as e:
        log.debug('Sentry cannot capture exception: ')
        log.exception(e)


def parse_raw_data_to_obj(data):
    convert_data = {}
    try:
        convert_data = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    except:
        try:
            convert_data = json.loads(data)
            if 'header' in convert_data['message']: del convert_data['message']['header']
            convert_data = convert_dict_to_json(convert_data)
        except Exception as e:
            safe_capture_error(e)
    return convert_data


async def async_request(**kwargs):
    r = await asyncio.get_event_loop().run_in_executor(None, functools.partial(requests.request, **kwargs))
    return r.json()


def without_keys(d, keys):
    return {k: v for k, v in d.items() if k not in keys}


def batch(arr, n):
    i = 0
    while i < len(arr):
        yield arr[i:i + n]
        i += n


def find_file_in_dir(file_name: str, try_count: int, dir_path):
    count = 0
    if count > try_count: return False
    entries = os.listdir(dir_path)
    if not file_name in entries:
        result = find_file_in_dir(file_name, count + 1, dir_path.parent)
        return result
    else:
        return dir_path


def deprecated(describe):
    def decorator(func):
        def wrapped(*args, **kwargs):
            return None

        return wrapped

    return decorator


def from_url(cls, url, db=None, decode_components=False, **kwargs):
    url = urlparse(url)
    url_options = {}

    for name, value in iteritems(parse_qs(url.query)):
        if value and len(value) > 0:
            parser = URL_QUERY_ARGUMENT_PARSERS.get(name)
            if parser:
                try:
                    url_options[name] = parser(value[0])
                except (TypeError, ValueError):
                    warnings.warn(UserWarning(
                        "Invalid value for `%s` in connection URL." % name
                    ))
            else:
                url_options[name] = value[0]

    if decode_components:
        username = unquote(url.username) if url.username else None
        password = unquote(url.password) if url.password else None
        path = unquote(url.path) if url.path else None
        hostname = unquote(url.hostname) if url.hostname else None
    else:
        username = url.username or None
        password = url.password or None
        path = url.path
        hostname = url.hostname

    # We only support redis://, rediss:// and unix:// schemes.
    if url.scheme == 'unix':
        url_options.update({
            'username': username,
            'password': password,
            'path': path,
            'connection_class': UnixDomainSocketConnection,
        })

    elif url.scheme in ('redis', 'rediss'):
        url_options.update({
            'host': hostname,
            'port': int(url.port or 6379),
            'username': username,
            'password': password,
        })

        # If there's a path argument, use it as the db argument if a
        # querystring value wasn't specified
        if 'db' not in url_options and path:
            try:
                url_options['db'] = int(path.replace('/', ''))
            except (AttributeError, ValueError):
                pass

        if url.scheme == 'rediss':
            url_options['connection_class'] = SSLConnection
    else:
        valid_schemes = ', '.join(('redis://', 'rediss://', 'unix://'))
        raise ValueError('Redis URL must specify one of the following '
                         'schemes (%s)' % valid_schemes)

    # last shot at the db value
    url_options['db'] = int(url_options.get('db', db or 0))

    # update the arguments from the URL values
    kwargs.update(url_options)

    # backwards compatability
    if 'charset' in kwargs:
        warnings.warn(DeprecationWarning(
            '"charset" is deprecated. Use "encoding" instead'))
        kwargs['encoding'] = kwargs.pop('charset')
    if 'errors' in kwargs:
        warnings.warn(DeprecationWarning(
            '"errors" is deprecated. Use "encoding_errors" instead'))
        kwargs['encoding_errors'] = kwargs.pop('errors')

    return cls(**kwargs)
