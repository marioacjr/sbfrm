
"""Make Description."""

import threading
from os.path import basename, join
import PySimpleGUI as sg

import json

from src.fileutils import configs
from src.collection import Collection

from time import sleep


def make_window():
    """Make Description."""
    last_up_col = sg.user_settings_get_entry('-last up_col-', '')
    last_up_sys = sg.user_settings_get_entry('-last up_sys-', '')
    if not last_up_col and not last_up_sys:
        last_up_col = False
        last_up_sys = True
    
    choose_operation = [sg.Text("Choose Operation.", font=("Helvetica", 12))]
    
    operation = [[sg.Radio('Update System', "-RADIO-",
                           default=last_up_sys, key="-UPDATE_SYSTEM-"),
                 sg.Radio('Update Collection', "-RADIO-",
                           default=last_up_col, key="-UPDATE_COLLECTION-")]]
    
    set_src_dest = [sg.Text("Set Source and Destination Paths.", font=("Helvetica", 12))]

    select_src = [sg.Text("     Source", size=(13, 1)),
                  sg.Input(configs["gui_last_src"], key='-SOURCE-', enable_events=True),
                  sg.FolderBrowse(initial_folder=configs["gui_last_src"])]

    select_dest = [sg.Text("     Destination", size=(13, 1)),
                   sg.Input(configs["gui_last_dest"], key='-DEST-'),
                   sg.FolderBrowse(initial_folder=configs["gui_last_dest"])]
    
    src_mdir_names = [sg.Text("Source Media Folder Names.", font=("Helvetica", 12)),
         sg.Text("(Comma separated, no spaces after comma)",
                 font=("Helvetica", 8),
                 text_color='dark gray')]

    select_boxart = [sg.Text("     Boxart", size=(13, 1)),
                     sg.Input(",".join(configs["src_media_dirs_list"]["boxart"]), key='-BOXART-', size=(57, 1))]

    select_img = [sg.Text("     Image", size=(13, 1)),
                  sg.Input(",".join(configs["src_media_dirs_list"]["image"]), key='-IMAGE-', size=(57, 1))]

    select_thumb = [sg.Text("     Thumbnail", size=(13, 1)),
                    sg.Input(",".join(configs["src_media_dirs_list"]["thumbnail"]), key='-THUMB-', size=(57, 1))]

    select_marc = [sg.Text("     Marquee", size=(13, 1)),
                   sg.Input(",".join(configs["src_media_dirs_list"]["marquee"]), key='-MARQUEE-', size=(57, 1))]

    select_vid = [sg.Text("     Video", size=(13, 1)),
                  sg.Input(",".join(configs["src_media_dirs_list"]["video"]), key='-VIDEO-', size=(57, 1))]
    
    act_buttons = [sg.Button('Ok'), sg.Button('Exit')]
    layout = [
        choose_operation,
        operation,
        set_src_dest,
        select_src,
        select_dest,
        src_mdir_names,
        select_boxart,
        select_img,
        select_thumb,
        select_marc,
        select_vid,
        act_buttons,
    ]

    return sg.Window('SBFRM V0.5.5', layout, enable_close_attempted_event=True,
                     finalize=True, icon="logo.ico",
                     location=sg.user_settings_get_entry('-location-', (300, 300)))


def make_progress_window(location):
    """Make Description"""
    layout = [
        [sg.Output(size=(72, 6), key='-CONSOLE-')],
        [sg.Text("Collection Progress:", size=(16, 1)), sg.ProgressBar(
            max_value=10, orientation='h', size=(37, 10),
            key='-PROGRESS_SYSTEMS-')],
        [sg.Text("System Progress:", size=(16, 1)), sg.ProgressBar(
            max_value=10, orientation='h', size=(37, 10),
            key='-PROGRESS_GAMES-')],
        [sg.Button('Cancel')]
    ]
    return sg.Window('Progress', layout, enable_close_attempted_event=True,
                     location=location, modal=True, finalize=True)


def update_collection(collection, values, gui):
    """Make Description"""    
    print(60*'='+'\n', 'Update Collection:')

    sys_paths = collection.list_systems(values['-SOURCE-'])
    progress_base = len(sys_paths)
    for sysid, sys_path in enumerate(sys_paths):
        if collection.stop_copy:
            break
        print('\n  Processing:', sys_path)
        gui.write_event_value('-PROGRESS_SYSTEMS-', [sysid, progress_base])
        src_path = join(values['-SOURCE-'], sys_path)
        dest_path = join(values['-DEST-'], sys_path)
        collection.update_sys_from(dest_path, src_path, gui=gui)

    gui.write_event_value('-UPDATE_COLLECTION_END-', '')


def update_sys_from(collection, values, gui):
    """Make Description"""
    print(60*'='+'\n', 'Update System:', values['-DEST-'])

    collection.update_sys_from(values['-DEST-'], values['-SOURCE-'], gui=gui)

    gui.write_event_value('-UPDATE_SYSTEM_END-', '')


def main():
    """Make Description."""    
    sg.theme('DarkAmber') 

    window1, window2 = make_window(), None
    col = None

    while True:
        window, event, values = sg.read_all_windows()
        if event in [sg.WIN_CLOSED, 'Exit']:
            # The line of code to save the position before exiting
            last = window1.current_location()
            sg.user_settings_set_entry('-location-', last)

            last = values['-UPDATE_COLLECTION-']
            sg.user_settings_set_entry('-last up_col-', last)

            last = values['-UPDATE_SYSTEM-']
            sg.user_settings_set_entry('-last up_sys-', last)
            
            configs["gui_last_src"] = values['-SOURCE-']
            configs["gui_last_dest"] = values['-DEST-']
            configs["src_media_dirs_list"]["boxart"] = values['-BOXART-'].split(",")
            configs["src_media_dirs_list"]["image"] = values['-IMAGE-'].split(",")
            configs["src_media_dirs_list"]["marquee"] = values['-MARQUEE-'].split(",")
            configs["src_media_dirs_list"]["thumbnail"] = values['-THUMB-'].split(",")
            configs["src_media_dirs_list"]["video"] = values['-VIDEO-'].split(",")
            jsonString = json.dumps(configs, indent=4)
            jsonFile = open("config.json", "w")
            jsonFile.write(jsonString)
            jsonFile.close()
            
            window.close()
            if window == window2:
                window2 = None
            elif window == window1:
                break

        if event in ['-UPDATE_COLLECTION-', '-UPDATE_SYSTEM-']:
            last = values['-UPDATE_COLLECTION-']
            sg.user_settings_set_entry('-last up_col-', last)

            last = values['-UPDATE_SYSTEM-']
            sg.user_settings_set_entry('-last up_sys-', last)

        if event in ['-SOURCE-', '-DEST-']:
            sg.user_settings_set_entry('-last source-', values['-SOURCE-'])
            sg.user_settings_set_entry('-last dest-', values['-DEST-'])

        if event == 'Ok' and values['-UPDATE_COLLECTION-'] is True:
            xpos, ypos = window1.current_location()
            xpos += 30
            ypos += 300
            window2 = make_progress_window((xpos, ypos))
            col = Collection(window)
            thread = threading.Thread(
                target=update_collection, args=(col, values, window),
                daemon=True)
            thread.start()

        if event == 'Ok' and values['-UPDATE_SYSTEM-'] is True:
            xpos, ypos = window1.current_location()
            xpos += 30
            ypos += 300
            window2 = make_progress_window((xpos, ypos))
            col = Collection()
            thread = threading.Thread(
                target=update_sys_from, args=(col, values, True),
                daemon=True)
            thread.start()

        if event == 'Cancel':
            print("\n\n=============================================",
                  "\nHalting the Process. Please wait...",
                  "\n=============================================")
            col.stop_copy = True
        

        if event == '-PROGRESS_GAMES-':
            window2[event].update_bar(values[event][0], max=values[event][1])

        if event == '-PROGRESS_SYSTEMS-':
            window2[event].update_bar(values[event][0], max=values[event][1])

        if event in ['-UPDATE_SYSTEM_END-', '-UPDATE_COLLECTION_END-']:
            print('\nFinished!\n')
            window2.close()

    window1.close()


if __name__ == '__main__':
    main()
