import enum

import db_connection

# We just store one collection of settings at a time, so the row id is fixed.
_ROW_ID = 1


class StreamingMode(enum.Enum):
    MJPEG = 'MJPEG'
    H264 = 'H264'


class Settings:
    # The columns of the settings table should never have a `NON NULL`
    # constraint, otherwise it wouldn’t be possible to selectively set or update
    # individual columns.

    def __init__(self):
        self._db_connection = db_connection.get()
        # Initialize the table by making sure the “hard-coded” row exists.
        self._db_connection.execute(
            'INSERT OR IGNORE INTO settings(id) VALUES (?)', [_ROW_ID])

    def set_requires_https(self, should_be_required):
        self._db_connection.execute(
            'UPDATE settings SET requires_https=? WHERE id=?',
            [should_be_required, _ROW_ID])

    def requires_https(self):
        """Retrieves the setting whether HTTPS connections are required.

        If there is no setting in the database, it defaults to True.

        Returns:
            bool.
        """
        cursor = self._db_connection.execute(
            'SELECT requires_https FROM settings WHERE id=?', [_ROW_ID])
        # Reminder: the `requires_https` column is of type integer.
        raw_value = _fetch_single_value(cursor, 1)
        return raw_value > 0  # Convert integer value to bool.

    def get_streaming_mode(self):
        """Retrieves the preferred streaming mode for the remote screen.

        Returns:
            A `StreamingMode` value.
        """
        cursor = self._db_connection.execute(
            'SELECT streaming_mode FROM settings WHERE id=?', [_ROW_ID])
        raw_value = _fetch_single_value(cursor, StreamingMode.MJPEG.value)
        return StreamingMode(raw_value)

    def set_streaming_mode(self, streaming_mode):
        """Stores the preferred streaming mode.

        Args:
            streaming_mode: `StreamingMode` value.
        """
        self._db_connection.execute(
            'UPDATE settings SET streaming_mode=? WHERE id=?',
            [streaming_mode.value, _ROW_ID])

    def list_defined_kvms(self):
        """List KVM units defined in tinypilot database.
        """
        cursor = self._db_connection.execute(
            'SELECT codename FROM external_kvm'
        )
        return [x[0] for x in cursor.fetchall()]

    def get_kvm_actions(self, kvmint):
        """Return Actions and Labels for a KVM if it has any
        """
        cursor = self._db_connection.execute(
            'SELECT action, label FROM external_kvm_commands WHERE kvm_id=? ORDER BY label', [kvmint])
        verbs = [{x[0]: x[1]} for x in cursor.fetchall()]
        if len(verbs) == 0:
            return None
        return verbs

    def get_kvm_unitdata(self, kvmid, portct):
        """Return External KVM Data:

        This is a Python object detailing the KVM configuration for a specific
            unit. It must contain a row id, and a portscript or commandscript.
        """
        cursor = self._db_connection.execute(
            'SELECT id, portscript, commandscript, ports FROM external_kvm WHERE ports>=? AND codename=?', [int(portct), kvmid]
        )
        row = cursor.fetchone()
        if not row:
            return None

        (intid,portscript,commandscript, ports) = row

        return { 'intid': intid, 'portscript': portscript, 'commandscript': commandscript, 'ports': ports }

    def create_kvm(self, kvmname, kvmlabel):
        """Create a KVM with the given code name and label"""
        # check if it exists first
        defined = self.get_kvm_unitdata(kvmname, 0)
        if defined:
            print(f"{kvmname} exists")
            raise
        cursor = self._db_connection.execute(
            'INSERT INTO external_kvm(id, codename, label, ports) VALUES (NULL, ?, ?, 0)', [kvmname, kvmlabel]
        )

    def set_kvm_portscript(self, kvmname, scriptpath):
        """Set up the portscript for an External KVM"""
        defined = self.get_kvm_unitdata(kvmname, 0)
        if not defined:
            raise

        cursor = self._db_connection.execute(
            'UPDATE external_kvm SET portscript=? WHERE id=?', [defined['intid'], scriptpath]
        )

    def set_kvm_commandscript(self, kvmname, scriptpath):
        """Set up the commandscript for an External KVM"""
        defined = self.get_kvm_unitdata(kvmname, 0)
        if not defined:
            raise

        cursor = self._db_connection.execute(
            'UPDATE external_kvm SET commandscript=? WHERE id=?', [defined['intid'], scriptpath]
        )

    def delete_kvm(self, kvmname):
        """Delete a KVM by codename, if found"""
        # check if it exists first
        defined = self.get_kvm_unitdata(kvmname, 0)
        if defined:
            action_delete = self._db_connection.execute(
                'DELETE FROM external_kvm_commands WHERE kvm_id=?', [defined['intid']]
            )
            kvm_delete = self._db_connection.execute(
                'DELETE FROM external_kvm WHERE id=?', [defined['intid']]
            )

    def check_kvm_action(self, kvm_intid, action):
        """Return if KVM action is configured
        """
        cursor = self._db_connection.execute(
            'SELECT id FROM external_kvm_commands WHERE kvm_id=? AND action=?', [kvm_intid, action]
        )
        query = cursor.fetchone()
        if query is None:
            return False
        else:
            return True

    def add_kvm_action(self, kvmname, action, label):
        """Set up a KVM action verb/label pair
        """
        defined = self.get_kvm_unitdata(kvmname, 0)
        if not defined:
            raise

        cursor = self._db_connection.execute(
            'INSERT INTO external_kvm_commands (id, kvm_id, action, label) VALUES (NULL, ?, ?, ?)', [defined['intid'], action, label]
        )

    def del_kvm_action(self, kvmname, action):
        """Remove a KVM action
        """
        defined = self.get_kvm_unitdata(kvmname, 0)
        if not defined:
            raise

        cursor = self._db_connection.execute(
            'DELETE FROM external_kvm_commands WHERE kvm_id=? AND action=?', [defined['intid'], action]
        )

    def set_kvm_ports(self, kvmname, portct):
        """Set KVM port count"""
        self._db_connection.execute(
            'UPDATE external_kvm SET ports=? WHERE codename=?', [portct, kvmname]
        )

    def get_kvm_activeconfig(self):
        """Return External KVM configuration object.

        This is a Python object describing the KVM configuration for use in
            TinyPilot custom elements. It can be empty.
        """
        res = {}
        kvm_check = self._db_connection.execute(
            'SELECT SUM(ports) FROM external_kvm')
        kvm_value = _fetch_single_value(kvm_check, 0)

        if kvm_value > 0:
            cursor = self._db_connection.execute(
                'SELECT codename, label, id, ports FROM external_kvm WHERE ports > 0 ORDER BY label')
            for row in cursor:
                codename = row[0]
                label = row[1]
                kvm_id = row[2]
                ports = row[3]
                res[codename] = {'label': label, 'ports': ports}
                verbs = self.get_kvm_actions(kvm_id)
                if verbs:
                    res[codename]['verbs'] = verbs
        return res

def _fetch_single_value(connection_cursor, default_value):
    """Helper method to resolve a query for one single value."""
    row = connection_cursor.fetchone()
    if not row or row[0] is None:
        return default_value
    return row[0]
