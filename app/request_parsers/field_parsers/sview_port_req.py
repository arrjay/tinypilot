from request_parsers import errors

def parse_sview_port(port):
    if not isinstance(port, int):
        raise errors.InvalidSviewPortError('Port ID not numeric')

    if str(9) in str(port):
        raise errors.InvalidSviewPortError('Port IDs do not include digit 9')

    if str(0) in str(port):
        raise errors.InvalidSviewPortError('Port IDs do not include digit 0')

    return port
