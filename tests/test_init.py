from backup import _init
import unittest
import shutil
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
backup_config = os.path.join(current_dir, "..", "backup_config.json")

class TestBackupInit(unittest.TestCase):
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

    def test_init_creates_source_directory(self):
        # Arrange
        source = './source'
        destinations = []
        force = False
        add = False

        # Act
        _init(source, destinations, force, add)

        # Assert
        # Check if the source directory has been created
        self.assertTrue(os.path.exists(source))
    
    def test_init_creates_destination_directories(self):
        # Arrange
        source = './source'
        destinations = ['./destination1', './destination2']
        force = False
        add = False

        # Act
        _init(source, destinations, force, add)

        # Assert
        # Check if all destination directories have been created
        for dest in destinations:
            self.assertTrue(os.path.exists(dest))
    
    def test_init_overwrites_existing_destinations(self):
        # Arrange
        source = './source'
        destinations = ['./destination1', './destination2']
        new_destinations = ['./destination3', './destination4']
        force = True
        add = False

        # Act
        _init(source, destinations, force, add)
        # Overwrite the destinations with new ones
        _init(source, new_destinations, force, add)

        # Assert
        # Check if the destinations have been overwritten
        with open(backup_config) as config_file:
            paths = json.load(config_file)
        self.assertEqual(paths[source], new_destinations)
    
    def test_init_adds_destinations_without_overwriting(self):
       # Arrange
        source = './source'
        destinations = ['./destination1', './destination2']
        new_destinations = ['./destination3', './destination4']
        force = False
        add = True

        # Act
        _init(source, destinations, force, add)
        # Add the destinations with new ones
        _init(source, new_destinations, force, add)

        # Assert
        # Check if the destinations have been overwritten
        with open(backup_config) as config_file:
            paths = json.load(config_file)
        self.assertEqual(paths[source], destinations + new_destinations)

if __name__ == '__main__':
    unittest.main()