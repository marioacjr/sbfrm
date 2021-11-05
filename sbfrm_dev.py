import argparse
from src.baseclasses import Game, System

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

system = System('test/roms1/',
                'mastersystem',
                images='downloaded_images',
                videos='downloaded_videos')
system.load_gamelist()
system.load_games()
system.gen_xml_gamelist_from_games()
