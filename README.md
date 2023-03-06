# **SBFRM**

[Versão em Português](README_Pt-Br.md) |
[Changelog](CHANGELOG.md) |
[Use Examples](examples/)

## A Manager for Retrogames Collections.

This manager is used for collections in the EmulationStation format (those with a gamelist.xml file inside). It is quite simple but at the same time very powerful. Initially it was just a script to do very simple things to help me organize my game collections (I'm that hoarder guy, you know :). Over time I kept adding more features until I realized it was already pretty robust and could be useful for the community.

### The main features are:
- Merge a Source collection into a Destination collection;
- Avoid duplication of roms and their associated media;
- Avoid orphaned image and video files (without a relative game);
- Avoid wasted disk space;
- Locate the media files of a game and automatically include them in the gamelist.xml.
- Generate the small but complete gamelist.xml file.
- Reduce the time needed to scrapper collections by reusing existing information.

# Releases:

## Executable:

To use it, simply download the binary for your O.S. into the [releases](releases/) folder and run it. The binary was compiled from this python code and requires no requirements to run.

![Execute GUI](srfrm_gui.png)

### Requirements:
- Linux or Windows.

## Command line:

To use it, you must have Python3 or higher installed. Run the script [sbfrm.py](sbfrm.py), passing in the arguments as shown below. The required dependencies are listed in the requirements.txt file. It is advisable to create a virtual environment for the installation of the dependencies (this avoids the dependency packages being installed directly in your O.S. python installation).

### CLI:
    `python3 sbfrm.py update_collection src-collection-path/ dest-collection-path/`

### GUI:
    `python3 sbfrm_gui.py` 

### Requirements:
- Python3;
- Linux or Windows.
- Packages:
    - PySimpleGUI (only for sbfrm_gui.py).

See [examples](examples).

## About this Project
The **SBFRM**, is a python script, where you must pass some parameters on the command line to perform the tasks you want.

#### The simplest way to run it is:

    `python3 sbfrm.py update_collection src-collection-path/ dest-collection-path/`

#### Where:
- **update_collection** is the task you wish to perform. In this case, it is to add new roms to your collection;
- src-collection-path**: is the path to the source collection you wish to add;
- **dest-collection-path**: is the path to your collection where the files will be added and the gamelist.xml generated or updated;

Run the above command and watch magic happen. The run will automatically add new roms to your collection. It will also update the existing gamelist.xml file, or create a new one if it does not exist. The goal of the process is to avoid duplicate games and orphaned media.

#### The folder structure in the example above should look like this.

- src-collection-path
    - system_one/
        - Game AA (Europe, Japan).zip
        - Game AA (Europe, Japan) (Demo).zip
        - Game AA (Japan).zip
        - Game AA (USA).zip
        - Game AA (USA, Europe, Japan).zip
        - GAMEBB.zip
        - GAMEBBBB.zip
        - gamelist.xml
    - system_two/
        - Game CC (Europe, Japan).zip
        - Game CC (Europe, Japan) (Demo).zip
        - Game CC (USA).zip
        - GAMEDD.zip
        - GAMEDDDD.zip
        - gamelist.xml


- dest-collection-path/
    - system_one/
        - Game AA (Japan).zip
        - gamelist.xml
    - system_three/
        - Game EE (Europe, Japan).zip
        - Game EE (USA).zip
        - gamelist.xml

#### The execution of the script will perform the following work:

- In the **system_one/** folder of the target collection, the rom **Game AA (USA).zip** and **GAMEBB.zip** will be added. The rom **Game AA (Japan).zip** will be removed, because its version (USA) was found in the source collection. All image and video media and metadata related to both roms will be copied to the target collection. Similarly, all media and metadata associated with the rom **Game AA (Japan).zip** will be moved to the backup folder **system_one_removed/**;
- A folder for the **system_two/** system will be created. The roms **Game CC (USA).zip** and **GAMEDD.zip** will be copied. All media and metadata files associated with these two roms will be copied.
- The **system_three/** folder of the target collection will not change at all.


#### The final result of your collection will be as shown below:

- dest-collection-path/
    - system_one/
        - Game AA (USA).zip
        - GAMEBB.zip
        - gamelist.xml
    - system_three/
        - Game CC (USA).zip
        - GAMEDD.zip
        - gamelist.xml
    - system_three/
        - Game EE (Europe, Japan).zip
        - Game EE (USA).zip
        - gamelist.xml

#### Mandatory Parameters:
- **op**: Operation to be performed.
    - **update_collection**: Updates, in **dest-collection-path/**, all roms, images and video files for each system in the collection present in **src-collection-path/**. Updates the **gamelist.xml** for each system, or creates a new one if it doesn't exist;
    - **update_system**: Updates the respective system, or creates a new one if it does not exist. ;
- src-collection-path/**: Path to the directory where the collection to be added is located.
    - Ex: /media/user/SHARE1/roms
- dest-collection-path/**: Path of the directory where the files are to be added.
    - Ex: /media/user/SHARE/roms

#### Optional Settings:
It is possible to customize some operations before execution, such as region priority of the roms and name of the collections' media folders. These customizations must be made by changing their parameters in the file **configs.json**. This file must follow the pre-established structure existing in JSON format. The behavior of each of these parameters is described below.

- **-src_media_dirs_list**: Contains the list of folders where the script should look for the media associated with the roms in the source collection. Within each list of its sub items, the name of the folder where the media of that type are located should be entered.

- **-dest_media_dirs_names**: Contains the folder names of the media in the target collection. Each media type must contain one, and only one, name for the media of that type.

- **filemode**: Defines the type of operation performed from the source collection to the target collection. Under **options** are the available operation options (**this parameter should not be changed**). In **mode** the desired type must be informed. The **cp** type copies the files from the source to the destination. This type of operation is safer, but slower. The **mv** type moves files from the source to the destination. This mode is faster when the source and destination are located on the same partition.

- **-overwrite_file**: Defines whether the destination file should be overwritten, if it exists. Change this parameter to 0 (zero) if you do not want to overwrite and to 1 (um) otherwise.

- **overwrite_gamelist_info**: Defines whether the target's **gamelist.xml** metadata should be overwritten by the new data located at the source

- **verbose**: Defines whether to generate textual output on execution teminal or user gui.

- **region_order**: Defines the priority list of rom regions to be kept in the destination collection. The first item in this list has a higher priority than the second, and so on. Each item in this list must appear in parentheses in the roms name.

- **removed_devcomm_status**: Contains the list of the development and commercial status of the roms to be removed from the target collection. Each item in this list must appear in parentheses in the rom name.

## Collection Reporting and Organization of Media Files


After the script is processed, a set of text files with information about the totals of missing media files will be created for each of the collections present in **dest/**. These files are very useful for identifying and adding what is missing in the collection. For example, through them you can create a task force to complete all missing information in a collection.

Will also backup the previous **gamelist.xml** to avoid as much as possible the loss of information if a problem occurs.

## Final Considerations

Far be it from me to think that this is a spectacular project and that there is no other equal or better. There is a lot that can be improved, certainly there are bugs that I didn't notice, a lot of code refactoring to be done, more tests to be implemented, etc, etc. Anyway, I hope it is useful to you and help you save a lot of disk space and time organizing your roms. Time that should be used for playing and having fun.

If you have come so far it is because you are really interested in my work and are probably wondering what the hell **sbfrm** stands for, which is an acronym for Small Big Fucking Retro Gamelist Manager. Yes, I was very inspired when searching for a name for this project :p

Otherwise, here are my ideas for future work to be implemented (when I have some time to spare):
- Improve the duplicate file comparison. The current comparison, although simple, has good results but certainly has a lot of improvement to do.
- Implement a priority system for the roms language.
- Write a better document with examples and tricks of cool stuff that is possible to do with **sbfrm**.
- Improve my english :p

Donations:

    "I have no special talent. I'm just passionately curious."
    -Albert Einstein

Would you like to see this project continue to evolve? Your help will be very welcome!

https://www.paypal.com/donate?hosted_button_id=G7KRYRNQ247AG

![PayPal Donation](qrcode.png)