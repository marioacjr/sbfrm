"""Make Description."""
import argparse
from os.path import join

from src.collection import Collection
from src.terminalutils import print_verbose_msg

parser = argparse.ArgumentParser(description='RetroGames Collection Manager')

HELPTEXT = """Operation"""
parser.add_argument("op", help=HELPTEXT)

HELPTEXT = """Source Folder"""
parser.add_argument("src", help=HELPTEXT)

HELPTEXT = """Destiantion Folder"""
parser.add_argument("dest", help=HELPTEXT)

args = parser.parse_args()

col = Collection()
if args.op == "update_system":
    print_verbose_msg('cyan', 'Update System:')
    col.update_sys_from(args.dest, args.src)
    
elif args.op == "update_collection":
    print_verbose_msg('cyan', 'Update Collection:')
        
    sys_names = col.list_systems(args.src)
    for sys_name in sys_names:
        print_verbose_msg('lightcyan', f'\n    Processing: {sys_name}')
            
        src_path = join(args.src, sys_name)
        dest_path = join(args.dest, sys_name)
        col.update_sys_from(dest_path, src_path)
        
print_verbose_msg('lightcyan', '\n\n')
