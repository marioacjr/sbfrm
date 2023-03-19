# ChangeLog

---

## 0.5.12
- Bug Fix: Fixed crash error when removing clone games

---

## 0.5.11
- Bug Fix: Fixed bug of not processing a system folder without the gamelist.xml file

---

## 0.5.10
- Added Checkboxs to Overwrite Files, Overwrite Metadata and Copy or Move Files options.
- Bug Fix: Fixed GUI misalignment in Windows.

---

## 0.5.9
- Bux Fix: Games with multiple disc roms are no longer removed
- Readmes Update

---

## 0.5.8
- User Interface Improvements

---

## 0.5.7
- Bux Fix: Remove clones removes highest priority rom

---

## 0.5.6
- Bux Fix: Corrected GUI stop proccess

---

## 0.5.5
- Bux Fix: Corrected GUI terminal prints

---

## 0.5.4
- Bux Fix: Not saving the metadata of games removed from the collection fixed.
- Bug Fix: Configuration file (config.json) always overwritten.

---

## 0.5.3
- Bux Fix: Creation of the configs.json file when it doesn't exist.

---

## 0.5.2
- Bux Fix: progress screen prints of user interface fixed.

---

## 0.5.1
- Removed Game Clones are backed up to a System Backup folder (systemname_removed).

---

## 0.5.0
- Feature Added: Remove Game Clones.
                    For this system, clones are considered any game with same <name> tag in gamelist.xml and diferent file name in system folder.
- Removed Feature: SubSystem Files Load.
                   These files are read from the paths indicated by gamelist.xml. All files in subfolders of a source system will be merged with the files in the root of the target system.
- Bug Fix: Wrong entries in report files corrected
- Performance improvements in loading systems, especially on very large systems.

---

## 0.4.5
- Bug Fix: system_update does not add metadata for media paths when the target system does not contain any files.

---

## 0.4.4
- Avoids copying files with the same name and different extension.
- Add or Overwrite metadata in gamelist.xml for files with same name and
different extensions.
- Bug Fix: not updating subsystems in the update_system operation.

---

## 0.4.3
- Cancel Process option Optmized.
- GUI Text Correction (Linux Version).
- Change Source Media Dir Name to List Dir Names.
- Changed SubSystems Names to accept Comma Separated and Multilines format.

---

## 0.4.2
- Add Progress window.
- Add Cancel Process option.
- Code refatoring.

---

## 0.4.1
- Added Reports Generation.
- Code refatoring.

---

## 0.4.0
- Added GUI.
- Code refatoring.
- Removed report features (will be added soon).

---

## 0.3.5
- Bugfix on gamelist.xml generation.
- Added new linux example.
- Code refatoring.

---

## 0.3.4
- Updated baseclasses Game, System
- The Game class is now generating its xml element.
- The System class is now generating and saving to disk the gamelist.xml
- Started implementing unit tests
- Code refatoring.

---

## 0.3.3
- Created baseclasses Game, System, Collection
- Created utils FileHandler, GameListHandler, StringHandler.
- Code refatoring.

---

## 0.3.2
- Created baseclasses Game, System, GameListHandler, Utils().
- Code refatoring.

---

## 0.3.1
- Bugfix on update_subcollection method.
- Code refatoring.

---

## 0.3.0
- Code organized in Classes and Methods (object-oriented).
- Code refatoring.

---

## 0.2.1
- Bugfix on Raise Collection Operation.
- Code refatoring.

---

## 0.2.0
- Added support to run on Windows.
- Added examples for Windows (**.bat**) and Linux (**.sh**).
- Changed base path of main python file for project root.
- Changed name of main python file for **sbfrm.py**.
- Added the README.
- Added the README in Pt-Br.

---

## 0.1.0
- First Alpha Version.
