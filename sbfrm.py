import argparse
from src.collection_handler import CollectionHandler

parser = argparse.ArgumentParser(description='RetroGames Collection Manager')
parser.add_argument("op", help="Operation")
parser.add_argument("src", help="Source Folder")
parser.add_argument("dest", help="Destiantion Folder")
parser.add_argument("-box_src", help="Box Folder Source")
parser.add_argument("-img_src", help="Image Folder Source")
parser.add_argument("-marq_src", help="Marquee Folder Source")
parser.add_argument("-thumb_src", help="Thumbnail Folder Source")
parser.add_argument("-vid_src", help="Video Folder Source")
parser.add_argument("-subcol_list", help="SubCollections Tag Lists")
parser.add_argument("-filemode", help="For copy or move file: '-filemode cp' or -filemode mv")
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
