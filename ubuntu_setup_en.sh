#!/bin/bash
# Ubuntu/Windows Auto Switcher - Ubuntu Setup Script

echo "Ubuntu/Windows Auto Switcher - Ubuntu Setup Script"
echo "=================================================="
echo

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "[ERROR] This script must be run as root"
    echo "Please run with sudo: sudo ./ubuntu_setup_en.sh"
    exit 1
fi

# Get log directory
LOG_DIR=$(python3 - <<'PY'
from windows_ubuntu_switcher.config import LOG_DIR
print(LOG_DIR)
PY
)

# Create mount point directory
echo "Creating mount point directory..."
mkdir -p /mnt/windows
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create mount point directory"
    exit 1
fi
echo "[SUCCESS] Mount point directory created: /mnt/windows"

# Find shared partition
echo "Finding shared partition..."
SHARED_PART=$(blkid | grep -i "LABEL=\"SHARED\"" | cut -d: -f1)
if [ -z "$SHARED_PART" ]; then
    echo "[WARNING] No partition with label SHARED found"
    echo "Please enter the device path of the shared partition (e.g. /dev/sda3):"
    read SHARED_PART
    if [ -z "$SHARED_PART" ]; then
        echo "[ERROR] No partition path provided"
        exit 1
    fi
fi
echo "[SUCCESS] Found shared partition: $SHARED_PART"

# Get partition UUID
SHARED_UUID=$(blkid -s UUID -o value $SHARED_PART)
if [ -z "$SHARED_UUID" ]; then
    echo "[ERROR] Could not get partition UUID"
    exit 1
fi
echo "[SUCCESS] Partition UUID: $SHARED_UUID"

# Configure auto-mount
echo "Configuring auto-mount..."
if grep -q "/mnt/windows" /etc/fstab; then
    echo "[WARNING] Mount configuration for /mnt/windows already exists in /etc/fstab"
else
    echo "# Windows shared partition" >> /etc/fstab
    echo "UUID=$SHARED_UUID /mnt/windows ntfs defaults,auto,rw,users 0 0" >> /etc/fstab
    echo "[SUCCESS] Added auto-mount configuration to /etc/fstab"
fi

# Mount partition
echo "Mounting shared partition..."
mount -a
if [ $? -ne 0 ]; then
    echo "[WARNING] Failed to mount partition, please check /etc/fstab configuration"
else
    echo "[SUCCESS] Shared partition mounted"
fi

# Set permissions
echo "Setting partition permissions..."
chmod 777 /mnt/windows
if [ $? -ne 0 ]; then
    echo "[WARNING] Failed to set permissions"
else
    echo "[SUCCESS] Partition permissions set"
fi

# Copy script to system directory
echo "Copying startup script to system directory..."
cp ubuntu-windows-switcher.sh /usr/local/bin/
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to copy script"
    exit 1
fi
chmod +x /usr/local/bin/ubuntu-windows-switcher.sh
echo "[SUCCESS] Script copied to /usr/local/bin/"

# Install systemd service
echo "Installing systemd service..."
cp ubuntu-windows-switcher.service /etc/systemd/system/
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to copy service file"
    exit 1
fi
systemctl daemon-reload
systemctl enable ubuntu-windows-switcher.service
if [ $? -ne 0 ]; then
    echo "[WARNING] Failed to enable service"
else
    echo "[SUCCESS] Service enabled"
fi

# Find Windows boot entry
echo "Finding Windows boot entry in GRUB..."
WINDOWS_ENTRIES=$(grep -i "menuentry " /boot/grub/grub.cfg | grep -i windows)
if [ -z "$WINDOWS_ENTRIES" ]; then
    echo "[WARNING] No Windows boot entry found, please check GRUB configuration manually"
else
    echo "Found the following Windows boot entries:"
    echo "$WINDOWS_ENTRIES"
    
    # Extract the first Windows boot entry name
    WINDOWS_ENTRY=$(echo "$WINDOWS_ENTRIES" | head -n 1 | sed -n 's/.*menuentry \+"\([^"]*\)".*/\1/p')
    if [ -n "$WINDOWS_ENTRY" ]; then
        echo "Will use boot entry: $WINDOWS_ENTRY"
        
        # Update Windows boot entry name in script
        sed -i "s/WINDOWS_GRUB_ENTRY=\"Windows Boot Manager\"/WINDOWS_GRUB_ENTRY=\"$WINDOWS_ENTRY\"/" /usr/local/bin/ubuntu-windows-switcher.sh
        echo "[SUCCESS] Updated Windows boot entry name in script"
    fi
fi

# Test grub-reboot command
echo "Testing grub-reboot command..."
which grub-reboot > /dev/null
if [ $? -ne 0 ]; then
    echo "[WARNING] grub-reboot command not found, please ensure grub2 is installed"
else
    echo "[SUCCESS] grub-reboot command available"
fi

# Create log directory
echo "Creating log file..."
touch /var/log/ubuntu-windows-switcher.log
chmod 666 /var/log/ubuntu-windows-switcher.log
echo "[SUCCESS] Log file created: /var/log/ubuntu-windows-switcher.log"

echo
echo "Ubuntu setup completed!"
echo "The system will automatically check for the flag file on next boot and perform the appropriate action."
echo
echo "You can manually test the script with:"
echo "sudo /usr/local/bin/ubuntu-windows-switcher.sh"
echo
echo "To view logs, use:"
echo "cat /var/log/ubuntu-windows-switcher.log"
echo

# Ask if want to test now
echo "Do you want to test the script now? (y/n)"
read TEST_NOW
if [ "$TEST_NOW" = "y" ] || [ "$TEST_NOW" = "Y" ]; then
    echo "Running test..."
    /usr/local/bin/ubuntu-windows-switcher.sh
fi

echo "Setup complete!"
echo "Logs have been saved to ${LOG_DIR}. Please attach the log file when reporting issues."