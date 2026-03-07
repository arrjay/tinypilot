-- Add column in settings table for configuring the path to an external script
-- that will take a port number argument to control an external kvm switch

ALTER table settings
ADD COLUMN generic_kvm_script TEXT;
ALTER table settings
ADD COLUMN generic_kvm_portnr INTEGER;
