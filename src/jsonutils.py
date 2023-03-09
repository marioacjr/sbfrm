import json
from os.path import isfile

def check_is_configs_exists():
    """Make Description."""
    config_dict = {
        "src_media_dirs_list": {
            "boxart": [
                "boxart",
                "images",
                "downloaded_boxarts"
            ],
            "image": [
                "image",
                "images",
                "downloaded_images"
            ],
            "marquee": [
                "marquee",
                "images",
                "downloaded_wheels"
            ],
            "thumbnail": [
                "thumbnail",
                "images",
                "downloaded_thumbnails"
            ],
            "video": [
                "video",
                "videos",
                "downloaded_videos"
            ]
        },
        "dest_media_dirs_names": {
            "boxart": "boxart",
            "image": "image",
            "marquee": "marquee",
            "thumbnail": "thumbnail",
            "video": "video"
        },
        "filemode": {
            "options": [
                "cp",
                "mv"
            ],
            "mode": "cp"
        },
        "overwrite_file": 1,
        "overwrite_gamelist_info": 0,
        "verbose": 1,
        "gamelist_provider": {
            "system": "system_one",
            "software": "SBFRM",
            "web": "https://github.com/marioacjr/sbfrm"
        },
        "region_order": [
            "USA",
            "World",
            "Canada",
            "UK",
            "Australia",
            "New Zealand",
            "Singapore",
            "Ireland",
            "Europe",
            "Hong Kong",
            "Japan",
            "Asia",
            "Thailand",
            "Spain",
            "Mexico",
            "Argentina",
            "Latin America",
            "Brazil",
            "Portugal",
            "France",
            "Belgium",
            "Netherlands",
            "Germany",
            "Austria",
            "Italy",
            "Switzerland",
            "China",
            "Taiwan",
            "Korea",
            "Russia",
            "Ukraine",
            "Estonia",
            "Poland",
            "Latvia",
            "Lithuania",
            "Denmark",
            "Norway",
            "Sweden",
            "Scandinavia",
            "Finland",
            "Hungary",
            "Czech",
            "Greece",
            "Macedonia",
            "India",
            "South Africa",
            "Israel",
            "Slovakia",
            "Turkey",
            "Croatia",
            "Slovenia",
            "United Arab Emirates",
            "Bulgaria",
            "Romania",
            "Albania",
            "Serbia",
            "Indonesia",
            "Unknown"
        ],
        "removed_devcomm_status": [
            "Beta",
            "Demo",
            "Enhancement Chip",
            "Sample",
            "Preview",
            "Program",
            "Rental",
            "Trainer",
            "Taikenban Sample ROM",
            "Test Drive"
        ],
        "gui_last_src": "test/roms_src",
        "gui_last_dest": "test/roms_dest"
    }
    
    if not isfile("config.json"):
        jsonString = json.dumps(config_dict, indent=4)
        jsonFile = open("config.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()