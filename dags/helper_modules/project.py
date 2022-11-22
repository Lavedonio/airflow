"""
    Project-related helper functions.
"""
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SCRIPTS_PATHS = {
    'bash': PROJECT_ROOT / 'scripts' / 'bash',
    'python': PROJECT_ROOT / 'scripts' / 'python',
    'sql': PROJECT_ROOT / 'scripts' / 'sql',
}
