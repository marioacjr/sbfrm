
"""Make Description."""

from os.path import basename, join
import PySimpleGUI as sg

from src.collection import Collection


sg.theme('DarkAmber')  # please make your windows colorful

operation = [[sg.Radio('Update Collection', "-RADIO-", default=True),
              sg.Radio('Update System', "-RADIO-")]]
select_src = [sg.Text("     Source", size=(15, 1)),
              sg.Input(sg.user_settings_get_entry('-last source-', ''),
              key='-SOURCE-', enable_events=True),
              sg.FolderBrowse(initial_folder=sg.user_settings_get_entry('-last source-', ''))]
select_dest = [sg.Text("     Destination", size=(15, 1)),
               sg.Input(sg.user_settings_get_entry('-last dest-', ''),
               key='-DEST-'),
               sg.FolderBrowse(initial_folder=sg.user_settings_get_entry('-last dest-', ''))]
select_boxart = [sg.Text("     Boxart", size=(15, 1)),
                 sg.Input(sg.user_settings_get_entry('-last boxarts-', ''),
                 key='-BOXART-', enable_events=True),
                 sg.FolderBrowse()]
select_img = [sg.Text("     Image", size=(15, 1)),
              sg.Input(sg.user_settings_get_entry('-last images-', ''),
              key='-IMAGE-', enable_events=True),
              sg.FolderBrowse()]
select_thumb = [sg.Text("     Thumbnail", size=(15, 1)),
                sg.Input(sg.user_settings_get_entry('-last thumbs-', ''),
                key='-THUMB-', enable_events=True),
                sg.FolderBrowse()]
select_marc = [sg.Text("     Marquee", size=(15, 1)),
               sg.Input(sg.user_settings_get_entry('-last marquees-', ''),
                        key='-MARQUEE-',
                        enable_events=True),
               sg.FolderBrowse()]
select_vid = [sg.Text("     Video", size=(15, 1)),
              sg.Input(sg.user_settings_get_entry('-last videos-', ''),
              key='-VIDEO-', enable_events=True),
              sg.FolderBrowse()]
subsystems = [sg.Text("     Subsystems", size=(15, 1)),
              sg.Multiline(sg.user_settings_get_entry('-last subsystems-', ''),
              key='-SUBSYSLIST-', size=(42, 6))]
layout = [
    [sg.Text("Choose Operation.", font=("Helvetica", 12))],
    operation,
    [sg.Text("Set Source and Destination Paths.", font=("Helvetica", 12))],
    select_src,
    select_dest,
    [sg.Text("Set the System Media Folder Source Names.", font=("Helvetica", 12))],
    select_boxart,
    select_img,
    select_thumb,
    select_marc,
    select_vid,
    [sg.Text("Set the SubSystems Names.", font=("Helvetica", 12)),
     sg.Text("(One per line, no spaces)",
             font=("Helvetica", 8), text_color='dark gray')],
    subsystems,
    [sg.Button('Ok'), sg.Button('Exit')],
    [sg.Output(size=(72, 6), key='-CONSOLE-', visible=False)],
    [sg.ProgressBar(max_value=10, orientation='h',
                    size=(50, 10), key='-PROGRESS-',
                    visible=False)]
]

window = sg.Window('SBFRM V0.4.0', layout, enable_close_attempted_event=True,
                   location=sg.user_settings_get_entry('-location-', (None, None)))

while True:
    event, values = window.read()
    if event in [sg.WINDOW_CLOSE_ATTEMPTED_EVENT, 'Exit']:
        # The line of code to save the position before exiting
        sg.user_settings_set_entry('-location-', window.current_location())
        sg.user_settings_set_entry('-last source-', values['-SOURCE-'])
        sg.user_settings_set_entry('-last dest-', values['-DEST-'])
        sg.user_settings_set_entry('-last boxarts-', values['-BOXART-'])
        sg.user_settings_set_entry('-last images-', values['-IMAGE-'])
        sg.user_settings_set_entry('-last thumbs-', values['-THUMB-'])
        sg.user_settings_set_entry('-last marquees-', values['-MARQUEE-'])
        sg.user_settings_set_entry('-last videos-', values['-VIDEO-'])
        sg.user_settings_set_entry('-last subsystems-', values['-SUBSYSLIST-'])
        break
    if event in ['-SOURCE-', '-DEST-']:
        sg.user_settings_set_entry('-last source-', values['-SOURCE-'])
        sg.user_settings_set_entry('-last dest-', values['-DEST-'])
    if event in ['-BOXART-', '-IMAGE-', '-THUMB-', '-MARQUEE-', '-VIDEO-']:
        values[event] = basename(values[event])
        window[event].update(values[event])
    if event == 'Ok' and values[0] is True:
        mdirs = {"boxart": values['-BOXART-'],
                 "image": values['-IMAGE-'],
                 "marquee": values['-THUMB-'],
                 "thumbnail": values['-MARQUEE-'],
                 "video": values['-VIDEO-']}
        subsyslist = values['-SUBSYSLIST-'].splitlines()
        col = Collection()
        print('============================================================\n',
              'Update Collection:')
        window.Element('-CONSOLE-').Update(visible=True)
        window.Element('-PROGRESS-').Update(visible=True)
        window['-PROGRESS-'].update_bar(0)
        sys_paths = col.list_systems(values['-SOURCE-'])
        progress_base = len(sys_paths)
        for sysid, sys_path in enumerate(sys_paths):
            print('\n  Processing:', sys_path)
            window['-PROGRESS-'].update_bar(sysid, max=progress_base)
            src_path = join(values['-SOURCE-'], sys_path)
            dest_path = join(values['-DEST-'], sys_path)
            col.update_sys_from(dest_path, src_path, mdirs,
                                subsyslist=subsyslist, verbose=False)
        window['-PROGRESS-'].update_bar(progress_base, max=progress_base)
        print('Finished!:')

    if event == 'Ok' and values[1] is True:
        print('Update System:', values['-DEST-'])
        window['-PROGRESS-'].update_bar(0.1, max=progress_base)
        col = Collection()
        media_dirs = {"boxart": values['-BOXART-'],
                      "image": values['-IMAGE-'],
                      "marquee": values['-THUMB-'],
                      "thumbnail": values['-MARQUEE-'],
                      "video": values['-VIDEO-']}
        col.update_sys_from(values['-DEST-'], values['-SOURCE-'], media_dirs,
                            verbose=False)
        print('Finished!:')

window.close()
