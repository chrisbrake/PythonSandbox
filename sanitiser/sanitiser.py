from cerberus import Validator


def keys_and_values_are_strings(d):
    """
    Checks to see if the keys and values of this dict are strings.
    :param d: The Dictionary to check
    :return: Boolean, True if all the keys and values are strings.
    """
    if not d:
        return False
    schema = {
        'a_dict': {
            'keyschema': {'type': 'string'},
            'valueschema': {'type': 'string'}}
    }
    v = Validator(schema)
    return v.validate({'a_dict': d})
