from request_parsers import json
from request_parsers.field_parsers import sview_port_req as port_parser


def parse(request):
    """Parses the sview port id request from the Flask request body.

    Args:
        request: Flask request with the following field in the body:
            (int) id

    Returns:
        The port id if successfully parsed.

    Raises:
        InvalidSviewPortError: if the port id is invalid.
    """
    (id,) = json.parse_json_body(request,
                                 required_fields=('id',))

    return port_parser.parse_sview_port(id)
