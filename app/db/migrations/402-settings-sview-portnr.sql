-- Add column in settings table identifying how many ports are on
-- an attached ATEN KVM, if any.

ALTER TABLE settings
ADD COLUMN sview_kvm_portnr INTEGER;
