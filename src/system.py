"""Make Description."""
import shutil
from datetime import datetime
from os import listdir, makedirs
from os.path import isfile, join, basename, splitext

import xml.etree.ElementTree as ET
import xml.dom.minidom as xdm

from src.terminalutils import get_progress_bar
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

def get_file_name(path):
    """Make Description."""
    return splitext(basename(path))[-2]


def get_file_extension(path):
    """Make Description."""
    return splitext(basename(path))[-1]

def dest_has_same_file(src_file_path, dest_dir):
    """Make Description."""
    src_filename = basename(src_file_path)
    dest_path = join(dest_dir, src_filename)
    return isfile(dest_path)


def same_filename_another_extension(src_file_path, dest_dir):
    """Make Description."""
    src_filename = get_file_name(basename(src_file_path))

    dest_names = [get_file_name(basename(f)) for f in listdir(dest_dir)]
    return src_filename in dest_names
        
def copy_file(src_path, src_filename, dest_path, dest_filename,
              dest_mdir=None, subsys=None, overwrite_file=False):
    """Make Description."""
    src_file = join(src_path, src_filename)
    if isfile(src_file):
        dest_path = join(dest_path)
        if dest_mdir is not None:
            dest_path = join(dest_path, dest_mdir)
        if subsys is not None:
            dest_path = join(dest_path, subsys)
        cond1 = not dest_has_same_file(src_file, dest_path)
        cond2 = not same_filename_another_extension(src_file, dest_path)
        if cond1 and cond2:
            shutil.copy(src_file, dest_path)
            return True
        elif isfile(join(dest_path, dest_filename)) and overwrite_file:
            dest_path = join(dest_path, dest_filename)
            shutil.copy(src_file, dest_path)
            return True
        
    return False


class System:
    """Base class for system."""

    def __init__(self, path):
        """Make Description."""
        self.path = path
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
            print(path, subsys)
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
            paths[key] = None
            if value is not None:
                for dir_name in value:
                    if subsys is not None:
                        dir_name = join(dir_name, subsys)
                    media_path = self.get_path(path, game_file, dir_name)
                    if media_path is not None:
                        paths[key] = media_path
                        break
        return paths

    def load(self, path, media_dirs, subsys=None):
        """Make Description."""
        gl_path = join(path, 'gamelist.xml')
        listgames = self.listgames(path, subsys=subsys)
        for game_file in listgames:
            paths = self.get_paths(path, game_file, media_dirs, subsys=subsys)
            game = Game()
            game.load(paths, gl_path, media_dirs, subsys=subsys)
            self.games.append(game)

    def load_info(self, gamelist_path):
        """Make Description."""
        for game in self.games:
            game.load_xml_info(gamelist_path)
            
    def make_sys_dirs(self, path, mdirs, subsys=None):
        """Make Description."""
        if subsys is None:
            makedirs(path, exist_ok=True)
        else:
            makedirs(join(path, subsys), exist_ok=True)

        for value in mdirs.values():
            mpath = join(path, value[0])
            if subsys is not None:
                mpath = join(mpath, subsys)
            makedirs(mpath, exist_ok=True)
            
    def copy_files_from_system(self, src_system, src_mdirs, media_dirs, subsys=None, verbose=False, overwrite_file=False,
                   gui=False):
        """Make Description."""        
        progress_base = len(src_system.games)
        if verbose:
            print_txt = '\n    Copying Files:'
            if subsys is not None:
                print_txt = print_txt.replace(':', ' (' + subsys + '):')
            print(print_txt, end='', flush=True)
        
        for gid, game in enumerate(src_system.games):
            if verbose:
                print(get_progress_bar(gid, progress_base), end='', flush=True)
                
            if gui:
                gui.write_event_value('-PROGRESS_GAMES-', [gid, progress_base])
                
            new_game = Game()
            copied = False
            for key, value in game.paths.items():
                if value is not None:
                    if key == 'path':
                        copied = copy_file(src_system.path, value.replace('./', ''),
                                  self.path, value.replace('./', ''),
                                  subsys=subsys, overwrite_file=overwrite_file)
                        if copied:
                            new_game.paths['path'] = value
                    elif key in src_mdirs:
                        dest_filename = get_file_name(game.paths['path'])
                        dest_filename += get_file_extension(basename(value))
                        copied = copy_file(src_system.path, value.replace('./', ''),
                                  self.path, dest_filename,
                                  dest_mdir=media_dirs[key][0],
                                  subsys=subsys,
                                  overwrite_file=overwrite_file)
                        if copied:
                            new_game.paths[key] = "./" + join(media_dirs[key][0], basename(value))
            if copied:
                self.games.append(new_game)

    def gen_report(self):
        """Make Description."""
        for game in self.games:
            for key, value in game.paths.items():
                if key != 'path' and value is None:
                    game_filename = basename(game.paths['path'])
                    self.reports['ausent_media'][key].append(game_filename)

            for key, value in game.info.items():
                if value is None:
                    game_filename = basename(game.paths['path'])
                    self.reports['ausent_info'][key].append(game_filename)

    def save_gamelist(self, path, provider=None):
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
