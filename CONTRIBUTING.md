# Contributing to Windows/Ubuntu Switcher

Thank you for your interest in contributing to Windows/Ubuntu Switcher! This document provides guidelines for contributing to the project.

## How Can I Contribute?

### Reporting Bugs

- Use the GitHub issue tracker
- Include detailed steps to reproduce the bug
- Provide system information (OS version, Python version, etc.)
- Include error messages and logs if available

### Suggesting Enhancements

- Use the GitHub issue tracker with the "enhancement" label
- Describe the feature and why it would be useful
- Consider the impact on existing functionality

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.6 or higher
- Git

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/windows-ubuntu-switcher.git
   cd windows-ubuntu-switcher
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python windows_ubuntu_switcher/main.py
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

## Testing

- Test on both Windows and Ubuntu systems
- Verify dual-boot switching functionality
- Test error handling and edge cases

## Questions?

If you have questions about contributing, feel free to:
- Open an issue on GitHub
- Contact the maintainers directly

Thank you for contributing to make Windows/Ubuntu Switcher better!
