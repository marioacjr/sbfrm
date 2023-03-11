"""Make Description."""
from os import listdir, makedirs
from os.path import isfile, join, basename, isdir

import xml.etree.ElementTree as ET
import xml.dom.minidom as xdm

from src.terminalutils import print_verbose_progressbar, print_verbose_msg
from src.terminalutils import text_colored as tc
from src.fileutils import configs, file_name, backup_gamelist
from src.fileutils import make_sys_dirs, get_config_item_list, remove_file
from src.fileutils import find_same_games, merge_file, get_backup_dir
from src.fileutils import same_game_another_disc
from src.game import Game

from time import sleep


class System:
    """Base class for system."""

    def __init__(self, path, stop, gui=False):
        """Make Description."""
        self.path = path

        self.games = []
        self.gui = gui

        self.cache = {
            "game_name": [],
            "game_path": []
        }

        self.removed_games = []

        self.stop = stop

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
            "games_removed": []
        }

    def __str__(self):
        """Make Description."""
        sout = tc('green', "Games:")
        for game in self.games:
            sout += str(game)
        return sout

    def make_cache_text(self, text):
        """Make Description."""
        cache_text = file_name(text).replace(" ", "")
        cache_text = cache_text.replace("-", "")
        cache_text = cache_text.replace(":", "")
        cache_text = cache_text.lower()
        return cache_text

    def read_game_xml_metadata(self, game_xml, tag):
        """Make Description."""
        if game_xml.find(tag) is not None:
            if game_xml.find(tag).text is not None:
                return game_xml.find(tag).text
        return False

    def load_game_metadata(self, game_metadata, game_xml, cache_key):
        """Make Description."""
        for key in game_metadata.keys():
            text = self.read_game_xml_metadata(game_xml, key)
            if text:
                path = text.replace("./", "")
                if configs['overwrite_gamelist_info'] or game_metadata[key] == None:
                    game_metadata[key] = path

    def add_to_cache(self, game):
        """Make Description."""
        if game.paths['path'] is not None:
            self.cache['game_path'].append(game.paths['path'])
        if game.info['name'] is not None:
            self.cache["game_name"].append(game.info['name'])

    def check_if_in_cache(self, game):
        """Make Description."""
        result = False
        if game.paths['path'] is not None:
            result = result or game.paths['path'] in self.cache['game_path']
        if game.info['name'] is not None:
            result = result or game.info['name'] in self.cache['game_name']

        return result

    def load(self):
        """Make Description."""
        if not isdir(self.path):
            make_sys_dirs(self.path)
            return

        self.load_from_gamelist()
        self.load_from_filegames()

    def load_from_gamelist(self):
        """Make Description."""
        print_verbose_msg(
            'green', '\n            Loading GameListXml:', gui=self.gui)

        gamelist_path = join(self.path, 'gamelist.xml')

        if isfile(gamelist_path):
            tree = ET.parse(gamelist_path)
            progress_base = len(tree.getroot())
            for progress_id, game_xml in enumerate(tree.getroot()):
                print_verbose_progressbar(
                    progress_id, progress_base, gui=self.gui)
                if self.stop:
                    break

                path = self.read_game_xml_metadata(game_xml, 'path')
                if path:
                    if isfile(join(self.path, path.replace("./", ""))):
                        game = Game()
                        self.load_game_metadata(game.paths, game_xml, 'path')
                        self.load_game_metadata(game.info, game_xml, 'name')
                        self.games.append(game)

    def load_from_filegames(self):
        """Make Description."""
        print_verbose_msg(
            'green', '\n            Loading GameFiles:  ', gui=self.gui)

        listgamefiles = self.listgamesfiles()
        progress_base = len(listgamefiles)
        for progress_id, gamefile_path in enumerate(listgamefiles):
            print_verbose_progressbar(progress_id, progress_base, gui=self.gui)
            if self.stop:
                break

            game = Game()
            for key in game.paths.keys():
                if self.stop:
                    break
                if key == 'path':
                    game.paths[key] = gamefile_path
                else:
                    for src_media_dir in configs["src_media_dirs_list"][key]:
                        if self.stop:
                            break
                        for media_extension in self.media_extensions:
                            if self.stop:
                                break
                            media_path = join(self.path, src_media_dir)
                            media_path = join(media_path, file_name(
                                gamefile_path)+media_extension)
                            if isfile(media_path):
                                media_path = join(src_media_dir, file_name(
                                    gamefile_path)+media_extension)
                                game.paths[key] = media_path
                            else:
                                suffixes = {
                                    "boxart": "-boxart",
                                    "image": "-image",
                                    "marquee": "-marquee",
                                    "thumbnail": "-thumb",
                                    "video": "-video"
                                }
                                media_path = join(self.path, src_media_dir)
                                media_path = join(media_path, file_name(
                                    gamefile_path)+suffixes[key]+media_extension)
                                if isfile(media_path):
                                    media_path = join(src_media_dir, file_name(
                                        gamefile_path)+suffixes[key]+media_extension)
                                    game.paths[key] = media_path

            game_src_id = False
            for game_id, game_src in enumerate(self.games):
                if self.stop:
                    break
                if game_src.paths['path'] == game.paths['path']:
                    game_src_id = game_id
                    break

            for key in self.games[game_src_id].paths.keys():
                if self.stop:
                    break
                self.games[game_src_id].paths[key] = game.paths[key]

    def excluded_files(self, filename):
        """Make Description."""
        for ext in self.excluded_extensions:
            if ext in filename:
                return True
        return False

    def listgamesfiles(self):
        """Make Description."""
        path = self.path

        files = [f for f in listdir(path) if isfile(join(path, f))]
        files = [f for f in files if not self.excluded_files(f)]

        return files

    def load_info(self, gamelist_path):
        """Make Description."""
        for game in self.games:
            game.load_xml_info(gamelist_path)

    def remove_games_by_filename(self, filename_list, backup_path):
        """Make Description."""
        gamenames_to_remove = []
        for game_id, game in enumerate(self.games):
            if self.stop:
                break
            for filename in filename_list:
                if self.stop:
                    break
                path = "./" + filename
                if game.paths['path'] == path:
                    for key in game.paths.keys():
                        if self.stop:
                            break
                        if game.paths[key] is not None:
                            path = join(
                                self.path, game.paths[key].replace("./", ""))
                            dest_path = join(
                                backup_path, basename(game.paths[key]))
                            if key != 'path':
                                dest_path = join(
                                    backup_path, configs['dest_media_dirs_names'][key], basename(game.paths[key]))
                            remove_file(path, dest_path)
                            gamenames_to_remove.append(game_id)
                    games_removed = basename(game.paths['path'])
                    if games_removed not in self.reports['games_removed']:
                        self.reports['games_removed'].append(games_removed)

        new_games = []
        for game_id, game in enumerate(self.games):
            if self.stop:
                break
            if game_id not in gamenames_to_remove:
                new_games.append(game)
            else:
                self.removed_games.append(game)

        self.games = new_games

    def backup_removed_games_metadata(self):
        """Make Description."""
        print_verbose_msg(
            "green", '\n            Save Removed GameListXml Metadata:', gui=self.gui)

        dest_path = get_backup_dir(self.path)
        if isfile(dest_path):
            backup_gamelist(dest_path)

        srt_xml = '<?xml version="1.0" encoding="UTF-8"?><gameList></gameList>'
        root = ET.fromstring(srt_xml)

        progress_base = len(self.removed_games)
        for progress_id, game in enumerate(self.removed_games):
            print_verbose_progressbar(progress_id, progress_base, gui=self.gui)
            if self.stop:
                break
            game_xml = game.gen_game_xml()
            root.append(game_xml)

        path = join(dest_path, 'gamelist.xml')

        with open(path, "w", encoding="utf-8") as file_out:
            file_out.write(xdm.parseString(ET.tostring(root)).toprettyxml())

    def remove_games_clones(self):
        """Make Description."""
        games_to_remove = []
        names = []
        paths = []
        for game in self.games:
            if self.stop:
                break
            if game.info['name'] is not None:
                name = game.info['name']

                cond = name in names
                if cond:
                    path_id = names.index(name)
                    if not same_game_another_disc(game.paths['path'], paths[path_id]):
                        games_to_remove.append(basename(game.paths['path']))
                else:
                    names.append(name)
                    paths.append(basename(game.paths['path']))

        for game_to_remove in games_to_remove:
            if self.stop:
                break
            to_remove_item_list = get_config_item_list(game_to_remove)
            to_remove_priorities_list = [configs['region_order'].index(
                x) for x in to_remove_item_list if x in configs['region_order']]
            dest_same_names = find_same_games(self.path, game_to_remove)
            for dest_same_name in dest_same_names:
                if self.stop:
                    break
                dest_config_item_list = get_config_item_list(dest_same_name)
                dest_priorities_list = [configs['region_order'].index(
                    x) for x in dest_config_item_list if x in configs['region_order']]
                if len(to_remove_priorities_list) > 0 and len(dest_priorities_list) > 0:
                    cond = len(to_remove_priorities_list) < len(
                        dest_priorities_list)
                    cond = cond and to_remove_priorities_list[0] <= dest_priorities_list[0]
                    if cond:
                        games_to_remove.remove(game_to_remove)
                        games_to_remove.append(dest_same_name)

        self.remove_games_by_filename(
            games_to_remove, get_backup_dir(self.path))

    def copy_files_from_system(self, src_system):
        """Make Description."""
        print_verbose_msg("green", '\n            Copying:', gui=self.gui)

        backup_path = get_backup_dir(self.path)
        make_sys_dirs(backup_path)

        progress_base = len(src_system.games)
        for src_game_id, game in enumerate(src_system.games):
            print_verbose_progressbar(src_game_id, progress_base, gui=self.gui)
            if self.stop:
                break

            copy_cond = True

            src_game_name = basename(game.paths['path'])
            src_config_item_list = get_config_item_list(src_game_name)
            src_priorities_list = [configs['region_order'].index(
                x) for x in src_config_item_list if x in configs['region_order']]

            dest_same_names = find_same_games(self.path, src_game_name)
            for dest_same_name in dest_same_names:
                if self.stop:
                    break
                dest_config_item_list = get_config_item_list(dest_same_name)
                dest_priorities_list = [configs['region_order'].index(
                    x) for x in dest_config_item_list if x in configs['region_order']]

                if len(src_priorities_list) > 0 and len(dest_priorities_list) > 0:
                    cond = len(src_priorities_list) == 1
                    cond = cond and src_priorities_list[0] < dest_priorities_list[0]
                    if cond:
                        self.remove_games_by_filename(
                            [dest_same_name], backup_path)

                cond = len(src_priorities_list) > 1
                cond = cond and len(dest_priorities_list) == 1
                cond = cond and dest_priorities_list[0] <= min(
                    src_priorities_list)
                if cond:
                    copy_cond = False

                if src_game_name.__eq__(dest_same_name):
                    copy_cond = False

                cond = len(src_priorities_list) == 1
                cond = cond and len(dest_priorities_list) == 1
                cond = cond and dest_priorities_list[0] <= src_priorities_list[0]
                if cond:
                    copy_cond = False

            if any(x in src_config_item_list for x in configs['removed_devcomm_status']):
                copy_cond = False

            if copy_cond:
                new_game = Game()
                for key in new_game.paths.keys():
                    if self.stop:
                        break
                    if game.paths[key] is not None:
                        src_file = join(src_system.path, game.paths[key])
                        if isfile(src_file):
                            if key == 'path':
                                dest_path = join(
                                    self.path, basename(game.paths[key]))
                                merge_file(src_file, dest_path)
                                if game.paths[key] is not None:
                                    new_game.paths[key] = "./" + \
                                        basename(game.paths[key])
                            else:
                                media_dir = configs['dest_media_dirs_names'][key]
                                dest_path = join(
                                    self.path, media_dir, basename(game.paths[key]))
                                merge_file(src_file, dest_path)
                                if game.paths[key] is not None:
                                    new_game.paths[key] = "./" + \
                                        join(media_dir, basename(
                                            game.paths[key]))
                for key in new_game.info.keys():
                    if self.stop:
                        break
                    new_game.info[key] = game.info[key]

                self.games.append(new_game)

    def save_gamelist(self):
        """Make Description."""
        print_verbose_msg(
            "green", '\n            Save GameListXml File:', gui=self.gui)

        path = join(self.path, 'gamelist.xml')

        root = None
        if isfile(path):
            backup_gamelist(path)

        srt_xml = '<?xml version="1.0" encoding="UTF-8"?><gameList></gameList>'
        root = ET.fromstring(srt_xml)
        if configs["gamelist_provider"] is not None:
            provider_xml = ET.Element('provider')
            for key, value in configs["gamelist_provider"].items():
                if self.stop:
                    break
                subelement = ET.SubElement(provider_xml, key)
                subelement.text = value
            root.append(provider_xml)

        progress_base = len(self.games)
        for progress_id, game in enumerate(self.games):
            print_verbose_progressbar(progress_id, progress_base, gui=self.gui)
            if self.stop:
                break
            game_xml = game.gen_game_xml()
            root.append(game_xml)
        with open(path, "w", encoding="utf-8") as file_out:
            file_out.write(xdm.parseString(ET.tostring(root)).toprettyxml())

    def gen_report(self):
        """Make Description."""
        print_verbose_msg(
            "green", '\n            Generating Reports Files:', gui=self.gui)

        progress_base = len(self.games)
        for progress_id, game in enumerate(self.games):
            print_verbose_progressbar(progress_id, progress_base, gui=self.gui)
            if self.stop:
                break

            if game.paths['path'] is not None:
                text = f"Name: {game.info['name']}   File:{basename(game.paths['path'])}"
                for key, value in game.paths.items():
                    if self.stop:
                        break
                    if key != 'path' and value is None:
                        game_filename = text
                        self.reports['ausent_media'][key].append(game_filename)

                for key, value in game.info.items():
                    if self.stop:
                        break
                    if value is None:
                        game_filename = text
                        self.reports['ausent_info'][key].append(game_filename)

    def save_reports(self):
        """Make Description."""
        print_verbose_msg(
            "green", '\n            Saving Reports Files:', gui=self.gui)

        path = join(self.path, 'sbfrm_reports')
        makedirs(path, exist_ok=True)
        for key, media in self.reports['ausent_media'].items():
            if self.stop:
                break
            if key != 'path':
                report_path = join(path, 'games_wihout_')
                report_path += key + '.txt'
                report = ''
                for game_name in media:
                    if self.stop:
                        break
                    report += game_name + '\n'
                with open(report_path, "w", encoding="utf-8") as file_out:
                    file_out.write(report)

        for key, media in self.reports['ausent_info'].items():
            if self.stop:
                break
            if key != 'path':
                report_path = join(path, 'games_wihout_info_')
                report_path += key + '.txt'
                report = ''
                for game_name in media:
                    if self.stop:
                        break
                    report += game_name + '\n'
                with open(report_path, "w", encoding="utf-8") as file_out:
                    file_out.write(report)

        report_path = join(path, 'games_removed.txt')
        report = ''
        for game_added in self.reports['games_removed']:
            if self.stop:
                break
            report += game_added + '\n'
        with open(report_path, "w", encoding="utf-8") as file_out:
            file_out.write(report)
