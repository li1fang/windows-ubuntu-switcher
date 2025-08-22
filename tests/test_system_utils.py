import os
import sys
import unittest
from unittest.mock import patch

# Ensure modules can be imported when absolute imports are used internally
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
PACKAGE_DIR = os.path.join(PROJECT_ROOT, 'windows_ubuntu_switcher')
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, PACKAGE_DIR)

from windows_ubuntu_switcher.system_utils import create_flag_file, check_system_status


class TestSystemUtils(unittest.TestCase):
    @patch('windows_ubuntu_switcher.system_utils.time.sleep', return_value=None)
    @patch('windows_ubuntu_switcher.system_utils.messagebox.showerror')
    @patch('windows_ubuntu_switcher.system_utils.os.path.exists', return_value=False)
    def test_create_flag_file_s_drive_missing(self, mock_exists, mock_msgbox, mock_sleep):
        result = create_flag_file()
        self.assertFalse(result)
        mock_msgbox.assert_called_once()

    def test_check_system_status(self):
        with patch('windows_ubuntu_switcher.system_utils.os.path.exists', return_value=True), \
             patch('platform.system', return_value='TestOS'), \
             patch('platform.version', return_value='1.0'):
            status = check_system_status()
        self.assertEqual(status['system'], 'TestOS 1.0')
        self.assertTrue(status['s_drive_accessible'])


if __name__ == '__main__':
    unittest.main()
