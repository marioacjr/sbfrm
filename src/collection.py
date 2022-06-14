"""Make Description."""

import shutil

from os import listdir, makedirs
from os.path import isdir, isfile, join, basename, splitext
from src.terminalutils import get_progress_bar

from src.system import System


def get_file_name(path):
    """Make Description."""
    return splitext(basename(path))[-2]


def get_file_extension(path):
    """Make Description."""
    return splitext(basename(path))[-1]


def make_sys_dirs(path, mdirs, subsys=None):
    """Make Description."""
    if subsys is None:
        makedirs(path, exist_ok=True)
    else:
        makedirs(join(path, subsys), exist_ok=True)

    for value in mdirs.values():
        mpath = join(path, value)
        if subsys is not None:
            mpath = join(mpath, subsys)
        makedirs(mpath, exist_ok=True)


class Collection:
    """Base class for system."""

    def __init__(self):
        """Make Description."""
        self.systems = []
        self.excluded_dirs = ['backup', 'bezels', 'BGM', 'bios', 'mplayer',
                              'downloads', 'download', 'scummvm', 'ports',
                              'model2', 'model3', 'windows', '.update',
                              'System Volume Information', 'LOST.DIR']
        self.media_dirs = {"boxart": "boxart", "image": "image",
                           "marquee": "marquee", "thumbnail": "thumbnail",
                           "video": "video"}

    def __str__(self):
        """Make Description."""
        return ""

    def list_systems(self, path):
        """Make Description."""
        systems_path = [d for d in listdir(path) if isdir(join(path, d))]
        systems_path = [d for d in systems_path if not self.excluded_dir(d)]
        return systems_path

    def excluded_dir(self, dir_name):
        """Make Description."""
        for name in self.excluded_dirs:
            if name in dir_name:
                return True
        return False

    def copy_files(self, system_path, src_path, src_mdirs,
                   subsys=None, verbose=False):
        """Make Description."""
        make_sys_dirs(system_path, self.media_dirs, subsys=subsys)
        src_system = System()
        src_system.load(src_path, src_mdirs, subsys=subsys)
        progress_base = len(src_system.games)
        if verbose:
            print_txt = '\n    Copying Files:'
            if subsys is not None:
                print_txt = print_txt.replace(':', ' (' + subsys + '):')
            print(print_txt, end='', flush=True)
        for gid, game in enumerate(src_system.games):
            if verbose:
                print(get_progress_bar(gid, progress_base), end='', flush=True)

            for key, value in game.paths.items():
                if value is not None:
                    if key == 'path':
                        if subsys is None:
                            src_file = join(src_path, basename(value))
                            if isfile(src_file):
                                shutil.copy(src_file, system_path)
                        else:
                            src_file = join(src_path, subsys, basename(value))
                            if isfile(src_file):
                                dest_path = join(system_path, subsys)
                                shutil.copy(src_file, dest_path)
                    elif src_mdirs[key] is not None:
                        src_file = join(src_path, src_mdirs[key])
                        if subsys is not None:
                            src_file = join(src_file, subsys)
                        src_file = join(src_file, basename(value))
                        if isfile(src_file):
                            dest_path = get_file_name(game.paths['path'])
                            dest_path += get_file_extension(src_file)
                            if subsys is not None:
                                dest_path = join(subsys, dest_path)
                            dest_path = join(self.media_dirs[key], dest_path)
                            dest_path = join(system_path, dest_path)
                            shutil.copy(src_file, dest_path)

    def update_sys_from(self, sys_path, src_path, src_mdirs,
                        subsyslist=None, overwrite_info=False, provider=None,
                        verbose=False):
        """Make Description."""
        system = System()
        gl_dest_path = join(sys_path, 'gamelist.xml')
        gl_src_path = join(src_path, 'gamelist.xml')

        self.copy_files(sys_path, src_path, src_mdirs, verbose=verbose)
        system.load(sys_path, self.media_dirs)

        if isinstance(subsyslist, list):
            for subsys in subsyslist:
                if isdir(join(src_path, subsys)):
                    self.copy_files(sys_path, src_path, src_mdirs,
                                    subsys=subsys)
                    system.load(sys_path, self.media_dirs, subsys=subsys)

        if overwrite_info:
            system.load_info(gl_dest_path)
            system.load_info(gl_src_path)
        else:
            system.load_info(gl_src_path)
            system.load_info(gl_dest_path)

        system.set_gamelist(gl_dest_path, provider=provider)
