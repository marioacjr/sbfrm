import os
import src.xml_handler as xmlh
import src.file_handler as fh


class CollectionHandler:

    def __init__(self, src, dest, boxarts_src=False, images_src=False,
                 marquees_src=False, thumbnails_src=False, videos_src=False,
                 subcol_list=False, filemode=False):
        self.src = src
        self.dest = dest

        self.box_dest_dir = 'boxarts'
        self.img_dest_dir = 'images'
        self.marq_dest_dir = 'marquees'
        self.thumb_dest_dir = 'thumbnails'
        self.vid_dest_dir = 'videos'

        self.box_src_dir = boxarts_src
        self.img_src_dir = images_src
        self.marq_src_dir = marquees_src
        self.thumb_src_dir = thumbnails_src
        self.vid_src_dir = videos_src

        self.subcol_list = subcol_list
        self.filemode = filemode

    def copy_media_file(self, file, src_dir, dest_dir, tree, tag, ext,
                        src_media, dest_media, subcoltag=False):
        b = False
        if src_media:
            b = fh.copy_game_media(file, ext,
                                   src_dir, src_media, dest_dir,
                                   dest_media, subcoltag, self.filemode)
            b = b or fh.copy_game_media_by_gamelistfile(
                tree, file, tag, ext,
                src_dir, src_media, dest_dir, dest_media,
                subcoltag, self.filemode)
        return b

    def copy_collection_media(self, file, src_dir, dest_dir,
                              tree, subcoltag=False):
        i = self.copy_media_file(file, src_dir, dest_dir, tree,
                                 'image', '.png', self.img_src_dir,
                                 self.img_dest_dir, subcoltag)
        b = self.copy_media_file(file, src_dir, dest_dir, tree,
                                 'box', '.png', self.box_src_dir,
                                 self.box_dest_dir, subcoltag)
        t = self.copy_media_file(file, src_dir, dest_dir, tree,
                                 'thumbnail', '.png', self.thumb_src_dir,
                                 self.thumb_dest_dir, subcoltag)

        m = self.copy_media_file(file, src_dir, dest_dir, tree,
                                 'marquee', '.png', self.marq_src_dir,
                                 self.marq_dest_dir, subcoltag)

        v = self.copy_media_file(file, src_dir, dest_dir, tree,
                                 'video', '.mp4', self.vid_src_dir,
                                 self.vid_dest_dir, subcoltag)

        return i, b, t, m, v

    def copy_game_files(self, src_dir, dest_dir, file, tree, subcoltag):
        p = fh.copy_game_file(src_dir, dest_dir,
                              file, subcoltag, self.filemode)
        i, b, t, m, v = self.copy_collection_media(file, src_dir,
                                                   dest_dir, tree,
                                                   subcoltag)
        return p, i, b, t, m, v

    def copy_collection(self, src_dir, dest_dir, subcoltag=False):
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
            p, i, b, t, m, v = self.copy_game_files(src_dir, dest_dir, file,
                                                    tree2, subcoltag)

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

        xmlh.update_media_paths(tree, dest_dir, self.box_dest_dir,
                                self.img_dest_dir, self.marq_dest_dir,
                                self.thumb_dest_dir, self.vid_dest_dir)

        xmlh.save_xml(tree, xml_path)

        self.save_results(tree, dest_dir, game_wihout_image,
                          game_wihout_video, game_wihout_box,
                          game_wihout_marquee, game_wihout_thumbnails,
                          subcoltag)

    def update_collections(self, subcoltag=False):
        folders = fh.get_folders(self.src)
        for folder in folders:
            src_dir = os.path.join(self.src, folder)
            if os.path.isfile(os.path.join(src_dir, 'gamelist.xml')):
                dest_dir = os.path.join(self.dest, folder)

                if fh.check_folders(src_dir, dest_dir,
                                    self.img_dest_dir,
                                    self.box_dest_dir,
                                    self.vid_dest_dir,
                                    self.marq_dest_dir,
                                    self.thumb_dest_dir,
                                    subcoltag):

                    self.copy_collection(src_dir, dest_dir, subcoltag)

    def gen_raised_colname(self, subcol, src):
        colsufix = subcol.replace(' ', '')
        colsufix = colsufix.replace('#', '')
        colsufix = colsufix.replace('(', '')
        colsufix = colsufix.replace(')', '')
        n = os.path.basename(os.path.normpath(src)) + '_' + colsufix.lower()
        return n

    def copy_raised_files(self, subcol, file):
        newcolname = self.gen_raised_colname(subcol, self.src)
        subcolpath = os.path.join(self.src, subcol)
        dest_dir = os.path.join(self.dest, newcolname)

        p = fh.copy_game_file(subcolpath, dest_dir, file)

        variable = [[self.box_src_dir, '.png', self.box_dest_dir, False],
                    [self.img_src_dir, '.png', self.img_dest_dir, False],
                    [self.marq_src_dir, '.png', self.marq_dest_dir, False],
                    [self.thumb_src_dir, '.png', self.thumb_dest_dir, False],
                    [self.vid_src_dir, '.mp4', self.vid_dest_dir, False]]
        for v in variable:
            if v[0]:
                s = os.path.join(self.src, v[0], subcol)
                n = os.path.splitext(file)[0] + v[1]
                d = os.path.join(dest_dir, v[2])
                v[3] = fh.copy_game_file(s, d, n)

        b = variable[0][3]
        i = variable[1][3]
        m = variable[2][3]
        t = variable[3][3]
        v = variable[4][3]
        return p, i, b, t, m, v

    def check_folders(self, src, dest_dir):
        if fh.check_folders(src, dest_dir,
                            self.img_dest_dir,
                            self.box_dest_dir,
                            self.vid_dest_dir,
                            self.marq_dest_dir,
                            self.thumb_dest_dir):
            return True
        return False

    def raise_subcollection(self):
        subcollist = self.subcol_list.split(',')
        for subcol in subcollist:
            newcolname = self.gen_raised_colname(subcol, self.src)
            proc_col_msg = 'Processing Raised Collection: ' + newcolname
            print(proc_col_msg)
            subcolpath = os.path.join(self.src, subcol)
            dest_dir = os.path.join(self.dest, newcolname)

            if self.check_folders(subcolpath, dest_dir):

                xml_path = os.path.join(dest_dir, 'gamelist.xml')
                tree = xmlh.get_gamelist(xml_path)
                xmlh.backup_xml(tree, xml_path)

                xml_path2 = os.path.join(self.src, 'gamelist.xml')
                tree2 = xmlh.get_gamelist(xml_path2)

                files = fh.get_files(subcolpath)
                files.sort()
                for file in files:
                    p, i, b, t, m, v = self.copy_raised_files(subcol, file)
                    if p:
                        subcolfile = os.path.join(subcol, p)
                        self.copy_game_media_from_tree(subcolfile, tree2,
                                                       dest_dir)

                        game1 = xmlh.get_game_by_tag_text(tree.getroot(),
                                                          'path', p)
                        game2 = xmlh.get_game_by_tag_text(tree2.getroot(),
                                                          'path', subcolfile)

                        if not game1:
                            game1 = xmlh.create_game(p)
                        xmlh.update_game1_from_game2(game1, game2)
                        tree.getroot().append(game1)

                xmlh.update_media_paths(tree, dest_dir, self.box_dest_dir,
                                        self.img_dest_dir, self.marq_dest_dir,
                                        self.thumb_dest_dir, self.vid_dest_dir)
                xmlh.save_xml(tree, xml_path)

    def copy_game_media_from_tree(self, filename, tree, dest):
        if filename:
            game = xmlh.get_game_by_tag_text(tree.getroot(), 'path', filename)
            if game:
                vs = [['box', self.box_dest_dir, '.png'],
                      ['image', self.img_dest_dir, '.png'],
                      ['marquee', self.marq_dest_dir, '.png'],
                      ['thumbnail', self.thumb_dest_dir, '.png'],
                      ['video', self.vid_dest_dir, '.mp4']]
                for v in vs:
                    if game.find(v[0]) and game.find(v[0]).text:
                        if os.path.isfile(game.find(v[0]).text):
                            n = os.path.splitext(filename)[0] + v[2]
                            fh.copy_game_file(game.find(v[0]).text,
                                              os.path.join(dest, v[1],
                                              n))

    def update_subcollection(self):
        if self.subcol_list:
            subcollist = self.subcol_list.split(',')
            for subcoltag in subcollist:
                self.update_collections(subcoltag)

    def save_results(self, tree, dest_dir, game_wihout_image,
                     game_wihout_video, game_wihout_box, game_wihout_marquee,
                     game_wihout_thumbnails, subcoltag=False):
        fh.save_txt_file(dest_dir, 'game_wihout_image.txt',
                         game_wihout_image)
        fh.save_txt_file(dest_dir, 'game_wihout_video.txt',
                         game_wihout_video)
        fh.save_txt_file(dest_dir, 'game_wihout_box.txt',
                         game_wihout_box)
        fh.save_txt_file(dest_dir, 'game_wihout_marquee.txt',
                         game_wihout_marquee)
        fh.save_txt_file(dest_dir, 'game_wihout_thumbnails.txt',
                         game_wihout_thumbnails)

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
        i = len(fh.get_files(os.path.join(dest_dir, self.img_dest_dir)))
        v = len(fh.get_files(os.path.join(dest_dir, self.vid_dest_dir)))
        b = len(fh.get_files(os.path.join(dest_dir, self.box_dest_dir)))
        m = len(fh.get_files(os.path.join(dest_dir, self.marq_dest_dir)))
        t = len(fh.get_files(os.path.join(dest_dir, self.thumb_dest_dir)))
        if subcoltag:
            f += len(fh.get_files(os.path.join(dest_dir, subcoltag)))
            i += len(fh.get_files(
                os.path.join(dest_dir, self.img_dest_dir, subcoltag)))
            v += len(fh.get_files(
                os.path.join(dest_dir, self.vid_dest_dir, subcoltag)))
            b += len(fh.get_files(
                os.path.join(dest_dir, self.box_dest_dir, subcoltag)))
            m += len(fh.get_files(
                os.path.join(dest_dir, self.marq_dest_dir, subcoltag)))
            t += len(fh.get_files(
                os.path.join(dest_dir, self.thumb_dest_dir, subcoltag)))
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
