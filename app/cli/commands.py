import db.settings
from cli.registry import command


@command('streaming-mode')
def streaming_mode(_args):
    """Prints the currently applicable streaming mode."""
    mode = db.settings.Settings().get_streaming_mode().value
    print(mode)

@command('show-https-mode')
def show_https_mode(_args):
    """Prints whether the TinyPilot app is requiring HTTPS."""
    mode = db.settings.Settings().requires_https()
    print(mode)

@command('set-https-mode')
def set_https_mode(_args):
    """Configures if TinyPilot requires HTTPS. Takes a string, interpolates as boolean."""
    try:
        setting = _args[0]
        if setting == True:
            db.settings.Settings().set_requires_https(1)
        else:
            db.settings.Settings().set_requires_https(0)
    except Exception as e:
        raise e
