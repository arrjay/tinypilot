import re

from request_parsers import errors

_PORT_PATTERN = re.compile(r'^[a-z0-9.\-_]*$', re.IGNORECASE)

def parse_port_id(id):
    if not isinstance(id, str):
        raise errors.InvalidPortIdError('Port ID must be a string')
    if not (1 <= len(id) <= 255):
        raise errors.InvalidPortIdError('Port ID must be 1-255 characters'
                                        ' in length')
    if not _PORT_PATTERN.match(id):
        raise errors.InvalidPortIdError(
            'Port ID can only contain characters a-z, A-Z, 0-9, or .-_')

    return id.lower()
