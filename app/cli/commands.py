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

@command('show-kvm-gpio-script')
def show_kvm_gpio_script(_args):
    """Prints if a KVM GPIO Script is configured."""
    kvm_gpio_script = db.settings.Settings().get_gpio_kvm_script()
    if not kvm_gpio_script:
        print("There is no GPIO KVM Script configured.")
    else:
        print(kvm_gpio_script)

@command('set-kvm-gpio-script')
def set_kvm_gpio_script(_args):
    """Configures a GPIO KVM Script for Tinypilot"""
    try:
        if len(_args) < 2:
            script = ''
        else:
            script = _args[1]
        db.settings.Settings().set_gpio_kvm_script(script)
    except Exception as e:
        raise e

@command('show-kvm-aten-ports')
def show_kvm_aten_ports(_args):
    """Prints how many ATEN KVM ports are configured"""
    aten_kvm_ports = db.settings.Settings().get_kvm_aten_portcount()
    print(aten_kvm_ports)

@command('set-kvm-aten-ports')
def set_kvm_aten_ports(_args):
    """Configures the amount of ATEN KVM ports supported. Use 0 for no ports."""
    try:
        if len(_args) < 2:
            ports = 0
        else:
            ports = _args[1]
        db.settings.Settings().set_kvm_aten_portcount(ports)
    except Exception as e:
        raise e
