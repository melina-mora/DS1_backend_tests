import jsonpath_ng
import json


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


def update_json(body, path, new_value):
    body = string_to_json(body)
    jsonpath_expr = jsonpath_ng.parse(path)
    result = jsonpath_expr.update(body, new_value)
    return result


def extract(body, path, multiple=False):
    jsonpath_expr = jsonpath_ng.parse(path)
    result = [match.value for match in jsonpath_expr.find(body)]
    if multiple:
        return result
    else:
        return result[0]



