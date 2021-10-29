import os
import argparse
import xml_handler as xmlh
import file_handler as fh
import shutil
import hashlib

box_dirname = 'boxarts'
img_dirname = 'images'
marq_dirname = 'marquees'
thumb_dirname = 'thumbnails'
video_dirname = 'videos'

parser = argparse.ArgumentParser(description='RetroGames Collection Manager')
parser.add_argument("op", help="Operation: update_collections, update_subcollection or raise_subcollection")
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


def cp_collection_media(file, src_dir, dest_dir, tree, subcoltag=False):
    i, b, t, m, v = False, False, False, False, False
    if args.img_src:
        i = fh.copy_game_media(file, '.png', src_dir, args.img_src, dest_dir, img_dirname, subcoltag, args.filemode)
        i = i or fh.copy_game_media_by_gamelistfile(tree, file, 'image', '.png', src_dir, args.img_src, dest_dir, img_dirname, subcoltag, args.filemode)
    if args.box_src:
        b = fh.copy_game_media(file, '.png', src_dir, args.box_src, dest_dir, box_dirname, subcoltag, args.filemode)
        b = b or fh.copy_game_media_by_gamelistfile(tree, file, 'box', '.png', src_dir, args.box_src, dest_dir, box_dirname, subcoltag, args.filemode)
    if args.thumb_src:
        t = fh.copy_game_media(file, '.png', src_dir, args.thumb_src, dest_dir, thumb_dirname, subcoltag, args.filemode)
        t = t or fh.copy_game_media_by_gamelistfile(tree, file, 'thumbnail', '.png', src_dir, args.thumb_src, dest_dir, thumb_dirname, subcoltag, args.filemode)
    if args.marq_src:
        m = fh.copy_game_media(file, '.png', src_dir, args.marq_src, dest_dir, marq_dirname, subcoltag, args.filemode)
        m = m or fh.copy_game_media_by_gamelistfile(tree, file, 'marquee', '.png', src_dir, args.marq_src, dest_dir, marq_dirname, subcoltag, args.filemode)
    if args.vid_src:
        v = fh.copy_game_media(file, '.mp4', src_dir, args.vid_src, dest_dir, video_dirname, subcoltag, args.filemode)
        v = v or fh.copy_game_media_by_gamelistfile(tree, file, 'video', '.mp4', src_dir, args.vid_src, dest_dir, video_dirname, subcoltag, args.filemode)

    return i, b, t, m, v


def save_results(tree, dest_dir, game_wihout_image, game_wihout_video,
                 game_wihout_box, game_wihout_marquee, game_wihout_thumbnails,
                 subcoltag=False):
    fh.save_txt_file(dest_dir, 'game_wihout_image.txt', game_wihout_image)
    fh.save_txt_file(dest_dir, 'game_wihout_video.txt', game_wihout_video)
    fh.save_txt_file(dest_dir, 'game_wihout_box.txt', game_wihout_box)
    fh.save_txt_file(dest_dir, 'game_wihout_marquee.txt', game_wihout_marquee)
    fh.save_txt_file(dest_dir, 'game_wihout_thumbnails.txt', game_wihout_thumbnails)

    g, i, v, b, m, t, d = xmlh.get_tree_details(tree)
    collection_details = '\n\tGameList Results:'
    collection_details += '\n\t\tGames: ' + str(g)
    collection_details += '\n\t\tImages: ' + str(i)
    collection_details += '\n\t\tVideos: ' + str(v)
    collection_details += '\n\t\tBoxes: ' + str(b)
    collection_details += '\n\t\tMarquees: ' + str(m)
    collection_details += '\n\t\tThumbnails: ' + str(t)
    collection_details += '\n\t\tDescriptions: ' + str(d)

    f = len(fh.get_files(dest_dir))
    i = len(fh.get_files(os.path.join(dest_dir, img_dirname)))
    v = len(fh.get_files(os.path.join(dest_dir, video_dirname)))
    b = len(fh.get_files(os.path.join(dest_dir, box_dirname)))
    m = len(fh.get_files(os.path.join(dest_dir, marq_dirname)))
    t = len(fh.get_files(os.path.join(dest_dir, thumb_dirname)))
    if subcoltag:
        f += len(fh.get_files(os.path.join(dest_dir, subcoltag)))
        i += len(fh.get_files(os.path.join(dest_dir, img_dirname, subcoltag)))
        v += len(fh.get_files(os.path.join(dest_dir, video_dirname, subcoltag)))
        b += len(fh.get_files(os.path.join(dest_dir, box_dirname, subcoltag)))
        m += len(fh.get_files(os.path.join(dest_dir, marq_dirname, subcoltag)))
        t += len(fh.get_files(os.path.join(dest_dir, thumb_dirname, subcoltag)))
    collection_details += '\n\tFiles Results:'
    collection_details += '\n\t\tFiles: ' + str(f)
    collection_details += '\n\t\tImages: ' + str(i)
    collection_details += '\n\t\tVideos: ' + str(v)
    collection_details += '\n\t\tBoxes: ' + str(b)
    collection_details += '\n\t\tMarquees: ' + str(m)
    collection_details += '\n\t\tThumbnails: ' + str(t)
    collection_details += '\n====================================='

    fh.save_txt_file(dest_dir, 'gamelist_results.txt', collection_details)

    print(collection_details)


def copy_collection(src_dir, dest_dir, subcoltag=False):
    proc_col_msg = 'Processing Collection: ' + dest_dir
    if subcoltag:
        proc_col_msg += ' SubCollection: ' + subcoltag
    print(proc_col_msg)

    xml_path = os.path.join(dest_dir, 'gamelist.xml')
    tree = xmlh.get_gamelist(xml_path)
    xmlh.backup_xml(tree, xml_path)

    game_wihout_video = ''
    game_wihout_image = ''
    game_wihout_box = ''
    game_wihout_marquee = ''
    game_wihout_thumbnails = ''

    xml2_path = os.path.join(src_dir, 'gamelist.xml')
    tree2 = xmlh.get_gamelist(xml2_path)

    files = fh.get_files(src_dir, subcoltag)
    files.sort()
    for file in files:
        p = fh.copy_game_file(src_dir, dest_dir,
                              file, subcoltag, args.filemode)
        i, b, t, m, v = cp_collection_media(file, src_dir,
                                          dest_dir, tree2,
                                          subcoltag)
        if p:
            game = xmlh.create_game(p)
            tree.getroot().append(game)

        if not i:
            game_wihout_image += file + '\n'
        if not b:
            game_wihout_box += file + '\n'
        if not t:
            game_wihout_thumbnails += file + '\n'
        if not m:
            game_wihout_marquee += file + '\n'
        if not v:
            game_wihout_video += file + '\n'

    xmlh.update_tree1_from_tree2(tree, tree2)

    xmlh.update_media_paths(tree, dest_dir, box_dirname, img_dirname, marq_dirname, thumb_dirname, video_dirname)

    xmlh.save_xml(tree, xml_path)

    save_results(tree, dest_dir, game_wihout_image,
                 game_wihout_video, game_wihout_box,
                 game_wihout_marquee, game_wihout_thumbnails,
                 subcoltag)


def update_collections(subcoltag=False):
    folders = fh.get_folders(args.src)
    for folder in folders:
        src_dir = os.path.join(args.src, folder)
        if os.path.isfile(os.path.join(src_dir, 'gamelist.xml')):
            dest_dir = os.path.join(args.dest, folder)

            if fh.check_folders(src_dir, dest_dir,
                             img_dirname,
                             box_dirname,
                             video_dirname,
                             marq_dirname,
                             thumb_dirname,
                             subcoltag):

                copy_collection(src_dir, dest_dir, subcoltag)


def raise_subcollection(src_dir, subcoltag, dest_dir, newcolname):
    proc_col_msg = 'Processing Raised Collection: ' + newcolname
    print(proc_col_msg)
    subcolpath = os.path.join(src_dir, subcoltag)
    dest_dir = os.path.join(dest_dir, newcolname)

    if fh.check_folders(subcolpath, dest_dir,
                     img_dirname,
                     box_dirname,
                     video_dirname,
                     marq_dirname,
                     thumb_dirname):

        xml_path = os.path.join(dest_dir, 'gamelist.xml')
        tree = xmlh.get_gamelist(xml_path)
        xmlh.backup_xml(tree, xml_path)

        xml_path2 = os.path.join(src_dir, 'gamelist.xml')
        tree2 = xmlh.get_gamelist(xml_path2)

        files = fh.get_files(subcolpath)
        files.sort()
        for file in files:
            p = fh.copy_game_file(subcolpath, dest_dir, file)

            s = os.path.join(src_dir, args.img_src, subcoltag)
            n = os.path.splitext(file)[0] + '.png'
            d = os.path.join(dest_dir, img_dirname)
            fh.copy_game_file(s, d, n)

            path_text = os.path.join(subcoltag, n)
            tag = 'path'
            game2 = xmlh.get_game_by_tag_text(tree2.getroot(), tag, path_text)
            if game2 != False and game2.find(tag).text is not None:
                vs = [['box', args.box_src],
                      ['image', args.img_src],
                      ['marquee', args.marq_src],
                      ['thumbnail', args.thumb_src],
                      ['video', args.vid_src]]
                for v in vs:
                    if game2.find(v[0]) is not None:
                        if game2.find(v[0]).text is not None:
                            mf = game2.find(v[0]).text.replace('./', '')
                            if os.path.isfile(os.path.join(src_dir, mf)):
                                n2 = os.path.basename(mf)
                                s2 = os.path.join(src_dir, v[1])
                                fh.copy_game_file(s2, d, n2)

                if p:
                    game1 = xmlh.get_game_by_tag_text(tree.getroot(), 'path', p)
                    if not game1:
                        game1 = xmlh.create_game(p)
                    xmlh.update_game1_from_game2(game1, game2)
                    tree.getroot().append(game1)

        xmlh.update_media_paths(tree, dest_dir, box_dirname, img_dirname, marq_dirname, thumb_dirname, video_dirname)
        xmlh.save_xml(tree, xml_path)



def update_subcollection():
    if args.subsys_list:
        subcollist = args.subsys_list.split(',')
        for subcoltag in subcollist:
            update_collections(subcoltag)


if args.op == 'update_collections':
    update_collections()
elif args.op == 'update_subcollection':
    update_subcollection()
elif args.op == 'raise_subcollection':
    subcollist = args.subcol_list.split(',')
    for subcol in subcollist:
        colsufix = subcol
        for c in [' ', '#', '(', ')']:
            colsufix = colsufix.replace(c, '')
        newcolname = os.path.basename(os.path.normpath(args.src)) + '_' + colsufix.lower()
        raise_subcollection(args.src, subcol, args.dest, newcolname)
