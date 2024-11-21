import pytest
import os

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    
    original_permissions = {
        "resources/file_without_permission.bin": os.stat("resources/file_without_permission.bin").st_mode,
        "resources/file_without_permission.txt": os.stat("resources/file_without_permission.txt").st_mode,
        "resources/directory_without_permission": os.stat("resources/directory_without_permission").st_mode,
    }

    os.chmod("resources/file_without_permission.bin", 0o000)
    os.chmod("resources/file_without_permission.txt", 0o000)
    os.chmod("resources/directory_without_permission", 0o555)

    yield

    os.chmod("resources/file_without_permission.bin", original_permissions["resources/file_without_permission.bin"])
    os.chmod("resources/file_without_permission.txt", original_permissions["resources/file_without_permission.txt"])
    os.chmod("resources/directory_without_permission", original_permissions["resources/directory_without_permission"])