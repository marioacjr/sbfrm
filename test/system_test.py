"""Make Description."""

from os import remove
from os.path import isdir, isfile, islink, join
from shutil import rmtree
from unittest import TestCase
from src.system import System


def delete(path):
    """
    Remove file or folder.

    Path could either be relative or absolute.
    """
    if isfile(path) or islink(path):
        remove(path)
    elif isdir(path):
        rmtree(path)


class SystemTests(TestCase):
    """Make Description."""

    def test_load_system_path(self):
        """Make Description."""
        system_path = join("test", "roms_src", "system_a")
        src_system = System(system_path)
        src_system.load()

        roms = ['Game AA (Europe, Japan) (Demo).zip',
                'Game AA (Europe, Japan).zip',
                'Game AA (Japan).zip',
                'Game AA (USA, Europe, Japan).zip',
                'Game AA (USA).zip',
                'GAMEBBBB.zip',
                'GAMEBB.zip',
                'Game CC (USA) (Disc 1).zip',
                'Game CC (USA) (Disc 2).zip',
                'Game CC (USA) (Disc 3).zip'
                ]
        for game in src_system.games:
            self.assertTrue(game.paths['path'] in roms)
