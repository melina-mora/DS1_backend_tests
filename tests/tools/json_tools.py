from jsonpath_ng import parse
import json


class Parser:

    @staticmethod
    def string_to_json(source):
        try:
            load_input_json = json.loads(source)
        except ValueError as e:
            raise Exception("Could not parse '%s' as JSON: %s"%(source, e))

        return load_input_json

    @staticmethod
    def update_json(body, path, new_value, index=0):
        jsonpath_expr = parse(path)
        result = jsonpath_expr.update(body, new_value)
        return result




