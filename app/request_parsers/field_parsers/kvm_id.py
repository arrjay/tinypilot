import re
import db.settings

from request_parsers import errors

_KVM_PATTERN = re.compile(r'^[a-z0-9.\-_]*$', re.IGNORECASE)

def parse_kvm_id(id):
    if not isinstance(id, str):
        raise errors.InvalidPortIdError('Kvm ID must be a string')
    if not (1 <= len(id) <= 255):
        raise errors.InvalidPortIdError('Kvm ID must be 1-255 characters'
                                        ' in length')
    if not _KVM_PATTERN.match(id):
        raise errors.InvalidKvmIdError(
            'Kvm ID can only contain characters a-z, A-Z, 0-9, or .-_')

    kvm_str_id = id.lower()
    # filter to KVM units with at least one port
    kvm_int_data = db.settings.Settings().get_kvm_unitdata(kvm_str_id, 1)

    # KVM needs to have a commandscript or a portscript to be considered
    # something worth talking to
    if not kvm_int_data:
        if not kvm_int_data['portscript'] and not kvm_int_data['commandscript']:
            raise
        raise errors.InvalidKvmIdError(
            'Kvm ID not found or enabled in database')

    return [ kvm_str_id, kvm_int_data ]
