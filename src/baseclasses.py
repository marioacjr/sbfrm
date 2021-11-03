from src.utils import GameListHandler
from src.utils import FileHandler
from src.utils import StringHandler


class Game:
    """Base class for game in system."""

    def __init__(self, filename=None):
        self.filename = filename

        self.path = None
        self.boxart = None
        self.image = None
        self.marquee = None
        self.thumbnail = None
        self.video = None

        self.name = None
        self.sortname = None
        self.description = None
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

    def str_append(self, game_var, text):
        ush = StringHandler()
        s = ''
        if game_var is not None:
            s += '\n    ' + ush.str_green(text)
            s += str(game_var)
        return s

    def __str__(self):
        ush = StringHandler()
        s = ush.str_blue('Filename: ')
        s += str(self.filename)

        s += self.str_append(self.path, 'Path: ')
        s += self.str_append(self.name, 'Name: ')
        s += self.str_append(self.desc, 'Description: ')
        s += self.str_append(self.sortname, 'Sortname: ')
        s += self.str_append(self.boxart, 'Boxart: ')
        s += self.str_append(self.image, 'Image: ')
        s += self.str_append(self.marquee, 'Marquee: ')
        s += self.str_append(self.thumbnail, 'Thumbnail: ')
        s += self.str_append(self.video, 'Video: ')
        s += self.str_append(self.releasedate, 'ReleaseDate: ')
        s += self.str_append(self.developer, 'Developer: ')
        s += self.str_append(self.publisher, 'Publisher: ')
        s += self.str_append(self.players, 'Players: ')
        s += self.str_append(self.core, 'Core: ')
        s += self.str_append(self.rating, 'Rating: ')
        s += self.str_append(self.playcount, 'Playcount: ')
        s += self.str_append(self.lastplayed, 'LastPlayed: ')
        s += self.str_append(self.md5, 'MD5: ')
        s += self.str_append(self.genre, 'Genre: ')

        return s + '\n'

    def load_media_from_gamelist(self, gamelist, systempath):
        xmlg = gamelist.get_game_by_filename(self.filename)
        if gamelist.game_tag_text_exist(xmlg, 'path'):
            if gamelist.filename_equals_gamepath(self.filename,
                                                 xmlg.find('path').text):

                fh = FileHandler()

                if gamelist.game_tag_text_exist(xmlg, 'path'):
                    path = fh.path([systempath, xmlg.find('path').text])
                    if fh.check_file(path):
                        self.path = xmlg.find('path').text

                if gamelist.game_tag_text_exist(xmlg, 'boxart'):
                    path = fh.path([systempath, xmlg.find('boxart').text])
                    if fh.check_file(path):
                        self.boxart = xmlg.find('boxart').text

                if gamelist.game_tag_text_exist(xmlg, 'image'):
                    path = fh.path([systempath, xmlg.find('image').text])
                    if fh.check_file(path):
                        self.image = xmlg.find('image').text

                if gamelist.game_tag_text_exist(xmlg, 'marquee'):
                    path = fh.path([systempath, xmlg.find('marquee').text])
                    if fh.check_file(path):
                        self.marquee = xmlg.find('marquee').text

                if gamelist.game_tag_text_exist(xmlg, 'thumbnail'):
                    path = fh.path([systempath, xmlg.find('thumbnail').text])
                    if fh.check_file(path):
                        self.thumbnail = xmlg.find('thumbnail').text

                if gamelist.game_tag_text_exist(xmlg, 'video'):
                    path = fh.path([systempath, xmlg.find('video').text])
                    if fh.check_file(path):
                        self.video = xmlg.find('video').text

    def load_info_from_gamelist(self, gamelist):
        xmlg = gamelist.get_game_by_filename(self.filename)
        if xmlg:
            if gamelist.game_tag_text_exist(xmlg, 'name'):
                self.name = xmlg.find('name').text

            if gamelist.game_tag_text_exist(xmlg, 'desc'):
                self.desc = xmlg.find('desc').text

            if gamelist.game_tag_text_exist(xmlg, 'sortname'):
                self.sortname = xmlg.find('sortname').text

            if gamelist.game_tag_text_exist(xmlg, 'description'):
                self.description = xmlg.find('description').text

            if gamelist.game_tag_text_exist(xmlg, 'releasedate'):
                self.releasedate = xmlg.find('releasedate').text

            if gamelist.game_tag_text_exist(xmlg, 'developer'):
                self.developer = xmlg.find('developer').text

            if gamelist.game_tag_text_exist(xmlg, 'publisher'):
                self.publisher = xmlg.find('publisher').text

            if gamelist.game_tag_text_exist(xmlg, 'genre'):
                self.genre = xmlg.find('genre').text

            if gamelist.game_tag_text_exist(xmlg, 'players'):
                self.players = xmlg.find('players').text

            if gamelist.game_tag_text_exist(xmlg, 'core'):
                self.core = xmlg.find('core').text

            if gamelist.game_tag_text_exist(xmlg, 'emulator'):
                self.emulator = xmlg.find('emulator').text

            if gamelist.game_tag_text_exist(xmlg, 'rating'):
                self.rating = xmlg.find('rating').text

            if gamelist.game_tag_text_exist(xmlg, 'playcount'):
                self.playcount = xmlg.find('playcount').text

            if gamelist.game_tag_text_exist(xmlg, 'lastplayed'):
                self.lastplayed = xmlg.find('lastplayed').text

            if gamelist.game_tag_text_exist(xmlg, 'md5'):
                self.md5 = xmlg.find('md5').text

    def load_from_gamelist(self, gamelist, systempath):
        self.load_media_from_gamelist(gamelist, systempath)
        self.load_info_from_gamelist(gamelist)


class System:
    """Base class for System in collection."""

    def __init__(self, parent_dir, dir_name,
                 boxarts=False, images=False, marquees=False,
                 thumbnails=False, videos=False):
        self.parent_dir = parent_dir
        self.dir_name = dir_name
        self.gamelist = None
        self.game = list()
        self.box_dir = boxarts
        self.img_dir = images
        self.marq_dir = marquees
        self.thumb_dir = thumbnails
        self.vid_dir = videos

    def get_path(self):
        fh = FileHandler()
        return fh.path([self.parent_dir, self.dir_name])

    def get_gamelist_path(self):
        fh = FileHandler()
        return fh.path([self.get_path(), 'gamelist.xml'])

    def get_file_list(self):
        fh = FileHandler()
        files = fh.get_files(self.get_path())
        files.sort()
        return files

    def load_gamelist(self):
        self.gamelist = GameListHandler()
        self.gamelist.set_tree(self.get_gamelist_path())

    def load_games(self):
        for file in self.get_file_list():
            game = Game(file)
            game.load_from_gamelist(self.gamelist, self.get_path())
            self.game.append(game)


class Collection:
    """Base class for System Collection."""

    def __init__(self):
        pass
