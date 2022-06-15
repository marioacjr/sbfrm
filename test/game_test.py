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

    def test_load_game_path(self):
        """Make Description."""
        game_filename = "Game One (Japan).chd"
        system_path = join("test", "roms_src", "system_one")
        gamelist_path = join(system_path, "/gamelist.xml")
        paths = {
            "path": join(system_path, game_filename)}
        media_dirs = {"image": "downloaded_images",
                      "marquee": "downloaded_wheels",
                      "thumbnail": "downloaded_thumbnails",
                      "video": "downloaded_videos"}
        game = Game()
        game.load(paths, gamelist_path, media_dirs)

        self.assertTrue(game.paths['path'] == "./" + game_filename)
