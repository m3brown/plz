from jsonschema import exceptions, validate

from plz.colorize import print_error

from .v1 import schema as v1_schema
from .v2 import schema as v2_schema


class DeprecatedSchemaException(Exception):
    pass


DEPRECATED_SCHEMA_MESSAGE = """
Deprecated YAML schema: The schema for the plz.yaml file changed in plz-cmd==1.0.3, \
and is not backwards compatible with previous versions. To continue using the legacy \
schema, use plz-cmd==0.9.0.
"""


def deprecated_schema_message():
    print_error(DEPRECATED_SCHEMA_MESSAGE)


def check_integer_values(exception):
    integer_message = "expected string or bytes-like object"
    if str(exception) == integer_message:
        raise exceptions.ValidationError(
            "Parsing exception: '{}'. Confirm all integer values in the plz.yaml config are wrapped in quotes.".format(
                integer_message
            )
        )


def validate_configuration_data(parsed_data):
    try:
        validate(parsed_data, v2_schema)
    except exceptions.ValidationError as e:
        try:
            validate(parsed_data, v1_schema)
        except Exception:
            # Raise the original validation exception for v2
            raise e
        # If validation does not raise an exception, the config is
        # using the deprecated v1 schema.
        # TODO: fully deprecate (raise exception) in a future version
        # deprecated_schema_message()
        # raise DeprecatedSchemaException()
    except TypeError as e:
        check_integer_values(e)
        raise e
