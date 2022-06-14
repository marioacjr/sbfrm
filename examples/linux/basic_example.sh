#######################  README  #######################
# Este exemplo faz uma busca em todas as roms do       #
# diretório fonte e atualiza a coleção destino com os  #
# jogos, imagens e videos. Ao final do processo, cada  #
# coleção possuirá um relatório com a totalização de   #
# arquivos e lista de imagens e vídeos ausentes.       #
########################################################

# Aqui voce deve alterar os caminhos para a pasta de
# roms fonte e para a pasta onde está a coleção destino.
srcdir="test/roms_src/system_one"
destdir="test/roms_dest/system_one"

# Nomes dos diretórios onde estão as imagens e videos da coleção
boxsrc="downloaded_boxarts"
imgsrc="downloaded_images"
thumbsrc="downloaded_thumbnails"
vidsrc="downloaded_videos"
marqsrc="downloaded_wheels"

subsystems="## HACKS ##,# PT-BR #"

# Este comando executa uma atualização em apenas um sistema e seus subsistemas
python3 sbfrm.py update_system $srcdir $destdir -box_src $boxsrc -img_src $imgsrc -thumb_src $thumbsrc -vid_src $vidsrc -marq_src $marqsrc -subsyslist "$subsystems"

# Este comando executa a varredura na coleção inteira
# e atualiza as roms, imagens e videos que não existem
# na sua coleção.
srcdir="test/roms_src/"
destdir="test/roms_dest/"
python3 sbfrm.py update_collection $srcdir $destdir -img_src $imgsrc -vid_src $vidsrc -marq_src $marqsrc -subsys_list "$subsystems"
