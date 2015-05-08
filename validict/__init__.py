def validate(template, unvalidated, quiet=False):
    try:
        if isinstance(template, tuple):
            # We have multiple options on the template level.
            valid = False
            for template_option in template:
                try:
                    valid = validate(template_option, unvalidated)
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
            if all([validate(template[key], unvalidated.get(key)) for key in template]):
                return True
            else:
                raise FailedValidationError("{0} in template did not match topmost level of {1}".format(template, unvalidated))

        elif isinstance(template, list) and isinstance(unvalidated, list):
            # Two lists. The template list should have one element to demonstrate its members'
            # structure. This can be a tuple.
            if all([validate(template[0], item) for item in unvalidated]):
                return True
            else:
                raise FailedValidationError("Not all list items in {0} matched template {1}".format(unvalidated, template))

        elif isinstance(template, type):
            # Template declared a type. Time to compare values.
            if isinstance(unvalidated, template):
                return True
            else:
                raise FailedValidationError("{0} is not of type {1}".format(unvalidated, template))

        else:
            if template == unvalidated or template is None:
                return True
            else:
                raise FailedValidationError("{0} is not equal to {1}".format(unvalidated, template))
    except FailedValidationError, e:
        if quiet:
            return False
        else:
            raise e


class FailedValidationError(Exception):
    pass
