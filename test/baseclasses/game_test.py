"""Make Description."""

from os import remove
from os.path import isdir, isfile, islink, join
from shutil import rmtree
from unittest import TestCase
from src.game import Game


def delete(path):
    """
    Remove file or folder.

    Path could either be relative or absolute.
    """
    if isfile(path) or islink(path):
        remove(path)
    elif isdir(path):
        rmtree(path)


class GameTests(TestCase):
    """Make Description."""

    def test_load(self):
        """Make Description."""
        dest_system = join('test', 'roms_dest', 'system_one')
        delete(dest_system)
        game_name = "Game One (Japan)"
        system_name = "system_one"
        src_col = "test/roms_src"
        paths = {
            "path": join(src_col, system_name, game_name+".chd"),
            "boxart": None,
            "image": "downloaded_images",
            "marquee": "downloaded_wheels",
            "thumbnail": None,
            "video": "downloaded_videos"}
        media_dirs = {"image": None,
                      "marquee": None,
                      "video": None}
        game = Game()
        game.load(paths, join(src_col, system_name,
                  "/gamelist.xml"), media_dirs)
        print(game)
        print(paths)

        self.assertTrue(game.paths['path'] == "./" + game_name + ".chd")
