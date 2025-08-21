import os
import sys
import unittest
from unittest.mock import patch

# Ensure package and its modules can be imported when they use absolute imports
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
PACKAGE_DIR = os.path.join(PROJECT_ROOT, 'windows_ubuntu_switcher')
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, PACKAGE_DIR)

from windows_ubuntu_switcher.api import WindowsUbuntuSwitcherAPI, parse_args


class TestWindowsUbuntuSwitcherAPI(unittest.TestCase):
    def test_get_status_success(self):
        mock_status = {'system': 'TestOS', 's_drive_accessible': True}
        with patch('windows_ubuntu_switcher.api.check_system_status', return_value=mock_status):
            result = WindowsUbuntuSwitcherAPI.get_status()
        self.assertTrue(result['success'])
        self.assertEqual(result['status'], mock_status)

    @patch('windows_ubuntu_switcher.api.reboot_system')
    @patch('windows_ubuntu_switcher.api.create_flag_file')
    def test_switch_to_ubuntu_non_silent_success(self, mock_create, mock_reboot):
        mock_create.return_value = True
        api = WindowsUbuntuSwitcherAPI()
        result = api.switch_to_ubuntu(silent=False)
        self.assertTrue(result['success'])
        self.assertIn('标志文件创建成功', result['message'])
        mock_reboot.assert_not_called()

    @patch('windows_ubuntu_switcher.api.reboot_system')
    @patch('windows_ubuntu_switcher.api.create_flag_file')
    def test_switch_to_ubuntu_silent_success(self, mock_create, mock_reboot):
        mock_create.return_value = True
        mock_reboot.return_value = True
        api = WindowsUbuntuSwitcherAPI()
        result = api.switch_to_ubuntu(silent=True)
        self.assertTrue(result['success'])
        self.assertIn('系统重启中', result['message'])
        mock_reboot.assert_called_once()

    @patch('windows_ubuntu_switcher.api.reboot_system')
    @patch('windows_ubuntu_switcher.api.create_flag_file')
    def test_switch_to_ubuntu_silent_reboot_fail(self, mock_create, mock_reboot):
        mock_create.return_value = True
        mock_reboot.return_value = False
        api = WindowsUbuntuSwitcherAPI()
        result = api.switch_to_ubuntu(silent=True)
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], '系统重启失败')

    @patch('windows_ubuntu_switcher.api.create_flag_file', return_value=False)
    def test_switch_to_ubuntu_create_flag_fail(self, mock_create):
        api = WindowsUbuntuSwitcherAPI()
        result = api.switch_to_ubuntu(silent=False)
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], '标志文件创建失败')


class TestParseArgs(unittest.TestCase):
    def test_parse_args_status(self):
        with patch('windows_ubuntu_switcher.api.sys.argv', ['prog', '--status']):
            args = parse_args()
        self.assertTrue(args.status)
        self.assertFalse(args.switch)

    def test_parse_args_switch_silent_json(self):
        with patch('windows_ubuntu_switcher.api.sys.argv', ['prog', '--switch', '--silent', '--json']):
            args = parse_args()
        self.assertTrue(args.switch)
        self.assertTrue(args.silent)
        self.assertTrue(args.json)


if __name__ == '__main__':
    unittest.main()
