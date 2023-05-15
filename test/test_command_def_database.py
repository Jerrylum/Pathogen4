import sys

sys.path.insert(1, "./")
#
import json
import unittest

from command_creation.command_definition_database import CommandDefinitionDatabase


class TestCommandDefinitionDatabase(unittest.TestCase):
    def test_import_and_export(self):
        database = CommandDefinitionDatabase()

        lib_file = database.exportToJson()

        # with open("command_library.json", "w") as file:
        #     json.dump(lib_file, file, indent = 4)

        # lib_file_2 = None
        # with open("command_library.json", "r") as file:
        #     lib_file_2 = json.load(file)

        # database.importFromJson(lib_file_2)
        database.importFromJson(lib_file)

        lib_file_3 = database.exportToJson()

        self.assertEqual(json.dumps(lib_file), json.dumps(lib_file_3))


if __name__ == "__main__":
    unittest.main()
