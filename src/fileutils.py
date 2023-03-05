import re
import json
import shutil
from glob import glob
from datetime import datetime
from os import listdir, makedirs, remove
from os.path import isfile, join, basename, splitext

import xml.etree.ElementTree as ET
import xml.dom.minidom as xdm

configs = json.loads(open("config.json", 'r', encoding="utf8").read())

def list_files(path):
    """Make Description."""
    return [f for f in listdir(path) if isfile(join(path, f))]


def file_name(path):
    """Make Description."""
    return splitext(basename(path))[-2]


def file_extension(path):
    """Make Description."""
    return splitext(basename(path))[-1]


def backup_gamelist(path):
    """Make Description."""
    tree = ET.parse(path)
    root = tree.getroot()
    dt_now = '_' + str(datetime.now().strftime("%Y%m%d%H%M%S"))
    bkp_path = path.replace('.xml', dt_now+'.xml')
    with open(bkp_path, "w", encoding="utf-8") as file_out:
        prettyxml = xdm.parseString(ET.tostring(root)).toprettyxml()
        file_out.write(prettyxml)


def get_file_name(path):
    """Make Description."""
    return splitext(basename(path))[-2]


def get_file_extension(path):
    """Make Description."""
    return splitext(basename(path))[-1]


def dest_has_same_file(src_file_path, dest_dir):
    """Make Description."""
    src_filename = basename(src_file_path)
    dest_path = join(dest_dir, src_filename)
    return isfile(dest_path)


def dest_has_same_filename(src_file_path, dest_dir):
    """Make Description."""
    src_filename = get_file_name(basename(src_file_path))
    dest_names = [get_file_name(basename(f)) for f in listdir(dest_dir) if isfile(join(dest_dir, f))]
    return src_filename in dest_names


def get_config_item_list(name):
    """Make Description."""
    region_lang_list = re.findall(r'\(.*?\)', name)
    config_item_list = []
    for text in region_lang_list:
        text = text.replace("(", "").replace(")", "").replace(" ", "")
        text = text.split(",")
        config_item_list.extend(text)
    return config_item_list


def find_same_games(path, name):
    """Make Description."""
    text = file_name(name)
    ocur = [m.start() for m in re.finditer('\(', text)]    
    
    if len(ocur)>0:
        text = text[:ocur[0]+1]
    
    filelist = glob(join(path, text+"*"))
    for file_id, file in enumerate(filelist):
        filelist[file_id] = basename(file)
        
    return filelist

def merge_file(src_file, dest_path):
    """Make Description."""
    if configs["filemode"]['mode'] == "cp":
        shutil.copy(src_file, dest_path)
    elif configs["filemode"]['mode'] == "mv":
        shutil.move(src_file, dest_path)


def remove_file(path):
    """Make Description."""
    if isfile(path):
        remove(path)


def make_sys_dirs(path):
        """Make Description."""
        makedirs(path, exist_ok=True)

        for value in configs["dest_media_dirs_names"].values():
            mpath = join(path, value)
            makedirs(mpath, exist_ok=True)