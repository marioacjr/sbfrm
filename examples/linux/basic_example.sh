#######################  README  #######################
# Este exemplo faz uma busca em todas as roms do       #
# diretório fonte e atualiza a coleção destino com os  #
# jogos, imagens e videos. Ao final do processo, cada  #
# coleção possuirá um relatório com a totalização de   #
# arquivos e lista de imagens e vídeos ausentes.       #
########################################################

# Aqui voce deve alterar os caminhos para a pasta de
# roms fonte e para a pasta onde está a coleção destino.
srcdir="test/roms_src/"
destdir="test/roms_dest/"

# Nomes dos diretórios onde estão as imagens e videos da coleção
boxsrc="boxart,boxarts,downloaded_boxart,downloaded_boxarts"
imgsrc="image,images,downloaded_image,downloaded_images"
thumbsrc="thumbnail,thumbnails,downloaded_thumbnail,downloaded_thumbnails"
marqsrc="marquee,marquees,wheel,wheels,downloaded_wheel,downloaded_wheels"
vidsrc="video,videos,downloaded_video,downloaded_videos"

subsystems="# Japan #,## HACKS ##,# MARK III (JP) #,# TECTOY #,# GENESIS (JP) #,# PT-BR #,# DYNAVISION #,# SATELLAVIEW #,# SUPER FAMICOM (JP) #"

rm -rf $destdir/*

# Este comando executa a varredura na coleção inteira e atualiza as roms,
# imagens e videos da sua coleção.
python3 sbfrm.py update_collection $srcdir $destdir -box_src "$boxsrc" -img_src "$imgsrc" -thumb_src "$thumbsrc" -marq_src "$marqsrc" -vid_src "$vidsrc" -subsyslist "$subsystems" -verbose 0 -overwritefile 0

srcdir="test/roms_src/system_one"
destdir="test/roms_dest/system_one"
rm -rf $destdir/*
# # Este comando executa uma atualização em apenas um sistema e seus subsistemas
python3 sbfrm.py update_system $srcdir $destdir -box_src "$boxsrc" -img_src "$imgsrc" -thumb_src "$thumbsrc" -marq_src "$marqsrc" -vid_src "$vidsrc" -subsyslist "$subsystems" -verbose 0 -overwritefile 0
