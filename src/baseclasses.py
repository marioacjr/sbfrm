import os
import xml.etree.ElementTree as ET


class Game:
    """Base class for game in system."""

    def __init__(self, filename=None):
        self.filename = filename
        self.path = None
        self.name = None
        self.sortname = None
        self.description = None

        self.boxart = None
        self.image = None
        self.marquee = None
        self.thumbnail = None
        self.video = None

        self.releasedate = None
        self.developer = None
        self.publisher = None
        self.genre = None
        self.players = None
        self.core = None
        self.emulator = None
        self.rating = None
        self.playcount = None
        self.lastplayed = None
        self.md5 = None

    def __str__(self):
        u = Utils()
        str = u.str_blue('Filename: ') + self.filename

        if self.path is not None:
            str += '\n\t' + u.str_green('Path: ') + self.path

        if self.name is not None:
            str += '\n\t' + u.str_green('Name: ') + self.name

        if self.sortname is not None:
            str += '\n\t' + u.str_green('Sortname: ') + self.sortname

        if self.boxart is not None:
            str += '\n\t' + u.str_green('Boxart: ') + self.boxart

        if self.image is not None:
            str += '\n\t' + u.str_green('Image: ') + self.image

        if self.marquee is not None:
            str += '\n\t' + u.str_green('Marquee: ') + self.marquee

        if self.thumbnail is not None:
            str += '\n\t' + u.str_green('Thumbnail: ') + self.thumbnail

        if self.video is not None:
            str += '\n\t' + u.str_green('Video: ') + self.video

        return str + '\n'

    def import_info(self, gamelist):
        game = gamelist.get_game_by_filename(self.filename)
        if game:
            self.path = './'+self.filename

            if game.find('name') is not None:
                self.name = game.find('name').text

            if game.find('sortname') is not None:
                self.sortname = game.find('sortname').text

            if game.find('desc') is not None:
                self.description = game.find('desc').text

            if game.find('boxart') is not None:
                self.boxart = game.find('boxart').text

            if game.find('image') is not None:
                self.image = game.find('image').text

            if game.find('marquee') is not None:
                self.marquee = game.find('marquee').text

            if game.find('thumbnail') is not None:
                self.thumbnail = game.find('thumbnail').text

            if game.find('video') is not None:
                self.video = game.find('video').text

            if game.find('releasedate') is not None:
                self.releasedate = game.find('releasedate').text

            if game.find('developer') is not None:
                self.developer = game.find('developer').text

            if game.find('publisher') is not None:
                self.publisher = game.find('publisher').text

            if game.find('genre') is not None:
                self.genre = game.find('genre').text

            if game.find('players') is not None:
                self.players = game.find('players').text

            if game.find('core') is not None:
                self.core = game.find('core').text

            if game.find('emulator') is not None:
                self.emulator = game.find('emulator').text

            if game.find('rating') is not None:
                self.rating = game.find('rating').text

            if game.find('playcount') is not None:
                self.playcount = game.find('playcount').text

            if game.find('lastplayed') is not None:
                self.lastplayed = game.find('lastplayed').text

            if game.find('md5') is not None:
                self.md5 = game.find('md5').text


class System:
    """Base class for System in collection."""

    def __init__(self, name, boxarts, images, marquees, thumbnails, videos):
        self.name = name
        self.game = list()
        self.boxarts = boxarts
        self.images = images
        self.marquees = marquees
        self.thumbnails = thumbnails
        self.videos = videos

    def save_to_dir(self, path):
        pass

    def read_from_dir(self, path):
        pass


class GameListHandler:
    """Base class for GameListXml operations."""

    def __init__(self):
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

    def get_game_by_tag_text(self, tag, text):
        if self.tree is not None:
            for game in self.tree.getroot():
                if game.find(tag) is not None:
                    if game.find(tag).text is not None:
                        tag_text = game.find(tag).text
                        tag_text = tag_text.replace('./', '')
                        text = tag_text.replace('./', '')
                        if tag == 'path':
                            tag_text = os.path.splitext(tag_text)[0]
                            text = os.path.splitext(text)[0]
                        if tag_text == text:
                            return game
        return False

    def get_game_by_filename(self, filename):
        return self.get_game_by_tag_text('path', filename)


class Utils():
    """docstring for Utils."""

    def __init__(self):
        super(Utils, self).__init__()
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
