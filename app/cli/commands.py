import db.settings
from cli.registry import command


@command('show-streaming-mode')
def show_streaming_mode(_args):
    """Prints the currently applicable streaming mode."""
    mode = db.settings.Settings().get_streaming_mode().value
    print(mode)

@command('set-streaming-mode')
def set_streaming_mode(_args):
    """Stores the preferred streaming mode."""
    try:
        mode = _args[1]
        if db.settings.StreamingMode(mode):
            db.settings.Settings().set_streaming_mode(db.settings.StreamingMode(mode))
        else:
            raise ValueError("argument not a valid streaming mode")
    except Exception as e:
        raise e

@command('show-https-mode')
def show_https_mode(_args):
    """Prints whether the TinyPilot app is requiring HTTPS."""
    mode = db.settings.Settings().requires_https()
    print(mode)

@command('set-https-mode')
def set_https_mode(_args):
    """Configures if TinyPilot requires HTTPS. Takes a string, interpolates as boolean."""
    try:
        setting = _args[1]
        if setting == True:
            db.settings.Settings().set_requires_https(1)
        else:
            db.settings.Settings().set_requires_https(0)
    except Exception as e:
        raise e
