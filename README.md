# **SBFRM**

[Versão em Português](README_Pt-Br.md)

## A Manager for Retrogames Collections.

This manager is applied to collections in EmulationStation format (those with a gamelist.xml file inside). It is quite simple but at the same time very powerful. Initially it was just a script to do very simple things to manage my game collections (I am a game accumulator guy :). Over time I kept adding more features until I realized it was quite robust and could be useful for the community.

### The main features are:
- Merge collections;
- Avoid duplicate games;
- Avoid orphaned image and video files;
- Avoid wasting disk space;
- And, most importantly, generate the gamelist.xml file automatically.

Actually it is still a python script, where you must enter several parameters in the input to perform the tasks you want.

####  The simplest way to run:

`sudo python3 colection_handler.py update_collections src-collection/ dest-collection/`

####  Where:
- **update_collections** is the task you want to perform. In this case it is to add new roms to your collection;
- **src-collection/** is the path of the collection you want to add;
- **dest-collection/** is the path to your collection where the files will be added and the gamelist.xml generated or updated;

Run the command above and watch the magic happen. The run will automatically add new roms to your collection (without any image or video media in this case). It will also update the existing gamelist.xml file, or create a new one if it doesn't exist. The idea is, as far as possible, to avoid duplicate games, both in the files and in gamelist.xml

####  The folder structure in the example above should look similar to this.

- src-collection/
    - snes/
        - Name1 (USA,Japan).zip
        - Name2 (USA,Europe) (En,Fr,De).zip
        - Name3 (USA,Europe,Japan).zip
        - gamelist.xml
    - mastersystem/
        - Name4 (USA,Japan).zip
        - Name5 (USA) (En,Fr,De).zip
        - Name6 (USA,Europe,Japan).zip
        - gamelist.xml
    - megadrive/
        - Name7 (USA,Japan).zip
        - Name8 (USA) (En,Fr,De).zip
        - Name9 (USA,Europe,Japan).zip
        - gamelist.xml


- dest-collection/
    - snes/
        - Name2 (USA).zip
        - gamelist.xml
    - megadrive/
        - Name7 (Japan).zip
        - Name8 (En).zip
        - Name9.zip
        - gamelist.xml

#### The script will perform the following work:

- In the **snes/** folder only **Name1** and **Name3** will be added. The rom **Name2** will not be added because the version **Name2 (USA)** already exists at the destination;
- In the **mastersystem** folder all three roms will be added;
- In the **megadrive** folder no rom will be added, because all of them already have a version at the destination;

#### The final result of your collection will be as shown below:

- dest-collection/
    - snes/
        - Name1 (USA,Japan).zip
        - Name2 (USA).zip
        - Name3 (USA,Europe,Japan).zip
        - gamelist.xml
    - mastersystem/
        - Name4 (USA,Japan).zip
        - Name5 (USA) (En,Fr,De).zip
        - Name6 (USA,Europe,Japan).zip
        - gamelist.xml
    - megadrive/
        - Name7 (Japan).zip
        - Name8 (En).zip
        - Name9.zip
        - gamelist.xml

The example above is the simplest thing that sbfrm can do. In fact, it is capable of more complex things, like managing sub-collections (snes/## HACKS ##/) for example. The complete list of parameters is shown below:

#### Mandatory Parameters:
- **op**: Operation to be performed.
    - **update_collections**: Updates, in **dest/**, all roms, images and videos files for each collection (game system) present in **src/**. Update the **gamelist.xml** of each collection, or create a new one if it doesn't exist;
    - **update_subcollection**: Update or Adds sub-collections to their respective collections. A subcollection is the another roms folder inside a collection folder (e.g. nes/## HACKS ##/). This operation works together with the optional parameter **-subcol_list**. If the optional parameter is not passed, no subcollection will be considered;
    - **raise_subcollection**: Elevates a sub-collection into the collection hierarchy. The newly created collection will have its own folders for organizing images and videos and its own **gamelist.xml**. This operation works in conjunction with the optional **-subcol_list** parameter. If it is not set, the new collection will not be created.
- **src/**: Path of the directory where the collection to be added is located.
    - Ex: /media/user/SHARE1/roms
- **dest/**: Path of the directory where the files should be added.
    - Ex: /media/user/SHARE/roms

#### Optional Parameters:
- **-box_src**: Name of the directory where the game box image files that are to be added to your collection are located (e.g. -box_src Named_Boxarts or box_src downloaded_images). If this parameter is not declared, these media files will not be updated in the target collection.
- **-img_src**: Name of the directory where the gameplay image files to be added to your collection are located (e.g. -img_src Named_Snaps or -img_src downloaded_images). If this parameter is not declared, these media files will not be updated in the target collection.
- **-marq_src**: Name of the directory where the game lettering image files to be added to your collection are located (e.g. -marq_src Named_Marks or -marq_src downloaded_wheels). If this parameter is not declared, these media files will not be updated in the target collection.
- **-thumb_src**: Name of the directory containing the small game title image files to be added to your collection (e.g. -thumb_src Named_Titles or -thumb_src downloaded_images). If this parameter is not declared, these media files will not be updated in the target collection.
- **-vid_src**: Name of the directory containing the games' video files to be added to your collection (e.g. -vid_src videos or -vid_src downloaded_videos). If this parameter is not declared, these media files will not be updated in the target collection.
- **-subcol_list**: List of sub-collections to be considered during script processing (ex: -subcol_list "## HACKS ##, # PT-BR #, # TECTOY #"). The list must be separated by commas, with no spaces between items, and enclosed in double quotes. For each collection present in **src**, the entire list will be evaluated, and, if any subdirectory exists with the same name as the item, the script will update or raise the subcollection.
- **-filemode**: Defines whether files will be copied or moved to the destination (e.g. -filemode cp or -filemode mv). This option is very useful if you have limited disk space or want the processing to be faster (files are moved almost instantly if they are within the same partition :p).

It is not my intention to think that this is a spectacular project and that there is no other equal or better one. There is a lot that can be improved, certainly there are bugs that I didn't notice, a lot of code refactoring to be done, lack of test implementation, etc, etc. But I hope it will be useful to you and help you save a lot of disk space and time organizing your roms. Time that should be used for playing and having fun. If you got this far, it is because you are really interested in my work and probably are, or will at some point, wonder what the hell sbfrm means, which is the acronym for Small Big Fucking Retro Gamelist Manager :)

Otherwise, here are my ideas for future work to be implemented (when I have some time to spare):
- Graphical Interface (to make it easier to use for those who are not used to using command line);
- Implement a new method to compare two directories and remove duplicate files from one of them (ex: remove the translated roms from the directory **nes/** and that are already present in the directory **nes/# PT-BR #/**);
- Improve the comparison of duplicate files. The current comparison has good results but it is quite simple. Using regex it may be possible to do more complex things like select files from a certain region, language, revision, etc.
- Write a document with examples and tricks of the cool things that I' ve been able to do with sbfrm
- Improve my english :p

Donation:

    "I have no special talent. I am only passionately curious."
    -Albert Einstein

Would you like to see this project continue to progress? Your help will be very welcome!

https://www.paypal.com/donate?hosted_button_id=G7KRYRNQ247AG

![Donation by PayPal](images/qrcode.png)
