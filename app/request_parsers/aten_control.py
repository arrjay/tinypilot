from request_parsers import json
from request_parsers.field_parsers import aten_control_seq as command_parser


def parse(request):
    """Parses the aten control command from the Flask request body.

    Args:
        request: Flask request with the following fields in the body:
            (str) command

    Returns:
        The ATEN command if successfully parsed.

    Raises:
        InvalidAtenCommandError: if the command is invalid.
    """
    (command,) = json.parse_json_body(request,
                                     required_fields=('command',))

    return command_parser.parse_aten_command(command)
