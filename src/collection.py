"""Make Description."""
from os import listdir
from os.path import isdir, join

from src.fileutils import configs, make_sys_dirs
from src.terminalutils import print_verbose_msg

from src.system import System


class Collection:
    """Base class for system."""

    def __init__(self, gui=False):
        """Make Description."""
        self.excluded_dirs = ['backup', 'bezels', 'BGM', 'bios', 'mplayer',
                              'downloads', 'download', 'scummvm', 'ports',
                              'model2', 'model3', 'windows', '.update',
                              'System Volume Information', 'LOST.DIR']
        self.stop_copy = False # Used by the GUI to stop gently the process.
        self.gui = gui

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

    def update_sys_from(self, dest_sys, src_sys):
        """Make Description."""
        print_verbose_msg('blue', '\n        Loading Source System:')
            
        src_system = System(src_sys)  
        src_system.load()
        
        print_verbose_msg('blue', '\n        Loading Dest System:')
        
        dest_system = System(dest_sys)
        make_sys_dirs(dest_sys)
        dest_system.load()
        
        
        print_verbose_msg('blue', '\n        Merging Source to Dest:')
        dest_system.copy_files_from_system(src_system)
        dest_system.remove_games_clones()
        
        print_verbose_msg('blue', '\n        Generating GamelistXml File:')
        
        gl_dest_path = join(dest_sys, 'gamelist.xml')
        dest_system.save_gamelist(gl_dest_path)
        
        print_verbose_msg('blue', '\n        Generating Reports Files:')
        
        dest_system.gen_report()
        dest_system.save_reports(dest_sys)
        
        
