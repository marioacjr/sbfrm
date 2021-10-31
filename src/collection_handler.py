import os
import src.xml_handler as xmlh
import src.file_handler as fh
import shutil
import hashlib

box_dirname = 'boxarts'
img_dirname = 'images'
marq_dirname = 'marquees'
thumb_dirname = 'thumbnails'
video_dirname = 'videos'


def cp_collection_media(file, src_dir, dest_dir, tree, args, subcoltag=False):
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


def copy_collection(src_dir, dest_dir, args, subcoltag=False):
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
                                          args, subcoltag)
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


def update_collections(args, subcoltag=False):
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

                copy_collection(src_dir, dest_dir, args, subcoltag)


def gen_raised_colname(subcol, src):
    colsufix = subcol.replace(' ', '')
    colsufix = colsufix.replace('#', '')
    colsufix = colsufix.replace('(', '')
    colsufix = colsufix.replace(')', '')
    n = os.path.basename(os.path.normpath(src)) + '_' + colsufix.lower()
    return n


def copy_raised_files(args, subcol, file):
    newcolname = gen_raised_colname(subcol, args.src)
    subcolpath = os.path.join(args.src, subcol)
    dest_dir = os.path.join(args.dest, newcolname)

    p = fh.copy_game_file(subcolpath, dest_dir, file)

    variable = [[args.box_src, '.png', box_dirname, False],
              [args.img_src, '.png', img_dirname, False],
              [args.marq_src, '.png', marq_dirname, False],
              [args.thumb_src, '.png', thumb_dirname, False],
              [args.vid_src, '.mp4', video_dirname, False]]
    for v in variable:
        if v[0]:
            s = os.path.join(args.src, v[0], subcol)
            n = os.path.splitext(file)[0] + v[1]
            d = os.path.join(dest_dir, v[2])
            v[3] = fh.copy_game_file(s, d, n)

    b = variable[0][3]
    i = variable[1][3]
    m = variable[2][3]
    t = variable[3][3]
    v = variable[4][3]
    return p, i, b, t, m, v


def check_folders(src, dest_dir):
    if fh.check_folders(src, dest_dir,
                        img_dirname,
                        box_dirname,
                        video_dirname,
                        marq_dirname,
                        thumb_dirname):
        return True
    return False


def raise_subcollection(args):
    subcollist = args.subcol_list.split(',')
    for subcol in subcollist:
        newcolname = gen_raised_colname(subcol, args.src)
        proc_col_msg = 'Processing Raised Collection: ' + newcolname
        print(proc_col_msg)
        subcolpath = os.path.join(args.src, subcol)
        dest_dir = os.path.join(args.dest, newcolname)

        if check_folders(subcolpath, dest_dir):

            xml_path = os.path.join(dest_dir, 'gamelist.xml')
            tree = xmlh.get_gamelist(xml_path)
            xmlh.backup_xml(tree, xml_path)

            xml_path2 = os.path.join(args.src, 'gamelist.xml')
            tree2 = xmlh.get_gamelist(xml_path2)

            files = fh.get_files(subcolpath)
            files.sort()
            for file in files:
                p, i, b, t, m, v = copy_raised_files(args, subcol, file)
                if p:
                    subcolfile = os.path.join(subcol, p)
                    copy_game_media_from_tree(subcolfile, tree2, dest_dir)

                    game1 = xmlh.get_game_by_tag_text(tree.getroot(), 'path', p)
                    game2 = xmlh.get_game_by_tag_text(tree2.getroot(), 'path',
                                                      subcolfile)

                    if not game1:
                        game1 = xmlh.create_game(p)
                    xmlh.update_game1_from_game2(game1, game2)
                    tree.getroot().append(game1)

            xmlh.update_media_paths(tree, dest_dir, box_dirname, img_dirname, marq_dirname, thumb_dirname, video_dirname)
            xmlh.save_xml(tree, xml_path)


def copy_game_media_from_tree(filename, tree, dest):
    if filename:
        game = xmlh.get_game_by_tag_text(tree.getroot(), 'path', filename)
        if game:
            vs = [['box', box_dirname, '.png'],
                  ['image', img_dirname, '.png'],
                  ['marquee', marq_dirname, '.png'],
                  ['thumbnail', thumb_dirname, '.png'],
                  ['video', video_dirname, '.mp4']]
            for v in vs:
                if game.find(v[0]) and game.find(v[0]).text:
                    if os.path.isfile(game.find(v[0]).text):
                        n = os.path.splitext(filename)[0] + v[2]
                        fh.copy_game_file(game.find(v[0]).text,
                                          os.path.join(dest, v[1],
                                          n))





def update_subcollection(args):
    if args.subsys_list:
        subcollist = args.subsys_list.split(',')
        for subcoltag in subcollist:
            update_collections(subcoltag)
