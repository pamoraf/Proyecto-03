import pytest
import os

RESOURCES_DIR = "./src/tests/resources"

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    original_permissions = {
        os.path.join(RESOURCES_DIR, "file_without_permission.bin"): os.stat(os.path.join(RESOURCES_DIR, "file_without_permission.bin")).st_mode,
        os.path.join(RESOURCES_DIR, "file_without_permission.txt"): os.stat(os.path.join(RESOURCES_DIR, "file_without_permission.txt")).st_mode,
        os.path.join(RESOURCES_DIR, "directory_without_permission"): os.stat(os.path.join(RESOURCES_DIR, "directory_without_permission")).st_mode,
    }
    os.chmod(os.path.join(RESOURCES_DIR, "file_without_permission.bin"), 0o000)
    os.chmod(os.path.join(RESOURCES_DIR, "file_without_permission.txt"), 0o000)
    os.chmod(os.path.join(RESOURCES_DIR, "directory_without_permission"), 0o555)
    yield
    os.chmod(os.path.join(RESOURCES_DIR, "file_without_permission.bin"), original_permissions[os.path.join(RESOURCES_DIR, "file_without_permission.bin")])
    os.chmod(os.path.join(RESOURCES_DIR, "file_without_permission.txt"), original_permissions[os.path.join(RESOURCES_DIR, "file_without_permission.txt")])
    os.chmod(os.path.join(RESOURCES_DIR, "directory_without_permission"), original_permissions[os.path.join(RESOURCES_DIR, "directory_without_permission")])

@pytest.fixture(scope="session")
def text_samples():
    text = []
    path = os.path.abspath(os.path.join(RESOURCES_DIR, "text"))
    print(path)
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as file:
            text.append(file.read()) 
    return text