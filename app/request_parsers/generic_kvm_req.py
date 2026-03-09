from request_parsers import json, errors
from request_parsers.field_parsers import kvm_id as kvm_parser
import db.settings

def parse(request):
    """Parses the generic KVM control command from the Flask request body.

    Args:
        request: Flask request with the following fields in the body:
            (str) kvmtype
            (str) action

    Returns:
        The kvm command and arguments if successfully parsed.

    Raises:
        InvalidKvmRequestError: if the port is unparseable.
    """
    (kvmtype,action) = json.parse_json_body(request,
                                            required_fields=('kvmtype','action'))
    res = {}
    res['args'] = []

    try:
        (kvm_id_int, kvm_data) = kvm_parser.parse_kvm_id(kvmtype)
    except errors.Error as e:
        raise errors.InvalidKvmUnitError(
            'Failed to validate KVM request') from e

    # 'portselect' is the port-selection action which we don't validate against
    # the command table
    if action == 'portselect':
        if kvm_data['portscript']:
            res['script'] = kvm_data['portscript']
        else:
            res['script'] = kvm_data['commandscript']
            res['args'].append('portselect')
        # but we _do_ need to validate a port is valid now.
        try:
            # trip to int for validation
            port = int(request.get_json()['port'])
            port <= kvm_data['ports']
            # and back to str for running
            res['args'].append(str(port))
        except errors.Error as e:
            raise errors.InvalidKvmParameterError(
                'Valid port number required for this request') from e
        # shortcut and get outta here
        return res

    # this is the non-port-select case.
    # do we _have_ a commandscript?
    if not kvm_data['commandscript']:
        raise errors.InvalidKvmUnitError(
            'KVM Unit does not have a commandscript defined, no commands') from e

    check = db.settings.Settings().check_kvm_action(kvm_data['intid'], action)
    if not check:
        raise errors.InvalidKvmActionError(
            'KVM Unit does not support this action') from e

    res['args'].append(action)

    res['script'] = kvm_data['commandscript']
    # okay, now we need to verify we have a command that exists...
    return res
