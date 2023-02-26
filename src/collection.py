"""Make Description."""

import shutil

from os import listdir, makedirs
from os.path import isdir, isfile, join, basename, splitext
from src.terminalutils import get_progress_bar

from src.system import System


class Collection:
    """Base class for system."""

    def __init__(self):
        """Make Description."""
        self.excluded_dirs = ['backup', 'bezels', 'BGM', 'bios', 'mplayer',
                              'downloads', 'download', 'scummvm', 'ports',
                              'model2', 'model3', 'windows', '.update',
                              'System Volume Information', 'LOST.DIR']
        self.media_dirs = {"boxart": ["boxart"], "image": ["image"],
                           "marquee": ["marquee"], "thumbnail": ["thumbnail"],
                           "video": ["video"]}
        self.stop_copy = False # Used bay GUI to stop process before finish.

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

    def update_sys_from(self, sys_path, src_path, src_mdirs,
                        subsyslist=None, overwrite_info=False, provider=None,
                        verbose=False, overwrite_file=False, gui=False):
        """Make Description."""
        src_system = System(src_path)
        src_system.load(src_path, src_mdirs)
                        
        
        dest_system = System(sys_path)
        dest_system.make_sys_dirs(sys_path, self.media_dirs)
        dest_system.load(sys_path, self.media_dirs)
        dest_system.copy_files_from_system(src_system, src_mdirs, self.media_dirs,
                                           verbose=verbose, overwrite_file=overwrite_file, gui=gui)
        
        if isdir(sys_path):
            if isinstance(subsyslist, list):
                for subsys in subsyslist:
                    if isdir(join(src_path, subsys)):
                        dest_system.make_sys_dirs(sys_path, self.media_dirs, subsys)
                        dest_system.load(sys_path, self.media_dirs, subsys=subsys)
                        dest_system.copy_files_from_system(src_system, src_mdirs, self.media_dirs, subsys=subsys,
                                                           verbose=verbose, overwrite_file=overwrite_file, gui=gui)

        gl_dest_path = join(sys_path, 'gamelist.xml')
        gl_src_path = join(src_path, 'gamelist.xml')
        if overwrite_info:
            dest_system.load_info(gl_dest_path)
            dest_system.load_info(gl_src_path)
        else:
            dest_system.load_info(gl_src_path)
            dest_system.load_info(gl_dest_path)

        dest_system.save_gamelist(gl_dest_path, provider=provider)
        dest_system.gen_report()
        dest_system.save_reports(sys_path)
