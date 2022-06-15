"""Make Description."""

from datetime import datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom as xdm

from os import listdir, makedirs
from os.path import isfile, join, basename, splitext
from src.terminalutils import text_colored as tc
from src.game import Game


def list_files(path):
    """Make Description."""
    return [f for f in listdir(path) if isfile(join(path, f))]


def file_name(path):
    """Make Description."""
    return splitext(basename(path))[-2]


def file_extension(path):
    """Make Description."""
    return splitext(basename(path))[-1]


def backup_gamelist(path):
    """Make Description."""
    tree = ET.parse(path)
    root = tree.getroot()
    dt_now = '_' + str(datetime.now().strftime("%Y%m%d%H%M%S"))
    bkp_path = path.replace('.xml', dt_now+'.xml')
    with open(bkp_path, "w", encoding="utf-8") as file_out:
        prettyxml = xdm.parseString(ET.tostring(root)).toprettyxml()
        file_out.write(prettyxml)


class System:
    """Base class for system."""

    def __init__(self):
        """Make Description."""
        self.games = []
        self.excluded_extensions = ['.xml', '.txt', '.state', '.nvmem', '.cfg',
                                    '.txt', '.eeprom', '.srm', '.lst', '.keep',
                                    '.sh']
        self.media_extensions = ['.png', '.jpg', '.jpeg', '.mp4', '.ogg']
        self.reports = {
            "ausent_media": {
                'boxart': [],
                "image": [],
                "marquee": [],
                "thumbnail": [],
                "video": []
            },
            "ausent_info": {
                "name": [],
                "sortname": [],
                "desc": [],
                "releasedate": [],
                "developer": [],
                "publisher": [],
                "genreid": [],
                "genre": [],
                "players": [],
                "core": [],
                "emulator": [],
                "rating": [],
                "playcount": [],
                "lastplayed": [],
                "md5": [],
                "adult": []
            },
        }

    def __str__(self):
        """Make Description."""
        sout = tc('green', "Games:")
        for game in self.games:
            sout += str(game)
        return sout

    def excluded_files(self, filename):
        """Make Description."""
        for ext in self.excluded_extensions:
            if ext in filename:
                return True
        return False

    def listgames(self, path, subsys=None):
        """Make Description."""
        if subsys is not None:
            path = join(path, subsys)
        files = [f for f in listdir(path) if isfile(join(path, f))]
        files = [f for f in files if not self.excluded_files(f)]
        return files

    def get_path(self, path, game_file, media_dir):
        """Make Description."""
        for ext in self.media_extensions:
            game_file = join(path, media_dir, file_name(game_file) + ext)
            if isfile(game_file):
                return join(game_file)
        return None

    def get_paths(self, path, game_file, media_dirs, subsys=None):
        """Make Description."""
        paths = {"path": join(path, game_file)}
        if subsys is not None:
            paths = {"path": join(path, subsys, game_file)}
        for key, value in media_dirs.items():
            if value is not None:
                if subsys is not None:
                    value = join(value, subsys)
                paths[key] = self.get_path(path, game_file, value)
        return paths

    def load(self, path, media_dirs, subsys=None):
        """Make Description."""
        gl_path = join(path, 'gamelist.xml')
        for game_file in self.listgames(path, subsys=subsys):
            paths = self.get_paths(path, game_file, media_dirs, subsys=subsys)
            game = Game()
            game.load(paths, gl_path, media_dirs, subsys=subsys)
            self.games.append(game)
            for key, value in game.paths.items():
                if key != 'path' and value is None:
                    game_filename = basename(game.paths['path'])
                    self.reports['ausent_media'][key].append(game_filename)

    def load_info(self, gamelist_path):
        """Make Description."""
        for game in self.games:
            game.load_xml_info(gamelist_path)

    def gen_report(self):
        """Make Description."""
        for game in self.games:
            for key, value in game.info.items():
                if value is None:
                    game_filename = basename(game.paths['path'])
                    self.reports['ausent_info'][key].append(game_filename)

    def set_gamelist(self, path, provider=None):
        """Make Description."""
        root = None
        if isfile(path):
            backup_gamelist(path)

        srt_xml = '<?xml version="1.0" encoding="UTF-8"?><gameList></gameList>'
        root = ET.fromstring(srt_xml)
        if provider is not None:
            provider_xml = ET.Element('provider')
            for key, value in provider.items():
                subelement = ET.SubElement(provider_xml, key)
                subelement.text = value
            root.append(provider_xml)

        for game in self.games:
            game_xml = game.gen_game_xml()
            root.append(game_xml)
        with open(path, "w", encoding="utf-8") as file_out:
            file_out.write(xdm.parseString(ET.tostring(root)).toprettyxml())

    def save_reports(self, path):
        """Make Description."""
        path = join(path, 'sbfrm_reports')
        makedirs(path, exist_ok=True)
        for key, media in self.reports['ausent_media'].items():
            if key != 'path':
                report_path = join(path, 'games_wihout_')
                report_path += key + '.txt'
                report = ''
                for game_name in media:
                    report += game_name + '\n'
                with open(report_path, "w", encoding="utf-8") as file_out:
                    file_out.write(report)

        for key, media in self.reports['ausent_info'].items():
            if key != 'path':
                report_path = join(path, 'games_wihout_info_')
                report_path += key + '.txt'
                report = ''
                for game_name in media:
                    report += game_name + '\n'
                with open(report_path, "w", encoding="utf-8") as file_out:
                    file_out.write(report)
