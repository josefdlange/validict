from __future__ import unicode_literals

# Normalize python2 and python3 vacaboulary
# http://www.rfk.id.au/blog/entry/preparing-pyenchant-for-python-3/
try:
    is_python2 = str != unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    is_python2 = False
    unicode = str
    basestring = (str, bytes)
else:
    # 'unicode' exists, must be Python 2
    bytes = str


def validate(template, unvalidated, quiet=False, **kwargs):
    try:
        if isinstance(template, tuple):
            # We have multiple options on the template level.
            valid = False
            for template_option in template:
                try:
                    valid = validate(template_option, unvalidated, **kwargs)
                    if valid:
                        break
                except FailedValidationError:
                    pass
            if valid:
                return True
            else:
                raise FailedValidationError("None of {0} in template match topmost level of {1}".format(template, unvalidated))

        elif isinstance(template, dict) and isinstance(unvalidated, dict):
            # Two dictionaries. Compare key-by-key!
            if all([validate(template[key], unvalidated.get(key), **kwargs) for key in template]):
                return True
            else:
                raise FailedValidationError("{0} in template did not match topmost level of {1}".format(template, unvalidated))

        elif isinstance(template, list) and isinstance(unvalidated, list):
            # Two lists. The template list should have one element to demonstrate its members'
            # structure. This can be a tuple.
            if all([validate(template[0], item, **kwargs) for item in unvalidated]):
                return True
            else:
                raise FailedValidationError("Not all list items in {0} matched template {1}".format(unvalidated, template))

        elif isinstance(template, type):
            # Template declared a type. Time to compare values.
            if template in (str, unicode) and kwargs.get('fuzzy_string_typing'):
                template = basestring

            if isinstance(unvalidated, template):
                return True
            else:
                raise FailedValidationError("{0} is not of type {1}".format(unvalidated, template))

        else:
            if template == unvalidated or template is None:
                return True
            else:
                raise FailedValidationError("{0} is not equal to {1}".format(unvalidated, template))
    except FailedValidationError as e:
        if quiet:
            return False
        else:
            raise e


class FailedValidationError(Exception):
    pass


def deep_merge(base, incoming):
    if not isinstance(base, dict) or not isinstance(incoming, dict):
        return incoming
    for key in incoming:
        if key in base:
            base[key] = deep_merge(base[key], incoming[key])
        else:
            base[key] = incoming[key]
    return base
