import db.settings
from cli.registry import command

@command('streaming-mode')
def streaming_mode(_args):
    """Prints the currently applicable streaming mode."""
    mode = db.settings.Settings().get_streaming_mode().value
    print(mode)

@command('show-kvm-external-script')
def show_external_kvm_script(_args):
    """Prints if a KVM External Script is configured."""
    kvm_external_script = db.settings.Settings().get_external_kvm_script()
    if not kvm_external_script:
        print("There is no KVM External Script configured.")
    else:
        print(kvm_external_script)

@command('set-kvm-external-script')
def set_external_kvm_script(_args):
    """Configures a KVM External Script for Tinypilot"""
    try:
        if len(_args) < 2:
            script = ''
        else:
            script = _args[1]
        db.settings.Settings().set_external_kvm_script(script)
    except Exception as e:
        raise e

@command('show-kvm-configuration')
def get_kvm_config(_args):
    """Shows the current External KVM configuration object"""
    try:
        print(db.settings.Settings().get_kvm_definitions())
    except Exception as e:
        raise e
