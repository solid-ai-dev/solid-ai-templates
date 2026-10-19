"""The smoke checks, one module per family; tests/run_smoke.py runs them.
"""

import os
import sys

# The checks read the manifest the way the resolver does, so tools/ is
# importable before any family module loads.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "tools"))
