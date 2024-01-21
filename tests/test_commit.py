from backup import _init, _commit
from unittest.mock import patch
import unittest
import shutil
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
backup_config = os.path.join(current_dir, "..", "backup_config.json")

class TestBackupCommit(unittest.TestCase):
    def _clear(self):
        paths = ['./source', './source1', './destination1', './destination2', './destination3', './destination4']
        config_file = './backup_config.json'
    
        for path in paths:
            if os.path.exists(path):
                shutil.rmtree(path)
    
        if os.path.exists(config_file):
            with open(config_file, "w") as config_file:
                config_file.write("{}")
    def setUp(self):
        self._clear()
    def tearDown(self):
        self._clear()

    def test_commit_1source(self):
        source = './source'
        destinations = ['./destination1', './destination2']
        force = False
        add = False

        test_file = 'test.txt'
        test_file_contents = 'I\'m file content'

        _init(source, destinations, force, add)

        # create file in source
        with open(os.path.join(source, test_file), 'w') as f:
            f.write(test_file_contents)

        _commit(None)

        # check if file exists in destinations
        for dest in destinations:
            assert os.path.isfile(os.path.join(dest, test_file))
            with open(os.path.join(dest, test_file)) as f:
                assert f.read() == test_file_contents

    @patch('click.prompt', return_value='mocked_input')
    def test_commit_multisource(self, mock_input):
        source = './source'
        destinations = ['./destination1', './destination2']
        source1 = './source1'
        destinations1 = ['./destination3', './destination4']
        force = False
        add = False

        test_file = 'test.txt'
        test_file_contents = 'I\'m file content'

        _init(source, destinations, force, add)
        _init(source1, destinations1, force, add)

        # create file in source
        with open(os.path.join(source, test_file), 'w') as f:
            f.write(test_file_contents)

        _commit(None)

        # check if file exists in destinations
        for dest in destinations:
            assert os.path.isfile(os.path.join(dest, test_file))
            with open(os.path.join(dest, test_file)) as f:
                assert f.read() == test_file_contents


if __name__ == '__main__':
    unittest.main()                