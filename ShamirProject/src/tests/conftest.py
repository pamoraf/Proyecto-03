from typing import List
import pytest
import os

RESOURCES_DIR = "./src/tests/resources"

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    files_and_dirs = {
        "file_without_permission.bin": 0o000,
        "file_without_permission.txt": 0o000,
        "directory_without_permission": 0o555
    }
    original_permissions = {}
    for name, mode in files_and_dirs.items():
        path = os.path.join(RESOURCES_DIR, name)
        if not os.path.exists(path):
            if "directory" in name:
                os.makedirs(path)
            else:
                with open(path, 'w') as f:
                    f.write("")
        original_permissions[path] = os.stat(path).st_mode
        os.chmod(path, mode)
    yield
    for path, mode in original_permissions.items():
        os.chmod(path, mode)

@pytest.fixture(scope="session")
def text_samples() -> List[str]:
    text = []
    path = os.path.abspath(os.path.join(RESOURCES_DIR, "text"))
    print(path)
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as file:
            text.append(file.read()) 
    return text