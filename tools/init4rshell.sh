#!/bin/bash

USB1="/dev/serial/by-path/platform-fd500000.pcie-pci-0000\:01\:00.0-usb-0\:1.1\:1.0"
USB2="/dev/serial/by-path/platform-fd500000.pcie-pci-0000\:01\:00.0-usb-0\:1.2\:1.0"
USB3="/dev/serial/by-path/platform-fd500000.pcie-pci-0000\:01\:00.0-usb-0\:1.3\:1.0"
USB4="/dev/serial/by-path/platform-fd500000.pcie-pci-0000\:01\:00.0-usb-0\:1.4\:1.0"

echo
echo 'To connect type:'
echo 'rshell -p  $USB3 --buffer-size 512'
