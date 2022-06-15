srcdir="/media/mario/EEROMS"
destdir="test/roms_dest"

boxsrc="downloaded_boxarts"
imgsrc="downloaded_images"
thumbsrc="downloaded_thumbnails"
vidsrc="downloaded_videos"
marqsrc="downloaded_wheels"

subsystems="## HACKS ##,# PT-BR #"

rm -rf $destdir/*

python3 sbfrm.py update_collection $srcdir $destdir -box_src $boxsrc -img_src $imgsrc -thumb_src $thumbsrc -marq_src $marqsrc -vid_src $vidsrc -subsyslist "$subsystems" -verbose 1 -overwritefile 0

# python3 sbfrm.py update_system $srcdir $destdir -box_src $boxsrc -img_src $imgsrc -thumb_src $thumbsrc -vid_src $vidsrc -marq_src $marqsrc -subsyslist "$subsystems" -verbose 1 -overwritefile 1
