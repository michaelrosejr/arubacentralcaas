import pathlib
import sys

import pytest

cwd = pathlib.Path.cwd()

# Add the project's root directory to the system path
sys.path.append(str(cwd.parent))

# This is optional, but you can add a lib directory
# To the system path for tests to be able to use
sys.path.append(str(cwd / "lib"))

pytest.main()
