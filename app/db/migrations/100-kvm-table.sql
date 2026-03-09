-- Create a table for storing KVM configurations.
-- This includes id (primary key)
--               codename (script entity name)
--               label (UI name)
--               ports
--               portscript (if defined, do not use generic port script)
--               commands (json structure of valid commands)
--               commandscript (if defined, script for command handling)

CREATE TABLE IF NOT EXISTS external_kvm(
    id INTEGER PRIMARY KEY,
    codename TEXT NOT NULL UNIQUE,
    label TEXT NOT NULL UNIQUE,
    ports INTEGER NOT NULL,
    portscript TEXT,
    commandscript TEXT
);

CREATE TABLE IF NOT EXISTS external_kvm_commands(
    id INTEGER PRIMARY KEY,
    kvm_id INTEGER,
    action TEXT NOT NULL UNIQUE,
    label TEXT NOT NULL UNIQUE
);

-- for compatibility (or convenience), pre-populate the tables.
INSERT OR IGNORE INTO external_kvm(id, codename, label, ports, portscript)
VALUES (NULL, 'linksys_sview', 'SVIEW', 0, '/usr/lib/tinypilot/scripts/sview-port');

-- notice we supplied a command script
INSERT OR IGNORE INTO external_kvm(id, codename, label, ports, portscript, commandscript)
VALUES (NULL, 'aten_cs', 'ATEN', 0, '/usr/lib/tinypilot/scripts/aten-port', '/usr/lib/tinypilot/scripts/aten-control');

INSERT OR IGNORE INTO external_kvm_commands(id, kvm_id, action, label)
VALUES
  (NULL, (SELECT id FROM external_kvm WHERE codename = 'aten_cs'), 'reset', 'Reset KVM'),
  (NULL, (SELECT id FROM external_kvm WHERE codename = 'aten_cs'), 'sync-edid', 'Sync Monitor EDID'),
  (NULL, (SELECT id FROM external_kvm WHERE codename = 'aten_cs'), 'toggle-mouseemu', 'Toggle Mouse Emulation'),
  (NULL, (SELECT id FROM external_kvm WHERE codename = 'aten_cs'), 'report', 'Report KVM Configuration');
