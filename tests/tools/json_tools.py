import json
from copy import deepcopy

import jsonpath_ng
from jsonpath_rw_ext import parse

from tools.exceptions import DataError


def string_to_json(source):
    try:
        if type(source) is str:
            load_input_json = json.loads(source)
            return load_input_json
        else:
            return source
    except ValueError as e:
        raise DataError("Could not parse '%s' as JSON: %s" % (source, e))


def dict_to_json(source):
    try:
        if type(source) is dict:
            load_input_json = json.dumps(source)
            return load_input_json
        else:
            return source
    except ValueError as e:
        raise DataError("Could not parse '%s' as JSON: %s" % (source, e))


def update_json(body, values):
    body = string_to_json(body)
    for value in values:
        jsonpath_expr = jsonpath_ng.parse(value) # Use jsonpath_ng.parse function here to use update() later.
        r = deepcopy(jsonpath_expr.update(body, values[value]))
    return r


def extract(body, path, multiple=False):
    jsonpath_expr = deepcopy(parse(path)) # Use parse from jsonpath-rw-ext here to parse with filters.
    result = [match.value for match in jsonpath_expr.find(body)]
    if multiple:
        return result
    else:
        try:
            return result[0]
        except IndexError as e:
            raise DataError("Could not find requested test data in files. Check test data.")


def pretty_print(body):
    print(json.dumps(body, indent=2))


def prepare_params(**params):
    for old_key in params.keys():
        components = old_key.split('_')
        # We capitalize the first letter of each component except the first one
        # with the 'title' method and join them together.
        new_key = components[0] + ''.join(x.title() for x in components[1:])
        params[new_key] = params.pop(old_key)
    query = ['='.join([k, str(v)]) for k, v in params.items()]
    query = '&'.join(query)
    return query
