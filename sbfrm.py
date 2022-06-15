"""Make Description."""

import argparse
from os.path import join

from src.collection import Collection
from src.terminalutils import text_colored

parser = argparse.ArgumentParser(description='RetroGames Collection Manager')

HELPTEXT = """Operation"""
parser.add_argument("op", help=HELPTEXT)

HELPTEXT = """Source Folder"""
parser.add_argument("src", help=HELPTEXT)

HELPTEXT = """Destiantion Folder"""
parser.add_argument("dest", help=HELPTEXT)

HELPTEXT = """Box Folder Source"""
parser.add_argument("-box_src", help=HELPTEXT)

HELPTEXT = """Image Folder Source"""
parser.add_argument("-img_src", help=HELPTEXT)

HELPTEXT = """Marquee Folder Source"""
parser.add_argument("-marq_src", help=HELPTEXT)

HELPTEXT = """Thumbnail Folder Source"""
parser.add_argument("-thumb_src", help=HELPTEXT)

HELPTEXT = """Video Folder Source"""
parser.add_argument("-vid_src", help=HELPTEXT)

HELPTEXT = """SubSystem Tag List"""
parser.add_argument("-subsyslist", help=HELPTEXT)

HELPTEXT = """For copy or move file: '-filemode [cp, mv]"""
parser.add_argument("-filemode", help=HELPTEXT)

HELPTEXT = """For copy or move file: '-overwritefile [0, 1]"""
parser.add_argument("-overwritefile", help=HELPTEXT)

HELPTEXT = """Print text output: -verbose [True, False]"""
parser.add_argument("-verbose", help=HELPTEXT)

args = parser.parse_args()

src, dest, subsyslist = args.src, args.dest, args.subsyslist
if subsyslist:
    subsyslist = subsyslist.split(',')
mdirs = {"boxart": args.box_src,
         "image": args.img_src,
         "marquee": args.marq_src,
         "thumbnail": args.thumb_src,
         "video": args.vid_src}
provider = {
    "system": "system_one",
    "software": "SBFRM",
    "web": "https://github.com/marioacjr/sbfrm"
}
verbose = args.verbose == '1'

col = Collection()
if args.op == "update_system":
    if verbose:
        print(text_colored('green', 'Update System:'), dest,
              flush=True, end='')
    col.update_sys_from(dest, src, mdirs, subsyslist=subsyslist,
                        verbose=verbose)
elif args.op == "update_collection":
    if verbose:
        print(text_colored('green', 'Update Collection:'), flush=True, end='')
    sys_paths = col.list_systems(args.src)
    for sys_path in sys_paths:
        if verbose:
            print(text_colored('green', '\n  Processing:'), sys_path, '',
                  flush=True, end='')
        src_path = join(args.src, sys_path)
        dest_path = join(args.dest, sys_path)
        col.update_sys_from(dest_path, src_path, mdirs, subsyslist=subsyslist,
                            verbose=verbose)
if verbose:
    print()
