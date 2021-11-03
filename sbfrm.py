import argparse
from src.collection_handler import CollectionHandler

parser = argparse.ArgumentParser(description='RetroGames Collection Manager')

helptext = """Operation"""
parser.add_argument("op", help=helptext)

helptext = """Source Folder"""
parser.add_argument("src", help=helptext)

helptext = """Destiantion Folder"""
parser.add_argument("dest", help=helptext)

helptext = """Box Folder Source"""
parser.add_argument("-box_src", help=helptext)

helptext = """Image Folder Source"""
parser.add_argument("-img_src", help=helptext)

helptext = """Marquee Folder Source"""
parser.add_argument("-marq_src", help=helptext)

helptext = """Thumbnail Folder Source"""
parser.add_argument("-thumb_src", help=helptext)

helptext = """Video Folder Source"""
parser.add_argument("-vid_src", help=helptext)

helptext = """SubCollections Tag Lists"""
parser.add_argument("-subcol_list", help=helptext)

helptext = """For copy or move file: '-filemode cp' or -filemode mv"""
parser.add_argument("-filemode", help=helptext)

args = parser.parse_args()

ch = CollectionHandler(args.src, args.dest, args.box_src, args.img_src,
                       args.marq_src, args.thumb_src, args.vid_src,
                       args.subcol_list, args.filemode)
if args.op == 'update_collections':
    ch.update_collections()
elif args.op == 'update_subcollection':
    ch.update_subcollection()
elif args.op == 'raise_subcollection':
    ch.raise_subcollection()
