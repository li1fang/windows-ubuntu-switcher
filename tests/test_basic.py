import unittest
import sys
import os

# Add the parent directory to the path so we can import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestBasicFunctionality(unittest.TestCase):
    """Basic tests for Windows/Ubuntu Switcher"""
    
    def test_imports(self):
        """Test that we can import the main modules"""
        try:
            import windows_ubuntu_switcher
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import windows_ubuntu_switcher: {e}")
    
    def test_config_exists(self):
        """Test that configuration files exist"""
        config_file = os.path.join(os.path.dirname(__file__), '..', 'windows_ubuntu_switcher', 'config.py')
        self.assertTrue(os.path.exists(config_file), "config.py should exist")
    
    def test_main_module_exists(self):
        """Test that main.py exists"""
        main_file = os.path.join(os.path.dirname(__file__), '..', 'windows_ubuntu_switcher', 'main.py')
        self.assertTrue(os.path.exists(main_file), "main.py should exist")

if __name__ == '__main__':
    unittest.main()
