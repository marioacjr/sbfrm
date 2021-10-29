import os
import shutil

def check_folders(src, dest, ifn, bfn, vfn, mfn, tfn, subsystemtag=False):
    if subsystemtag:
        src = os.path.join(src, subsystemtag)

    if os.path.isdir(src):
        if subsystemtag:
            ifn = os.path.join(ifn, subsystemtag)
            bfn = os.path.join(bfn, subsystemtag)
            vfn = os.path.join(vfn, subsystemtag)
            mfn = os.path.join(mfn, subsystemtag)
            tfn = os.path.join(tfn, subsystemtag)
            if not os.path.isdir(os.path.join(dest, subsystemtag)):
                os.makedirs(os.path.join(dest, subsystemtag))
        else:
            if not os.path.isdir(dest):
                os.makedirs(dest)

        if not os.path.isdir(os.path.join(dest, ifn)):
            os.makedirs(os.path.join(dest, ifn))
        if not os.path.isdir(os.path.join(dest, bfn)):
            os.makedirs(os.path.join(dest, bfn))
        if not os.path.isdir(os.path.join(dest, vfn)):
            os.makedirs(os.path.join(dest, vfn))
        if not os.path.isdir(os.path.join(dest, mfn)):
            os.makedirs(os.path.join(dest, mfn))
        if not os.path.isdir(os.path.join(dest, tfn)):
            os.makedirs(os.path.join(dest, tfn))
        return True
    else:
        return False


def get_files(path, subsystemtag=False):
    if subsystemtag:
        path = os.path.join(path, subsystemtag)
    l = list()
    try:
        if os.path.isdir(path) and len(os.listdir(path)) > 0:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            for file in files:
                if not excluded_file(file):
                    l.append(file)
    except Exception as e:
        print(e)
    l.sort()
    return l


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_folders(path):
    folders = list()
    for folder in os.listdir(path):
        if not excluded_folder(folder):
            p = os.path.join(path, folder)
            if len(get_files(p)) > 0:
                folders.append(folder)
    folders.sort()
    return folders


def excluded_folder(folder):
    if '.' == folder[0]:
        return True
    for e in ['backup', 'bezels', 'BGM', 'bios', 'System Volume Information',
              'mplayer', 'downloads', 'scummvm', 'ports', 'model2', 'model3',
              'windows']:
        if e in folder:
            return True
    return False


def excluded_file(file):
    for e in ['.xml', '.txt', '.state', '.nvmem', '.cfg', '.txt', '.eeprom',
              '.srm']:
        if e in file:
            return True
    return False


def dest_has_same_file_name(dest, file):
    files = get_files(dest)
    files.sort()

    n1 = os.path.splitext(file)[0]
    n1 = n1.split('(')[0]
    n1 = n1.lower()

    for f in files:
        n2 = os.path.splitext(f)[0]
        n2 = n2.split('(')[0]
        n2 = n2.lower()

        if n1 == n2:
            return True

        symbols = ['.', ',', '-', "'", '_', '&', '!', ' ']
        for s in symbols:
            n1 = n1.replace(s, '')
            n2 = n2.replace(s, '')
        if n1 == n2:
            return True
    return False


def copy_game_file(source, dest, file, subsystemtag=False, op="cp"):
    c1 = not excluded_file(file)
    c2 = not dest_has_same_file_name(dest, file)

    e = os.path.join(source, file)
    s = os.path.join(dest, file)
    r = file
    if subsystemtag:
        e = os.path.join(source, subsystemtag, file)
        s = os.path.join(dest, subsystemtag, file)
        r = os.path.join(subsystemtag,file)

    if c1 and c2 and os.path.isfile(e):
        if op == 'mv':
            shutil.move(e, s)
        else:
            shutil.copyfile(e, s)
        return r
    return False


def copy_game_media(filename, ext, scr_folder, src_media_folder, dest_folder, media_folder, subsystemtag=False, op="cp"):
    n = os.path.splitext(filename)[0] + ext
    if subsystemtag:
        n = os.path.join(subsystemtag, n)
    s = os.path.join(dest_folder, media_folder, n)
    c1 = src_media_folder
    if c1:
        c2 = os.path.isfile(os.path.join(scr_folder, c1, n))
        if c2:
            if op == 'mv':
                shutil.move(os.path.join(scr_folder, c1, n), s)
            else:
                shutil.copyfile(os.path.join(scr_folder, c1, n), s)
            return os.path.join(media_folder, n)
    return False


def copy_game_media_by_gamelistfile(tree, file, tag, ext, src_folder, src_image_folder, dest_folder, image_folder_name, subsystemtag=False, op="cp"):
    root = tree.getroot()
    for g in root:
        if g.find('path') != None:
            path = g.find('path').text.replace('./', '')
            file = file.replace('./', '')
            if file == path:
                if g.find(tag) != None and g.find(tag).text != None:
                    img = g.find(tag).text.replace('./', '')
                    if os.path.isfile(os.path.join(src_folder, img)):
                        n = os.path.splitext(file)[0] + ext
                        s = os.path.join(dest_folder, image_folder_name, n)
                        r = os.path.join(image_folder_name, n)
                        if subsystemtag:
                            s = os.path.join(dest_folder, image_folder_name, subsystemtag, n)
                            r = os.path.join(image_folder_name, subsystemtag, n)
                        if op == 'mv':
                            shutil.move(os.path.join(src_folder, img), s)
                        else:
                            shutil.copyfile(os.path.join(src_folder, img), s)
                        return r
    return False


def save_txt_file(fpath, fname, data):
    f = open(os.path.join(fpath, fname), 'w')
    f.write(data)
    f.close()
