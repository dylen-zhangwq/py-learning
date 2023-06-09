from __future__ import annotations

import os
from pathlib import Path

about: dict[str, str] = {}
here = os.path.abspath(os.path.dirname(__file__))
parent_path = Path(here).parent


def test_version() -> None:
    path = os.path.join(parent_path, "src/py_learning", "version.py")
    print(parent_path)
    print(path)
    with open(os.path.join(parent_path, "src/py_learning", "version.py"), encoding="utf-8") as f:
        exec(f.read(), about)
    assert "__version__" in about
