import jsonpath_ng
import json
from copy import deepcopy


def string_to_json(source):
    try:
        if source is type(str):
            load_input_json = json.loads(source)
            return load_input_json
        elif source is type(dict):
            load_input_json = json.dumps(source)
            return load_input_json
        else:
            return source
    except ValueError as e:
        raise Exception("Could not parse '%s' as JSON: %s"%(source, e))


def update_json(body, values):
    if type(values) is dict:
        body = string_to_json(body)
        for value in values:
            jsonpath_expr = deepcopy(jsonpath_ng.parse(value))
            r = deepcopy(jsonpath_expr.update(body, values[value]))
        return r
    else:
        raise SyntaxError("Format not supported. Try: {'$.path':'new_value'}")


def extract(body, path, multiple=False):
    jsonpath_expr = deepcopy(jsonpath_ng.parse(path))
    result = [match.value for match in jsonpath_expr.find(body)]
    if multiple:
        return result
    else:
        return result[0]



