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

    def get_kvm_unitdata(self, kvmid):
        """Return External KVM Data:

        This is a Python object detailing the KVM configuration for a specific
            unit. It must contain a row id, and a portscript or commandscript.
        """
        cursor = self._db_connection.execute(
            'SELECT id, portscript, commandscript, ports FROM external_kvm WHERE ports > 0 AND codename=?', [kvmid]
        )
        row = cursor.fetchone()
        if not row:
            raise

        (intid,portscript,commandscript, ports) = row

        if not portscript and not commandscript:
            raise

        return { 'intid': intid, 'portscript': portscript, 'commandscript': commandscript, 'ports': ports }

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

    def get_kvm_definitions(self):
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
                c2 = self._db_connection.execute(
                    'SELECT action, label FROM external_kvm_commands WHERE kvm_id=? ORDER BY label', [kvm_id])
                actions = c2.fetchall()
                verbs = [{x[0]: x[1]} for x in actions]
                if len(actions) > 0:
                    verbs = {}
                    for x in actions:
                        verbs[x[0]] = x[1]
                    res[codename]['verbs'] = verbs
        return res

    def get_gpio_kvm_script(self):
        """Retrieves path to a simple gpio-controlling (flip) script for a KVM

        If there is no setting in the database, it returns False

        Returns:
            string or False.
        """
        cursor = self._db_connection.execute(
            'SELECT gpio_kvm_script FROM settings WHERE id=?', [_ROW_ID])
        raw_value = _fetch_single_value(cursor, "")
        if raw_value == "":
            return False
        else:
            return raw_value

def _fetch_single_value(connection_cursor, default_value):
    """Helper method to resolve a query for one single value."""
    row = connection_cursor.fetchone()
    if not row or row[0] is None:
        return default_value
    return row[0]
