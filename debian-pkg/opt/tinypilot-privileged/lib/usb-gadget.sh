#!/bin/bash

# Shared parameters and functionality for the usb gadget.
# See: docs/usb-gadget-driver.md

export USB_DEVICE_DIR="g"
readonly USB_DEVICE_DIR
export USB_GADGET_PATH="/sys/kernel/config/usb_gadget"
readonly USB_GADGET_PATH
export USB_DEVICE_PATH="${USB_GADGET_PATH}/${USB_DEVICE_DIR}"
readonly USB_DEVICE_PATH

export USB_STRINGS_DIR="strings/0x409"
readonly USB_STRINGS_DIR
export USB_KEYBOARD_FUNCTIONS_DIR="functions/hid.keyboard"
readonly USB_KEYBOARD_FUNCTIONS_DIR
export USB_MOUSE_FUNCTIONS_DIR="functions/hid.mouse"
readonly USB_MOUSE_FUNCTIONS_DIR
export USB_MOUSE_REL_FUNCTIONS_DIR="functions/hid.mouse_rel"
readonly USB_MOUSE_REL_FUNCTIONS_DIR
export USB_MASS_STORAGE_NAME="mass_storage.0"
readonly USB_MASS_STORAGE_NAME
export USB_MASS_STORAGE_FUNCTIONS_DIR="functions/${USB_MASS_STORAGE_NAME}"
readonly USB_MASS_STORAGE_FUNCTIONS_DIR

export USB_CONFIG_INDEX=1
readonly USB_CONFIG_INDEX
export USB_CONFIG_DIR="configs/c.${USB_CONFIG_INDEX}"
readonly USB_CONFIG_DIR
export USB_ALL_CONFIGS_DIR="configs/*"
readonly USB_ALL_CONFIGS_DIR
export USB_ALL_FUNCTIONS_DIR="functions/*"
readonly USB_ALL_FUNCTIONS_DIR

function usb_gadget_activate {
  ls /sys/class/udc > "${USB_DEVICE_PATH}/UDC"
  # shellcheck disable=SC2199 # We want to flatten the array here. Not an error.
  if [[ -n "$@" ]]; then
    chmod 777 "$@"
  fi
}
export -f usb_gadget_activate

function usb_gadget_deactivate {
  echo '' > "${USB_DEVICE_PATH}/UDC"
}
export -f usb_gadget_deactivate
