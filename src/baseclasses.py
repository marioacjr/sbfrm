from src.utils import GameListHandler
from src.utils import FileHandler
from src.utils import StringHandler


class Game:
    """Base class for game in system."""

    def __init__(self, filename=None):
        self.fn = filename

        self.path = None
        self.box = None
        self.img = None
        self.marq = None
        self.thumb = None
        self.vid = None

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
        s += str(self.fn)

        s += self.str_append(self.path, 'Path: ')
        s += self.str_append(self.name, 'Name: ')
        s += self.str_append(self.description, 'Description: ')
        s += self.str_append(self.sortname, 'Sortname: ')
        s += self.str_append(self.box, 'Boxart: ')
        s += self.str_append(self.img, 'Image: ')
        s += self.str_append(self.marq, 'Marquee: ')
        s += self.str_append(self.thumb, 'Thumbnail: ')
        s += self.str_append(self.vid, 'Video: ')
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

    def set_media_by_fn(self, sp, md, ext):
        if md:
            fh = FileHandler()
            f = fh.ch_ext(self.fn, ext)
            p = fh.path([sp, md, f])
            if fh.check_file(p):
                return fh.path(['./', md, f])
        return None

    def load_media_by_fn(self, sp, bd, id, md, td, vd):
        fh = FileHandler()
        p = fh.path([sp, self.fn])
        if fh.check_file(p):
            self.path = fh.path(['./', self.fn])
            self.box = self.set_media_by_fn(sp, bd, '.png')
            self.img = self.set_media_by_fn(sp, id, '.png')
            self.marq = self.set_media_by_fn(sp, md, '.png')
            self.thumb = self.set_media_by_fn(sp, td, '.png')
            self.vid = self.set_media_by_fn(sp, vd, '.mp4')

    def set_gl_media(self, gl, xmlg, tag, sp):
        fh = FileHandler()
        if gl.game_tag_text_exist(xmlg, tag):
            path = fh.path([sp, xmlg.find(tag).text])
            if fh.check_file(path):
                r = xmlg.find(tag).text
                if './' not in r[:2]:
                    r = './' + r
                return r

    def set_info(self, gl, xmlg, tag):
        if gl.game_tag_text_exist(xmlg, tag):
            return xmlg.find(tag).text

    def load_media_from_gamelist(self, gl, sp):
        xmlg = gl.get_game_by_filename(self.fn)
        if gl.game_tag_text_exist(xmlg, 'path'):
            if gl.filename_equals_gamepath(self.fn,
                                           xmlg.find('path').text):

                self.path = self.set_gl_media(gl, xmlg, 'path', sp)
                self.box = self.set_gl_media(gl, xmlg, 'boxart', sp)
                self.img = self.set_gl_media(gl, xmlg, 'image', sp)
                self.marq = self.set_gl_media(gl, xmlg, 'marquee', sp)
                self.thumb = self.set_gl_media(gl, xmlg, 'thumbnail', sp)
                self.vid = self.set_gl_media(gl, xmlg, 'video', sp)

    def load_info_from_gamelist(self, gl):
        xmlg = gl.get_game_by_filename(self.fn)
        if xmlg:
            self.name = self.set_info(gl, xmlg, 'name')
            self.description = self.set_info(gl, xmlg, 'desc')
            self.sortname = self.set_info(gl, xmlg, 'sortname')
            self.releasedate = self.set_info(gl, xmlg, 'releasedate')
            self.developer = self.set_info(gl, xmlg, 'developer')
            self.publisher = self.set_info(gl, xmlg, 'publisher')
            self.genre = self.set_info(gl, xmlg, 'genre')
            self.players = self.set_info(gl, xmlg, 'core')
            self.core = self.set_info(gl, xmlg, 'name')
            self.emulator = self.set_info(gl, xmlg, 'emulator')
            self.rating = self.set_info(gl, xmlg, 'rating')
            self.playcount = self.set_info(gl, xmlg, 'playcount')
            self.lastplayed = self.set_info(gl, xmlg, 'lastplayed')
            self.md5 = self.set_info(gl, xmlg, 'md5')

    def load_from_gamelist(self, gamelist, systempath):
        self.load_media_from_gamelist(gamelist, systempath)
        self.load_info_from_gamelist(gamelist)

    def gen_xml_element(self):
        glh = GameListHandler()
        e = glh.create_element('game')

        glh.append_subelement(e, 'path', self.path)
        glh.append_subelement(e, 'boxart', self.box)
        glh.append_subelement(e, 'image', self.img)
        glh.append_subelement(e, 'marquee', self.marq)
        glh.append_subelement(e, 'thumbnail', self.thumb)
        glh.append_subelement(e, 'video', self.vid)

        glh.append_subelement(e, 'name', self.name)
        glh.append_subelement(e, 'sortname', self.sortname)
        glh.append_subelement(e, 'desc', self.description)
        glh.append_subelement(e, 'releasedate', self.releasedate)
        glh.append_subelement(e, 'developer', self.developer)
        glh.append_subelement(e, 'publisher', self.publisher)
        glh.append_subelement(e, 'genre', self.genre)
        glh.append_subelement(e, 'players', self.players)
        glh.append_subelement(e, 'core', self.core)
        glh.append_subelement(e, 'emulator', self.emulator)
        glh.append_subelement(e, 'rating', self.rating)
        glh.append_subelement(e, 'lastplayed', self.lastplayed)
        glh.append_subelement(e, 'md5', self.md5)
        return e


class System:
    """Base class for System in collection."""

    def __init__(self, parent_dir, dir_name,
                 boxarts=False, images=False, marquees=False,
                 thumbnails=False, videos=False):
        self.parent_dir = parent_dir
        self.dir_name = dir_name
        self.gamelist = None
        self.games = list()
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
            sp = self.get_path()
            bp = self.box_dir
            ip = self.img_dir
            mp = self.marq_dir
            tp = self.thumb_dir
            vp = self.vid_dir
            game.load_media_by_fn(sp, bp, ip, mp, tp, vp)
            game.load_from_gamelist(self.gamelist, sp)
            self.games.append(game)

    def gen_xml_gamelist_from_games(self):
        root = self.gamelist.create_element('gameList')
        for g in self.games:
            e = g.gen_xml_element()
            root.append(e)
        self.gamelist.set_root(root)
        p = self.get_gamelist_path().replace('.xml', '2.xml')
        self.gamelist.save_xml(p)


class Collection:
    """Base class for System Collection."""

    def __init__(self):
        pass
