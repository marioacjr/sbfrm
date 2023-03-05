"""Make Description."""

import xml.etree.ElementTree as ET
from os.path import isfile, basename, dirname, join, splitext

from src.fileutils import configs, get_file_name
from src.terminalutils import text_colored as tc


def get_xml_tag_text(game_xml, tag):
    """Make Description."""
    tag_text = None
    if game_xml.find(tag) is not None:
        if game_xml.find(tag).text is not None:
            tag_text = game_xml.find(tag).text
    return tag_text


class Game:
    """Base class for game."""

    def __init__(self):
        """Make Description."""
        self.paths = {
            "path": None,
            "boxart": None,
            "image": None,
            "marquee": None,
            "thumbnail": None,
            "video": None}
        self.info = {
            "name": None,
            "sortname": None,
            "desc": None,
            "releasedate": None,
            "developer": None,
            "publisher": None,
            "genreid": None,
            "genre": None,
            "players": None,
            "core": None,
            "emulator": None,
            "rating": None,
            "playcount": None,
            "lastplayed": None,
            "md5": None,
            "adult": None}

    def __str__(self):
        """Make Description."""
        sout = tc('green', f"  {self.info['name']}\n")
        sout += tc('green', '    Files:\n')
        for key, value in self.paths.items():
            sout += "      " + tc('green', key) + ": " + str(value) + "\n"
        sout += tc('green', '    Info:\n')
        for key, value in self.info.items():
            sout += "      " + tc('green', key) + ": " + str(value) + "\n"
        return sout

    def load(self, paths, gamelist_path):
        """Make Description."""
        self.set_paths(paths)
        self.load_xml_paths(gamelist_path)
        self.load_xml_info(gamelist_path)

    def set_paths(self, paths):
        """Make Description."""
        for key, value in paths.items():
            if value is not None and isfile(value):
                if key == 'path':
                    path = basename(value)
                    self.paths[key] = "./" + path
                else:
                    if key in configs["dest_media_dirs_names"].keys():
                        path = basename(value)
                        dir_name = dirname(value)
                        dir_name = basename(dir_name)
                        if isfile(value):
                            self.paths[key] = "./" + join(dir_name, path)

    def load_xml_paths(self, gamelist_path):
        """Make Description."""
        games_xml = self.get_games_xml(gamelist_path)
        for game_xml in games_xml:
            tags = self.paths.keys()
            for tag in tags:
                tag_text = get_xml_tag_text(game_xml, tag)
                if tag_text is not None and tag != 'path':
                    path = basename(dirname(tag_text))
                    path = join(path, basename(tag_text))
                    if isfile(join(dirname(gamelist_path), path)):
                        self.paths[tag] = './' + path

    def load_xml_info(self, gamelist_path):
        """Make Description."""
        games_xml = self.get_games_xml(gamelist_path)
        for game_xml in games_xml:
            tags = self.info.keys()
            for tag in tags:
                if game_xml.find(tag) is not None:
                    if game_xml.find(tag).text is not None:
                        self.info[tag] = game_xml.find(tag).text

    def get_games_xml(self, gamelist_path):
        """Make Description."""
        games_xml = []
        if isfile(gamelist_path):
            tree = ET.parse(gamelist_path)
            for game in tree.getroot():
                if game.find('path') is not None:
                    if game.find('path').text is not None:
                        # name_a = splitext(game.find('path').text)[0]
                        # name_b = splitext(self.paths['path'])[0]
                        name_a = get_file_name(game.find('path').text)
                        name_b = get_file_name(self.paths['path'])
                        if name_a == name_b:
                            games_xml.append(game)
        return games_xml

    def gen_game_xml(self):
        """Make Description."""
        game_xml = ET.Element('game')
        for key, value in self.paths.items():
            subelement = ET.SubElement(game_xml, key)
            if value is not None:
                while "./" in value:
                    value = value.replace("./", "")
                value = "./"+value
            subelement.text = value
            
        for key, value in self.info.items():
            subelement = ET.SubElement(game_xml, key)
            subelement.text = value
        return game_xml
