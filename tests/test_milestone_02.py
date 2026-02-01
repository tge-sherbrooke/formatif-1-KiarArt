#!/usr/bin/env python3
"""
Milestone 2: Basic Functionality (35 points)
=============================================

This milestone verifies that the student has:
1. Implemented BMP280 sensor reading logic
2. Used I2C communication correctly
3. Created proper temperature/pressure reading functions

These tests analyze code structure - actual hardware testing
is done locally via validate_pi.py.
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
# Test 2.1: I2C Initialization (10 points)
# ---------------------------------------------------------------------------
def test_i2c_initialization():
    """
    Verify that the script initializes I2C communication.

    Expected: Code that creates an I2C bus using board.I2C()

    Suggestion: Initialize I2C with:
        i2c = board.I2C()
    """
    script_path = REPO_ROOT / "test_bmp280.py"

    if not script_path.exists():
        pytest.skip("test_bmp280.py not found")

    content = script_path.read_text()

    # Check for I2C initialization patterns
    has_i2c = any([
        "board.I2C()" in content,
        "busio.I2C" in content,
        "board.SCL" in content,
    ])

    if not has_i2c:
        pytest.fail(
            f"\n\n"
            f"Expected: I2C bus initialization\n"
            f"Actual: No I2C initialization found\n\n"
            f"Suggestion: Add I2C initialization in your code:\n"
            f"  import board\n"
            f"  i2c = board.I2C()  # Uses board.SCL and board.SDA\n"
            f"\n"
            f"The BMP280 communicates via I2C protocol.\n"
        )


# ---------------------------------------------------------------------------
# Test 2.2: BMP280 Sensor Object Creation (10 points)
# ---------------------------------------------------------------------------
def test_bmp280_sensor_creation():
    """
    Verify that the script creates a BMP280 sensor object.

    Expected: BMP280_I2C sensor initialization

    Suggestion: Create sensor with:
        sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    """
    script_path = REPO_ROOT / "test_bmp280.py"

    if not script_path.exists():
        pytest.skip("test_bmp280.py not found")

    content = script_path.read_text()

    # Check for sensor creation patterns
    has_sensor = any([
        "BMP280_I2C" in content,
        "Adafruit_BMP280_I2C" in content,
        "adafruit_bmp280." in content and "i2c" in content.lower(),
    ])

    if not has_sensor:
        pytest.fail(
            f"\n\n"
            f"Expected: BMP280 sensor object creation\n"
            f"Actual: No BMP280 sensor initialization found\n\n"
            f"Suggestion: Create the sensor object:\n"
            f"  import adafruit_bmp280\n"
            f"  sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)\n"
            f"\n"
            f"If your sensor is at address 0x77 (not 0x76):\n"
            f"  sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)\n"
        )


# ---------------------------------------------------------------------------
# Test 2.3: Temperature Reading (7 points)
# ---------------------------------------------------------------------------
def test_temperature_reading():
    """
    Verify that the script reads temperature from the sensor.

    Expected: Code that accesses sensor.temperature

    Suggestion: Read temperature with:
        temp = sensor.temperature
        print(f"Temperature: {temp:.1f} C")
    """
    script_path = REPO_ROOT / "test_bmp280.py"

    if not script_path.exists():
        pytest.skip("test_bmp280.py not found")

    content = script_path.read_text()

    has_temp = any([
        ".temperature" in content,
        "temperature" in content.lower() and "sensor" in content.lower(),
    ])

    if not has_temp:
        pytest.fail(
            f"\n\n"
            f"Expected: Temperature reading from sensor\n"
            f"Actual: No temperature reading found\n\n"
            f"Suggestion: Read temperature like this:\n"
            f"  temperature = sensor.temperature\n"
            f"  print(f\"Temperature: {{temperature:.1f}} C\")\n"
        )


# ---------------------------------------------------------------------------
# Test 2.4: Pressure Reading (8 points)
# ---------------------------------------------------------------------------
def test_pressure_reading():
    """
    Verify that the script reads pressure from the sensor.

    Expected: Code that accesses sensor.pressure

    Suggestion: Read pressure with:
        pressure = sensor.pressure
        print(f"Pressure: {pressure:.1f} hPa")
    """
    script_path = REPO_ROOT / "test_bmp280.py"

    if not script_path.exists():
        pytest.skip("test_bmp280.py not found")

    content = script_path.read_text()

    has_pressure = any([
        ".pressure" in content,
        "pressure" in content.lower() and "sensor" in content.lower(),
    ])

    if not has_pressure:
        pytest.fail(
            f"\n\n"
            f"Expected: Pressure reading from sensor\n"
            f"Actual: No pressure reading found\n\n"
            f"Suggestion: Read pressure like this:\n"
            f"  pressure = sensor.pressure\n"
            f"  print(f\"Pressure: {{pressure:.1f}} hPa\")\n"
            f"\n"
            f"The BMP280 measures atmospheric pressure in hectopascals (hPa).\n"
        )


# ---------------------------------------------------------------------------
# Test 2.5: Hardware Validation Passed (Bonus for early tests)
# ---------------------------------------------------------------------------
def test_hardware_markers_present():
    """
    Verify that hardware validation markers exist.

    Expected: Marker files from validate_pi.py execution

    Suggestion: Run validate_pi.py on your Raspberry Pi and push results.
    """
    markers_dir = REPO_ROOT / ".test_markers"

    if not markers_dir.exists():
        pytest.skip("No .test_markers/ directory - skipping hardware check")

    # Look for BMP280-specific markers
    bmp_markers = list(markers_dir.glob("*bmp*")) + list(markers_dir.glob("*i2c*"))

    # Also check the general test summary
    summary = markers_dir / "test_summary.txt"

    if summary.exists():
        content = summary.read_text().lower()
        if "bmp280" in content or "i2c" in content:
            return  # Pass - hardware was validated

    if not bmp_markers:
        pytest.fail(
            f"\n\n"
            f"Expected: BMP280/I2C hardware validation markers\n"
            f"Actual: No hardware-specific markers found\n\n"
            f"Suggestion: On your Raspberry Pi:\n"
            f"  1. Connect the BMP280 sensor to I2C pins\n"
            f"  2. Run: sudo i2cdetect -y 1\n"
            f"  3. Verify address 0x76 or 0x77 appears\n"
            f"  4. Run: python3 validate_pi.py\n"
            f"  5. Commit and push .test_markers/\n"
        )
