from request_parsers import json
from request_parsers.field_parsers import generic_port_id as port_parser

def parse(request):
    """Parses the generic KVM control command from the Flask request body.

    Args:
        request: Flask request with the following fields in the body:
            (str) id

    Returns:
        The port string if successfully parsed.

    Raises:
        InvalidKvmPortError: if the port is unparseable.
    """
    (id,) = json.parse_json_body(request,
                                 requires_fields=('id',))

    return port_parser.parse_port_id(command)
