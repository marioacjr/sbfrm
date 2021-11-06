import os
import shutil
import xml.etree.ElementTree as ET
import xml.dom.minidom as xdm
from datetime import datetime


class FileHandler:
    """Base class for File operations."""

    def __init__(self):
        super(FileHandler, self).__init__()

    def get_files(self, path):
        filelist = list()
        try:
            if os.path.isdir(path) and len(os.listdir(path)) > 0:
                files = [f for f in os.listdir(path)
                         if os.path.isfile(os.path.join(path, f))]
                for file in files:
                    if not self.excluded_file(file):
                        filelist.append(file)
        except Exception as e:
            print(e)
        filelist.sort()
        return filelist

    def excluded_file(self, file):
        for e in ['.xml', '.txt', '.state', '.nvmem', '.cfg', '.txt',
                  '.eeprom', '.srm']:
            if e in file:
                return True
        return False

    def ch_ext(self, filename, ext):
        return os.path.splitext(filename)[0] + ext

    def check_file(self, path, ext=False):
        if path is not None:
            if ext:
                path = self.ch_ext(self, path, ext)
            if os.path.isfile(path):
                return path
        return None

    def path(self, name_list):
        p = ''
        for n in name_list:
            p = os.path.join(p, n)
        return p


class GameListHandler:
    """Base class for GameListXml operations."""

    def __init__(self):
        super(GameListHandler, self).__init__()
        self.path = None
        self.tree = None

    def set_tree(self, path):
        tree = None
        if not os.path.isfile(path):
            s = '<?xml version="1.0" encoding="UTF-8"?><gameList></gameList>'
            f = open(path, "w")
            f.write(s)
            f.close()
        tree = ET.parse(path)
        self.tree = tree
        self.path = path

    def set_root(self, element):
        self.tree._setroot(element)

    def get_game_by_tag_text(self, tag, text):
        if self.tree is not None:
            for game in self.tree.getroot():
                if game.find(tag) is not None:
                    if game.find(tag).text is not None:
                        tag_text = game.find(tag).text
                        tag_text = tag_text.replace('./', '')
                        text = text.replace('./', '')
                        if tag == 'path':
                            tag_text = tag_text.split('(')[0]
                            text = text.split('(')[0]
                        if tag_text == text:
                            return game
        return False

    def get_game_by_filename(self, filename):
        return self.get_game_by_tag_text('path', filename)

    def game_tag_text_exist(self, game, tag):
        b = False
        if game and game.find(tag) is not None:
            if game.find(tag).text is not None:
                b = True
        return b

    def filename_equals_gamepath(self, filename, gamepath):
        filename = filename.replace('./', '')
        filename = os.path.splitext(filename)[0]
        gamepath = gamepath.replace('./', '')
        gamepath = os.path.splitext(gamepath)[0]
        return filename == gamepath

    def create_element(self, tag):
        return ET.Element(tag)

    def append_subelement(self, element, tag, text):
        subelement = ET.SubElement(element, tag)
        subelement.text = text
        # return element

    def pretty_print(self, root):
        """Description"""
        root = self.tree.getroot()
        xml_string = xdm.parseString(ET.tostring(root)).toprettyxml()
        # remove the weird newline issue
        xml_string = os.linesep.join([s for s in xml_string.splitlines()
                                      if s.strip()])
        return xml_string

    def save_xml(self, path):
        self.tree.write(path)
        xml_string = self.pretty_print(path)
        with open(path, "w", encoding="utf-8") as file_out:
            file_out.write(xml_string)

    def backup_xml(self, path):
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        bkp_path = path.replace('.xml', '_'+now+'.xml')
        shutil.copyfile(path, bkp_path)


class StringHandler():
    """docstring for Utils."""

    def __init__(self):
        super(StringHandler, self).__init__()
        self.reset = '\033[0m'
        self.bold = '\033[01m'
        self.disable = '\033[02m'
        self.underline = '\033[04m'
        self.reverse = '\033[07m'
        self.strikethrough = '\033[09m'
        self.invisible = '\033[08m'
        self.black = '\033[30m'
        self.red = '\033[31m'
        self.green = '\033[32m'
        self.orange = '\033[33m'
        self.blue = '\033[34m'
        self.purple = '\033[35m'
        self.cyan = '\033[36m'
        self.darkgrey = '\033[90m'
        self.yellow = '\033[93m'
        self.pink = '\033[95m'

        self.lightcyan = '\033[96m'
        self.lightgrey = '\033[37m'
        self.lightred = '\033[91m'
        self.lightgreen = '\033[92m'
        self.lightblue = '\033[94m'

        self.bgblack = '\033[40m'
        self.bgred = '\033[41m'
        self.bggreen = '\033[42m'
        self.bgorange = '\033[43m'
        self.bgblue = '\033[44m'
        self.bgpurple = '\033[45m'
        self.bgcyan = '\033[46m'
        self.bglightgrey = '\033[47m'

    def str_red(self, text):
        """docstring for Utils.print"""

        return self.red + text + self.reset

    def str_blue(self, text):
        """docstring for Utils.print"""

        return self.blue + text + self.reset

    def str_green(self, text):
        """docstring for Utils.print"""

        return self.green + text + self.reset
