
"""Make Description."""
import platform
import threading
from os.path import basename, join
import PySimpleGUI as sg

import json

from src.fileutils import configs
from src.collection import Collection


def make_window():
    """Make Description."""
    size_tab = (14, 1)
    size_src_dest = (61, 1)
    size_src_dirs = (73, 1)
    size_progress = (48, 10)
    size_console = (87, 15)
    if platform.system().__eq__('Windows'):
        size_tab = (14, 1)
        size_src_dest = (61, 1)
        size_src_dirs = (70, 1)
        size_progress = (43, 10)
        size_console = (86, 15)

    choose_operation = [sg.Text("Set Operation.", font=("Helvetica", 12))]

    operation = [sg.Radio('Update System', "-RADIO-", enable_events=True,
                          default=configs["gui_last_op"][0], key="-UPDATE_SYSTEM-"),
                 sg.Radio('Update Collection', "-RADIO-", enable_events=True,
                          default=configs["gui_last_op"][1], key="-UPDATE_COLLECTION-")]
    options = [sg.Checkbox("Overwrite Dest Files",
                           key="-OVERWRITE_FILES-",
                           default=configs["overwrite_file"],
                           pad=((0, 0), (0, 10))),
               sg.Checkbox("Move Source Files",
                           key="-FILE_MODE-",
                           default=True if configs["filemode"]['mode'] == 'mv' else False,
                           pad=((0, 0), (0, 10))),
               sg.Checkbox("Overwrite Existing Metadata",
                           key='-OVERWRITE_METADATA-',
                           default=configs["overwrite_gamelist_info"],
                           pad=((0, 0), (0, 10)))]

    set_src_dest = [
        sg.Text("Set Source and Destination Paths.", font=("Helvetica", 12), pad=((0, 0), (10, 0)))]

    select_src = [sg.Text("     Source", size=size_tab),
                  sg.Input(configs["gui_last_src"], key='-SOURCE-',
                           enable_events=True, size=size_src_dest),
                  sg.FolderBrowse(initial_folder=configs["gui_last_src"])]

    select_dest = [sg.Text("     Destination", size=size_tab),
                   sg.Input(configs["gui_last_dest"],
                            key='-DEST-',
                            enable_events=True,
                            size=size_src_dest),
                   sg.FolderBrowse(initial_folder=configs["gui_last_dest"],
                                   pad=((5, 0), (5, 10)))]

    src_mdir_names = [sg.Text("Source Media Folder Names.", font=("Helvetica", 12), pad=((0, 0), (10, 0))),
                      sg.Text("(Comma separated, no spaces after comma)",
                              font=("Helvetica", 8),
                              text_color='dark gray',
                              pad=((0, 0), (10, 0)))]

    select_boxart = [sg.Text("     Boxart", size=size_tab),
                     sg.Input(",".join(configs["src_media_dirs_list"]["boxart"]), key='-BOXART-', size=size_src_dirs)]

    select_img = [sg.Text("     Image", size=size_tab),
                  sg.Input(",".join(configs["src_media_dirs_list"]["image"]), key='-IMAGE-', size=size_src_dirs)]

    select_thumb = [sg.Text("     Thumbnail", size=size_tab),
                    sg.Input(",".join(configs["src_media_dirs_list"]["thumbnail"]), key='-THUMB-', size=size_src_dirs)]

    select_marc = [sg.Text("     Marquee", size=size_tab),
                   sg.Input(",".join(configs["src_media_dirs_list"]["marquee"]), key='-MARQUEE-', size=size_src_dirs)]

    select_vid = [sg.Text("     Video", size=size_tab),
                  sg.Input(",".join(configs["src_media_dirs_list"]["video"]), key='-VIDEO-', size=size_src_dirs, pad=((5, 0), (5, 10)))]

    progress_bars = [
        [sg.Text("Process Info", font=("Helvetica", 12), pad=((0, 0), (10, 0)))],
        [sg.Output(size=size_console, key='-CONSOLE-')],
        [sg.Text("Collection Progress:", size=(16, 1)),
         sg.ProgressBar(
            max_value=10, orientation='h',
            size=size_progress,
            key='-PROGRESS_COLLECTION-')],
        [sg.Text("System Progress:", size=(16, 1)),
         sg.ProgressBar(max_value=10,
                        orientation='h',
                        size=size_progress,
                        key='-PROGRESS_SYSTEM-')]
    ]

    act_buttons = [sg.Button('Ok', key='-OK_BUTTON-',
                             pad=((0, 0), (10, 0))),
                   sg.Button('Exit', key='-EXIT_BUTTON-',
                             pad=((10, 0), (10, 0))),
                   sg.Button('Stop', key='-STOP_BUTTON-',
                             visible=False,
                             pad=((10, 0), (10, 0)))]

    layout = [
        choose_operation,
        operation,
        options,
        [sg.HorizontalSeparator()],
        set_src_dest,
        select_src,
        select_dest,
        [sg.HorizontalSeparator()],
        src_mdir_names,
        select_boxart,
        select_img,
        select_thumb,
        select_marc,
        select_vid,
        [sg.HorizontalSeparator()],
        progress_bars,
        act_buttons,
    ]

    return sg.Window('SBFRM V0.5.10', layout, enable_close_attempted_event=True,
                     finalize=True, icon="logo.ico",
                     location=sg.user_settings_get_entry('-location-', (500, 500)))


def update_collection(collection, values, gui):
    """Make Description"""
    sys_paths = collection.list_systems(values['-SOURCE-'])
    progress_base = len(sys_paths)
    for sysid, sys_path in enumerate(sys_paths):
        if collection.stop:
            break
        print('\n  Processing:', sys_path)
        gui['-PROGRESS_COLLECTION-'].update(sysid, max=progress_base)
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

    main_window = make_window()
    col = None

    while True:
        # window, event, values = sg.read_all_windows()
        event, values = main_window.read()
        if event in [sg.WIN_CLOSED, '-EXIT_BUTTON-', "-WINDOW CLOSE ATTEMPTED-"]:
            configs["gui_last_op"] = [int(
                values['-UPDATE_SYSTEM-'] == True), int(values['-UPDATE_COLLECTION-'] == True)]
            configs["gui_last_src"] = values['-SOURCE-']
            configs["gui_last_dest"] = values['-DEST-']

            src_boxart_list = values['-BOXART-'].split(",")
            configs["src_media_dirs_list"]["boxart"] = src_boxart_list

            src_image_list = values['-IMAGE-'].split(",")
            configs["src_media_dirs_list"]["image"] = src_image_list

            src_marquee_List = values['-MARQUEE-'].split(",")
            configs["src_media_dirs_list"]["marquee"] = src_marquee_List

            src_thumb_list = values['-THUMB-'].split(",")
            configs["src_media_dirs_list"]["thumbnail"] = src_thumb_list

            src_video_dirs_lisr = values['-VIDEO-'].split(",")
            configs["src_media_dirs_list"]["video"] = src_video_dirs_lisr

            filemode = 'mv' if values['-FILE_MODE-'] else 'cp'
            configs["filemode"]['mode'] = filemode

            overwrite_file = 1 if values["-OVERWRITE_FILES-"] else 0
            configs["overwrite_file"] = overwrite_file

            overwrite_gamelist_info = 1 if values["-OVERWRITE_METADATA-"] else 0
            configs["overwrite_gamelist_info"] = overwrite_gamelist_info

            jsonString = json.dumps(configs, indent=4)
            jsonFile = open("config.json", "w")
            jsonFile.write(jsonString)
            jsonFile.close()
            break

        if event == '-OK_BUTTON-' and values['-UPDATE_COLLECTION-'] is True:
            print(60*'='+'\n', 'Update Collection:')
            # main_window['-STOP_BUTTON-'].update(visible=True)
            main_window['-OK_BUTTON-'].update(visible=False)
            # main_window['-EXIT_BUTTON-'].update(visible=False)
            col = Collection(main_window)
            thread = threading.Thread(
                target=update_collection, args=(col, values, main_window),
                daemon=True)
            thread.start()
            continue

        if event == '-OK_BUTTON-' and values['-UPDATE_SYSTEM-'] is True:
            # main_window['-STOP_BUTTON-'].update(visible=True)
            main_window['-OK_BUTTON-'].update(visible=False)
            # main_window['-EXIT_BUTTON-'].update(visible=False)
            col = Collection()
            thread = threading.Thread(
                target=update_sys_from, args=(col, values, main_window),
                daemon=True)
            thread.start()
            continue

        if event == '-STOP_BUTTON-':
            col.stop = True
            print("\n\n=============================================",
                  "\nHalting the Process. Please wait...",
                  "\n=============================================")
            main_window['-STOP_BUTTON-'].update(visible=False)
            main_window['-OK_BUTTON-'].update(visible=True)
            main_window['-EXIT_BUTTON-'].update(visible=True)
            continue

        if event in ['-UPDATE_SYSTEM_END-', '-UPDATE_COLLECTION_END-']:
            main_window['-PROGRESS_COLLECTION-'].update(1, max=1)
            main_window['-PROGRESS_SYSTEM-'].update(1, max=1)
            main_window['-STOP_BUTTON-'].update(visible=False)
            main_window['-OK_BUTTON-'].update(visible=True)
            main_window['-EXIT_BUTTON-'].update(visible=True)
            continue

    main_window.close()


if __name__ == '__main__':
    main()
