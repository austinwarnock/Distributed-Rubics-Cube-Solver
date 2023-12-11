import os
import filecmp
import pytest

def get_files(folder):
    return [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]

@pytest.fixture
def folders():
    return {
        'folder1': 'correct_moves',
        'folder2': 'tests',
    }

def test_files_match_content(folders):
    folder1 = folders['folder1']
    folder2 = folders['folder2']

    files1 = get_files(folder1)
    files2 = get_files(folder2)

    # Ensure that the list of files in both folders is the same
    assert set(files1) == set(files2), "Files in folders are not the same"

    failed_attempts = []

    for file in files1:
        file_path1 = os.path.join(folder1, file)
        file_path2 = os.path.join(folder2, file)

        # Ensure that the content of the files is the same
        if not filecmp.cmp(file_path1, file_path2):
            failed_attempts.append(file)
            print(f"Content of {file} does not match")

    assert not failed_attempts, f"Failures: {failed_attempts}"
