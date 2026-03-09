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

@command('list-defined-kvms')
def show_kvm_list(_args):
    """Prints External KVM configuration names."""
    kvm_gpio_script = db.settings.Settings().list_defined_kvms()
    for ent in kvm_gpio_script:
        print(ent)

@command('get-kvmconfig')
def show_kvm_detail(_args):
    """Prints configuration data for a single KVM"""
    s = int(16) # padding for print
    data = db.settings.Settings().get_kvm_unitdata(_args[1], 0)
    print(f"{'Portscript:':<{s}}{data['portscript']}")
    print(f"{'Commandscript:':<{s}}{data['commandscript']}")
    print(f"{'Ports:':<{s}}{data['ports']}")
    verbs = db.settings.Settings().get_kvm_actions(data['intid'])
    if verbs is None:
        print(f"{'Actions:':<{s}}{'N/A'}")
    else:
        print(f"{'Actions:'}")
        # find the length of the longest verb so we can adjust padding here
        # if needed
        for dat in verbs:
            for key in dat.keys():
                size = len(key)
                if size > s:
                    s = size + 1
        # now go back and print things.
        for dat in verbs:
            for key in dat.keys():
              print(f"{key:>{s}}{' | '}{dat[key]}")

@command('add-kvm-config')
def add_kvm(_args):
    """Adds an External KVM configuration"""
    try:
        db.settings.Settings().create_kvm(_args[1], _args[2])
    except Exception as e:
        raise e

@command('remove-kvm-config')
def del_kvm(_args):
    """Removes an External KVM configuration"""
    try:
        db.settings.Settings().delete_kvm(_args[1])
    except Exception as e:
        raise e

@command('add-kvm-action')
def add_kvm_command(_args):
    db.settings.Settings().add_kvm_action(_args[1], _args[2], _args[3])

@command('remove-kvm-action')
def add_kvm_command(_args):
    db.settings.Settings().del_kvm_action(_args[1], _args[2])

@command('set-kvm-portscript')
def set_kvm_gpio_script(_args):
    """Configures an External KVM Port Script for Tinypilot"""
    try:
        if len(_args) < 3:
            script = ''
        else:
            script = _args[2]
        db.settings.Settings().set_kvm_portscript(_args[1], script)
    except Exception as e:
        raise e

@command('set-kvm-commandscript')
def set_external_kvm_script(_args):
    """Configures a KVM External Command Script for Tinypilot"""
    try:
        if len(_args) < 3:
            script = ''
        else:
            script = _args[2]
        db.settings.Settings().set_kvm_commandscript(_args[1], script)
    except Exception as e:
        raise e

@command('set-kvm-ports')
def set_kvm_sview_ports(_args):
    """Configures the amount of KVM ports supported.
    Use 0 for no ports.
    Use 1 for 'toggle' type KVM activation.
    """
    unit = _args[1]
    try:
        if len(_args) < 3:
            ports = 0
        else:
            ports = _args[2]
        db.settings.Settings().set_kvm_ports(unit, ports)
    except Exception as e:
        raise e

@command('show-kvm-active-configuration')
def get_kvm_config(_args):
    """Shows the current External KVM configuration object"""
    try:
        print(db.settings.Settings().get_kvm_activeconfig())
    except Exception as e:
        raise e
