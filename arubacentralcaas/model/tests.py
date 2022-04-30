import json
import sys

sys.path.append("..")
from config import settings  # noqa: E402


class central_test:
    def __init__(self, function_called):
        self.function_called = function_called

    def command(self, **kwargs):
        test_file_name = f"test_{self.function_called}.json"
        print(f"\nUsing test file: [yellow]{test_file_name}[/yellow]")
        with open(f"{settings.test_dir}{test_file_name}", "r") as file:
            test_json = json.load(file)
        return test_json
