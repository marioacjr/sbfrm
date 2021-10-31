import argparse
from src.collection_handler import update_collections, update_subcollection, raise_subcollection

parser = argparse.ArgumentParser(description='RetroGames Collection Manager')
parser.add_argument("op", help="Operation")
parser.add_argument("src", help="Source Folder")
parser.add_argument("dest", help="Destiantion Folder")
parser.add_argument("-box_src", help="Box Folder Source")
parser.add_argument("-filemode", help="For copy or move file: '-filemode cp' or -filemode mv")
parser.add_argument("-img_src", help="Image Folder Source")
parser.add_argument("-marq_src", help="Marquee Folder Source")
parser.add_argument("-thumb_src", help="Thumbnail Folder Source")
parser.add_argument("-vid_src", help="Video Folder Source")
parser.add_argument("-subcol_list", help="SubCollections Tag Lists")
args = parser.parse_args()


if args.op == 'update_collections':
    update_collections(args)
elif args.op == 'update_subcollection':
    update_subcollection(args)
elif args.op == 'raise_subcollection':
    raise_subcollection(args)
