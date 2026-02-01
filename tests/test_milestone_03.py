#!/usr/bin/env python3
"""
Milestone 3: Complete Implementation (40 points)
=================================================

This milestone verifies that the student has:
1. Code structure with main() function
2. Error handling for hardware issues
3. Complete working solution validated on hardware
4. Optional: NeoSlider support

These tests verify code completeness and best practices.
"""

import os
import ast
import re
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helper: Get repository root
# ---------------------------------------------------------------------------
def get_repo_root():
    """Find the repository root by looking for .github folder."""
    current = Path(__file__).parent.parent
    if (current / ".github").exists():
        return current
    return current


REPO_ROOT = get_repo_root()


# ---------------------------------------------------------------------------
# Test 3.1: Main Function Structure (10 points)
# ---------------------------------------------------------------------------
def test_main_function_exists():
    """
    Verify that the script has a main() function.

    Expected: A 'def main():' function and __name__ guard

    Suggestion: Structure your code like this:
        def main():
            # Your code here

        if __name__ == "__main__":
            main()
    """
    script_path = REPO_ROOT / "test_bmp280.py"

    if not script_path.exists():
        pytest.skip("test_bmp280.py not found")

    content = script_path.read_text()

    has_main = "def main(" in content or "def main():" in content
    has_guard = '__name__' in content and '__main__' in content

    if not has_main:
        pytest.fail(
            f"\n\n"
            f"Expected: A main() function for code organization\n"
            f"Actual: No main() function found\n\n"
            f"Suggestion: Organize your code with a main function:\n"
            f"  def main():\n"
            f"      i2c = board.I2C()\n"
            f"      sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)\n"
            f"      print(f\"Temperature: {{sensor.temperature:.1f}} C\")\n"
            f"\n"
            f"  if __name__ == \"__main__\":\n"
            f"      main()\n"
        )

    if not has_guard:
        pytest.fail(
            f"\n\n"
            f"Expected: __name__ == \"__main__\" guard\n"
            f"Actual: No __main__ guard found\n\n"
            f"Suggestion: Add at the end of your script:\n"
            f"  if __name__ == \"__main__\":\n"
            f"      main()\n"
            f"\n"
            f"This ensures main() only runs when script is executed directly.\n"
        )


# ---------------------------------------------------------------------------
# Test 3.2: Error Handling (10 points)
# ---------------------------------------------------------------------------
def test_error_handling():
    """
    Verify that the script includes error handling.

    Expected: try/except blocks for hardware errors

    Suggestion: Wrap hardware code in try/except:
        try:
            sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        except Exception as e:
            print(f"Error: {e}")
    """
    script_path = REPO_ROOT / "test_bmp280.py"

    if not script_path.exists():
        pytest.skip("test_bmp280.py not found")

    content = script_path.read_text()

    has_try = "try:" in content
    has_except = "except" in content

    if not (has_try and has_except):
        pytest.fail(
            f"\n\n"
            f"Expected: Error handling with try/except blocks\n"
            f"Actual: No error handling found\n\n"
            f"Suggestion: Add error handling for robustness:\n"
            f"  try:\n"
            f"      i2c = board.I2C()\n"
            f"      sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)\n"
            f"      print(f\"Temperature: {{sensor.temperature:.1f}} C\")\n"
            f"  except Exception as e:\n"
            f"      print(f\"Error reading sensor: {{e}}\")\n"
            f"      print(\"Check: I2C enabled? Sensor connected? Correct address?\")\n"
        )


# ---------------------------------------------------------------------------
# Test 3.3: Altitude Calculation (Optional - 5 points)
# ---------------------------------------------------------------------------
def test_altitude_reading():
    """
    Verify that the script reads altitude (optional bonus).

    Expected: Code that accesses sensor.altitude

    Suggestion: Read altitude with:
        altitude = sensor.altitude
        print(f"Altitude: {altitude:.1f} m")
    """
    script_path = REPO_ROOT / "test_bmp280.py"

    if not script_path.exists():
        pytest.skip("test_bmp280.py not found")

    content = script_path.read_text()

    has_altitude = ".altitude" in content

    if not has_altitude:
        # This is optional - just a warning, not a failure
        pytest.skip(
            "Altitude reading not found - this is optional but recommended"
        )


# ---------------------------------------------------------------------------
# Test 3.4: All Local Tests Passed (10 points)
# ---------------------------------------------------------------------------
def test_all_local_tests_passed():
    """
    Verify that all local tests passed on Raspberry Pi.

    Expected: all_tests_passed.txt marker file

    Suggestion: Ensure validate_pi.py completes successfully.
    """
    markers_dir = REPO_ROOT / ".test_markers"

    if not markers_dir.exists():
        pytest.fail(
            f"\n\n"
            f"Expected: .test_markers/ directory\n"
            f"Actual: Directory not found\n\n"
            f"Suggestion: Run validate_pi.py on your Raspberry Pi.\n"
        )

    passed_marker = markers_dir / "all_tests_passed.txt"
    bmp_marker = markers_dir / "bmp280_script_verified.txt"
    ssh_marker = markers_dir / "ssh_key_verified.txt"

    if passed_marker.exists():
        return  # All good!

    # Check which markers we have
    existing_markers = [f.name for f in markers_dir.glob("*.txt")]

    if bmp_marker.exists() and ssh_marker.exists():
        # Core markers exist, close enough
        return

    pytest.fail(
        f"\n\n"
        f"Expected: all_tests_passed.txt marker (or core markers)\n"
        f"Actual: Found markers: {existing_markers}\n\n"
        f"Suggestion: Ensure all local tests pass:\n"
        f"  python3 validate_pi.py\n"
        f"\n"
        f"If tests fail, fix the issues and run again.\n"
        f"Then commit and push the .test_markers/ folder.\n"
    )


# ---------------------------------------------------------------------------
# Test 3.5: NeoSlider Script (Optional - 5 points)
# ---------------------------------------------------------------------------
def test_neoslider_script():
    """
    Verify NeoSlider script exists (optional bonus).

    Expected: test_neoslider.py with valid syntax

    Suggestion: Create test_neoslider.py to control the NeoSlider.
    """
    script_path = REPO_ROOT / "test_neoslider.py"

    if not script_path.exists():
        pytest.skip(
            "test_neoslider.py not found - this is optional bonus content"
        )

    content = script_path.read_text()

    try:
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(
            f"\n\n"
            f"Expected: Valid Python syntax in test_neoslider.py\n"
            f"Actual: SyntaxError on line {e.lineno}\n\n"
            f"Suggestion: Fix the syntax error and try again.\n"
        )

    # Check for required imports
    if "adafruit_seesaw" not in content:
        pytest.fail(
            f"\n\n"
            f"Expected: adafruit_seesaw import for NeoSlider\n"
            f"Actual: Import not found\n\n"
            f"Suggestion: Add this import:\n"
            f"  from adafruit_seesaw.seesaw import Seesaw\n"
            f"  from adafruit_seesaw import neopixel\n"
        )


# ---------------------------------------------------------------------------
# Test 3.6: Code Quality Check (5 points)
# ---------------------------------------------------------------------------
def test_code_quality():
    """
    Verify basic code quality standards.

    Expected: Docstrings and comments

    Suggestion: Add documentation to your code.
    """
    script_path = REPO_ROOT / "test_bmp280.py"

    if not script_path.exists():
        pytest.skip("test_bmp280.py not found")

    content = script_path.read_text()

    # Check for docstring or comments
    has_docstring = '"""' in content or "'''" in content
    has_comments = content.count("#") >= 3  # At least 3 comment lines

    if not (has_docstring or has_comments):
        pytest.fail(
            f"\n\n"
            f"Expected: Documentation (docstrings or comments)\n"
            f"Actual: Minimal documentation found\n\n"
            f"Suggestion: Add documentation to explain your code:\n"
            f"  \"\"\"Script to read BMP280 temperature and pressure.\"\"\"\n"
            f"\n"
            f"  # Initialize I2C bus\n"
            f"  i2c = board.I2C()\n"
        )
