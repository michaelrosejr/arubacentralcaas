import json

# sys.path.append("..")
# from arubacentralcaas.config import settings  # noqa: E402

# import sys


class central_test:
    def __init__(self, function_called):
        self.function_called = function_called

    def command(self, **kwargs):
        test_file_name = f"test_{self.function_called[0]}.json"
        test_dir = self.function_called[1]
        print(f"\nUsing test file: [yellow]{test_file_name}[/yellow]")
        with open(f"{test_dir}{test_file_name}", "r") as file:
            test_json = json.load(file)
        return test_json
