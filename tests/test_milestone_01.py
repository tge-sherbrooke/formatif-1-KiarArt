#!/usr/bin/env python3
"""
Milestone 1: Environment Setup (25 points)
==========================================

This milestone verifies that the student has:
1. Created a valid test_bmp280.py script
2. Configured Python dependencies correctly
3. Run local tests on the Raspberry Pi

These tests run in GitHub Actions (no hardware access).
Hardware validation is done locally via validate_pi.py.
"""

import os
import ast
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
    # Fallback to parent
    return current


REPO_ROOT = get_repo_root()


# ---------------------------------------------------------------------------
# Test 1.1: Script Exists (5 points)
# ---------------------------------------------------------------------------
def test_bmp280_script_exists():
    """
    Verify that test_bmp280.py exists in the repository.

    Expected: test_bmp280.py file present

    Suggestion: Create a file named test_bmp280.py at the repository root.
    Copy the template from modele/test_bmp280.py if available.
    """
    script_path = REPO_ROOT / "test_bmp280.py"

    assert script_path.exists(), (
        f"\n\n"
        f"Expected: test_bmp280.py file in repository root\n"
        f"Actual: File not found at {script_path}\n\n"
        f"Suggestion: Create test_bmp280.py with your BMP280 sensor reading code.\n"
        f"You can start from modele/test_bmp280.py if you haven't already.\n"
    )


# ---------------------------------------------------------------------------
# Test 1.2: Script Has Valid Python Syntax (5 points)
# ---------------------------------------------------------------------------
def test_bmp280_script_syntax():
    """
    Verify that test_bmp280.py has valid Python syntax.

    Expected: Python code that compiles without SyntaxError

    Suggestion: Check for typos, missing colons, unbalanced parentheses.
    Run 'python3 -m py_compile test_bmp280.py' locally to find errors.
    """
    script_path = REPO_ROOT / "test_bmp280.py"

    if not script_path.exists():
        pytest.skip("test_bmp280.py not found - skipping syntax check")

    content = script_path.read_text()

    try:
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(
            f"\n\n"
            f"Expected: Valid Python syntax\n"
            f"Actual: SyntaxError on line {e.lineno}: {e.msg}\n\n"
            f"Suggestion: Check line {e.lineno} for:\n"
            f"  - Missing colons after 'if', 'for', 'def', 'class'\n"
            f"  - Unbalanced parentheses, brackets, or quotes\n"
            f"  - Incorrect indentation\n"
            f"\n"
            f"Run locally: python3 -m py_compile test_bmp280.py\n"
        )


# ---------------------------------------------------------------------------
# Test 1.3: Required Imports Present (5 points)
# ---------------------------------------------------------------------------
def test_bmp280_imports():
    """
    Verify that test_bmp280.py imports the required libraries.

    Expected: 'import board' and 'adafruit_bmp280' in the code

    Suggestion: Add these imports at the top of your script:
        import board
        import adafruit_bmp280
    """
    script_path = REPO_ROOT / "test_bmp280.py"

    if not script_path.exists():
        pytest.skip("test_bmp280.py not found - skipping import check")

    content = script_path.read_text()

    missing_imports = []

    if "import board" not in content and "from board" not in content:
        missing_imports.append("board")

    if "adafruit_bmp280" not in content:
        missing_imports.append("adafruit_bmp280")

    if missing_imports:
        pytest.fail(
            f"\n\n"
            f"Expected: Required imports for BMP280 sensor\n"
            f"Actual: Missing imports: {', '.join(missing_imports)}\n\n"
            f"Suggestion: Add these imports at the top of test_bmp280.py:\n"
            f"  import board\n"
            f"  import adafruit_bmp280\n"
        )


# ---------------------------------------------------------------------------
# Test 1.4: UV Dependencies Configured (5 points)
# ---------------------------------------------------------------------------
def test_uv_dependencies():
    """
    Verify that UV inline dependencies are configured in the script.

    Expected: UV script metadata block with dependencies

    Suggestion: Add this block at the top of test_bmp280.py (after shebang):
        # /// script
        # requires-python = ">=3.9"
        # dependencies = ["adafruit-circuitpython-bmp280", "adafruit-blinka"]
        # ///
    """
    script_path = REPO_ROOT / "test_bmp280.py"

    if not script_path.exists():
        pytest.skip("test_bmp280.py not found - skipping UV check")

    content = script_path.read_text()

    has_uv_block = "# /// script" in content or "dependencies" in content
    has_bmp280_dep = "adafruit-circuitpython-bmp280" in content or "adafruit_bmp280" in content

    if not has_uv_block:
        pytest.fail(
            f"\n\n"
            f"Expected: UV inline script metadata for dependency management\n"
            f"Actual: No UV script block found\n\n"
            f"Suggestion: Add this block at the top of your script:\n"
            f"  # /// script\n"
            f"  # requires-python = \">=3.9\"\n"
            f"  # dependencies = [\"adafruit-circuitpython-bmp280\", \"adafruit-blinka\"]\n"
            f"  # ///\n"
            f"\n"
            f"This allows running with: uv run test_bmp280.py\n"
        )


# ---------------------------------------------------------------------------
# Test 1.5: Local Tests Executed (5 points)
# ---------------------------------------------------------------------------
def test_local_tests_executed():
    """
    Verify that local tests were run on the Raspberry Pi.

    Expected: .test_markers/ directory with test results

    Suggestion: On your Raspberry Pi, run:
        python3 validate_pi.py
    Then commit and push the .test_markers/ folder.
    """
    markers_dir = REPO_ROOT / ".test_markers"

    if not markers_dir.exists():
        pytest.fail(
            f"\n\n"
            f"Expected: .test_markers/ directory with local test results\n"
            f"Actual: Directory not found\n\n"
            f"Suggestion: Run local hardware validation on your Raspberry Pi:\n"
            f"  python3 validate_pi.py\n"
            f"\n"
            f"Then add the markers to git:\n"
            f"  git add .test_markers/\n"
            f"  git commit -m \"feat: validation locale executee\"\n"
            f"  git push\n"
        )

    # Check for at least one marker file
    marker_files = list(markers_dir.glob("*.txt"))

    if not marker_files:
        pytest.fail(
            f"\n\n"
            f"Expected: At least one marker file in .test_markers/\n"
            f"Actual: Directory exists but is empty\n\n"
            f"Suggestion: Run local tests again:\n"
            f"  python3 validate_pi.py\n"
            f"Make sure the script completes successfully.\n"
        )
