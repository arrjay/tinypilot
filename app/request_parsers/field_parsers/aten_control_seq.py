from request_parsers import errors

ATEN_COMMANDS = [
        'reset',
        'switch-hsm-alt',
        'report',
        'sync-edid',
        'toggle-mouse-emulation',
        ]

def parse_aten_command(value):
    if not isinstance(value, str):
        raise errors.InvalidAtenCommandError('Command must be a string')

    if not value in ATEN_COMMANDS:
        raise errors.InvalidAtenCommandError('Command not in verb list')

    return value
