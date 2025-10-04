-- Add column in settings table for configuring the path to a GPIO-toggle script
-- that could control a simple (2-port) kvm switch

ALTER TABLE settings
ADD COLUMN gpio_kvm_script TEXT;
