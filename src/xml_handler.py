import os
import xml.dom.minidom
from datetime import datetime
import xml.etree.ElementTree as ET

media_tags = ['path', 'boxarts', 'image', 'video', 'marquee', 'thumbnail']


def get_gamelist(path):
    if not os.path.isfile(path):
        s = '<?xml version="1.0" encoding="UTF-8"?><gameList></gameList>'
        f = open(path, "w")
        f.write(s)
        f.close()
    tree = ET.parse(path)
    root = tree.getroot()
    return tree


def pretty_print_xml_given_root(root, output_xml):
    """
    Useful for when you are editing xml data on the fly
    """
    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
    # remove the weird newline issue
    xml_string = os.linesep.join([s for s in xml_string.splitlines() if s.strip()])
    with open(output_xml, "w", encoding="utf-8") as file_out:
        file_out.write(xml_string)


def pretty_print_xml_given_file(input_xml, output_xml):
    """
    Useful for when you want to reformat an already existing xml file
    """
    tree = ET.parse(input_xml)
    root = tree.getroot()
    pretty_print_xml_given_root(root, output_xml)


def save_xml(xml_tree, path):
    xml_tree.write(path)
    pretty_print_xml_given_file(path, path)


def backup_xml(tree, path):
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    bkp_path = path.replace('.xml', '_'+now+'.xml')
    save_xml(tree, bkp_path)


def create_game(p, i=False, t=False, b=False, m=False, v=False):
    game = ET.Element('game')

    path = ET.SubElement(game, 'path')
    path.text = p

    if i:
        img = ET.SubElement(game, 'image')
        img.text = i

    if t:
        thumb = ET.SubElement(game, 'thumbnail')
        thumb.text = t

    if b:
        box = ET.SubElement(game, 'box')
        box.text = b

    if m:
        marq = ET.SubElement(game, 'marquee')
        marq.text = m

    if v:
        vid = ET.SubElement(game, 'video')
        vid.text = v

    return game


def get_game_by_tag_text(root, tag, text):
    for game in root:
        if game.find(tag) is not None:
            if game.find(tag).text is not None:
                g_tag_text = game.find(tag).text.replace('./', '')
                text = text.replace('./', '')
                if tag == 'path':
                    g_tag_text = os.path.splitext(g_tag_text)[0]
                    text = os.path.splitext(text)[0]
                if g_tag_text == text:
                    return game
    return False


def update_game1_from_game2(game1, game2):
    if game2:
        for e2 in game2:
            if e2.tag not in media_tags:
                e1 = game1.find(e2.tag)
                if e1 is not None:
                    game1.append(e2)
                else:
                    if game1.find(e2.tag) is not None:
                        if game1.find(e2.tag).text is not None:
                            game1.find(e2.tag).text = game2.find(e2.tag).text


def update_root_from_game(root, game):
    tag = 'path'
    if game.find(tag) is not None and game.find(tag).text is not None:
        path_text = game.find(tag).text
        g = get_game_by_tag_text(root, tag, path_text)
        if g is not False:
            update_game1_from_game2(g, game)


def update_tree1_from_tree2(tree1, tree2):
    root1 = tree1.getroot()
    for game2 in tree2.getroot():
        update_root_from_game(root1, game2)


def set_element_by_tag(game, tag, t):
    t = t.replace('./', '')
    t = './' + t
    if game.find(tag) is not None:
        game.find(tag).text = t
    else:
        e = ET.SubElement(game, tag)
        e.text = t


def update_media_paths(tree, dest_dir, dest_box, dest_img, dest_marq,
                       dest_thumb, dest_video):
    for game in tree.getroot():
        if game.find('path') is not None:
            game_path = game.find('path').text
            game_path = game_path.replace('./', '')
            n = os.path.splitext(game_path)[0]
            media_file = n + '.png'

            s = os.path.join(dest_dir, game_path)
            tag = 'path'
            if os.path.isfile(s):
                set_element_by_tag(game, tag, game_path)

            s = os.path.join(dest_dir, dest_box, media_file)
            tag = 'box'
            if os.path.isfile(s):
                s = os.path.join(dest_box, media_file)
                set_element_by_tag(game, tag, s)

            s = os.path.join(dest_dir, dest_img, media_file)
            tag = 'image'
            if os.path.isfile(s):
                s = os.path.join(dest_img, media_file)
                set_element_by_tag(game, tag, s)

            s = os.path.join(dest_dir, dest_marq, media_file)
            tag = 'marquee'
            if os.path.isfile(s):
                s = os.path.join(dest_marq, media_file)
                set_element_by_tag(game, tag, s)

            s = os.path.join(dest_dir, dest_thumb, media_file)
            tag = 'thumbnail'
            if os.path.isfile(s):
                s = os.path.join(dest_thumb, media_file)
                set_element_by_tag(game, tag, s)

            media_file = n + '.mp4'
            s = os.path.join(dest_dir, dest_video, media_file)
            tag = 'video'
            if os.path.isfile(s):
                s = os.path.join(dest_video, media_file)
                set_element_by_tag(game, tag, s)


def get_tree_details(tree):
    r = tree.getroot()
    g = len(r)
    i = len(r.findall('game/image'))
    v = len(r.findall('game/video'))
    b = len(r.findall('game/box'))
    m = len(r.findall('game/marquee'))
    t = len(r.findall('game/thumbnail'))
    d = len(r.findall('game/desc'))
    return g, i, v, b, m, t, d
