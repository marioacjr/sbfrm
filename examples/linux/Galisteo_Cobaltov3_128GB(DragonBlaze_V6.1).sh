#######################  README  #######################
# Este exemplo faz uma busca em todas as roms da       #
# imagem Galisteo_Cobaltov3_128GB(DragonBlaze_V6 do    #
# Galisteo e atualiza a sua coleção com os jogos,      #
# imagens e videos que você ainda não possui.          #
# Todas as subcoleções serão transformadas em coleções #
# independentes com suas próprias gamelist.xml         #
# Ao final do processo, cada coleção possuirá um       #
# relatório com a totalização de arquivos e lista de   #
# imagens e vídeos ausentes.                           #
#                                                      #
# Todos os créditos ao trabalho do Galisteo, que       #
# realiza um trabalho incrível e disponibiliza essas   #
# imagens de forma gratuita.                           #
# Link para o Discord onde estão as imagens abaixo :   #
#                                                      #
#          https://discord.gg/38NaJVS                  #
#                                                      #
########################################################

Aqui voce deve alterar os caminhos para a pasta de
# roms da imagem do Galisteo e para a pasta onde
# está a sua coleção.
srcdir="/media/mario/SHARE1/roms"
destdir="/media/mario/SHARE/roms"

# Aqui não deve ser alterado, pois nesta imagem do
# Galisteo as pastas de imagens e vídeos tem
# essa padronização de nomes. Caso você use
# este exemplo em outra coleção, atualize esses
# nomes conforme necessário.
imgsrc="downloaded_images"
marqsrc="downloaded_wheels"
vidsrc="downloaded_videos"


# Este comando executa a varredura na coleção inteira
# e atualiza as roms. imagens e videos que não existem
# na sua coleção.
python3 sbfrm.py update_collections $srcdir/ $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc


# Os comandos daqui em diante transformam todas as
# subcoleções em coleções independentes com suas
# próprias gamelist.xml.
python3 sbfrm.py raise_subcollection $srcdir/fba_libretro $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subcol_list "## HACKS ##"

python3 sbfrm.py raise_subcollection $srcdir/gba $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subcol_list "# Japan #,# PT-BR #"

python3 sbfrm.py raise_subcollection $srcdir/gbc $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subcol_list "# PT-BR #"

python3 sbfrm.py raise_subcollection $srcdir/mame $destdir/ -img_src $imgsrc -marq_src $marqsrc -thumb_src thumbnails -vid_src $vidsrc -subcol_list "# ADK #,# ALPHA #,# ATARI #,# ATLUS #,# BANPRESTO #,# CAVE #,# CENTURY #,# CINEMATRONICS #,# COMAD #,# DATAEAST #,# DENIAM #,# EIGHTING #,# EOLITH #,# EXIDY #,# FACE #,# FUUKI #,# GAELCO #,# GOTTLIEB #,# GREMLIN #,## HACKS ##,# INCREDIBLE #,# IREM #,# JALECO #,# KANEKO #,# KONAMI #,# LELAND #,# MIDWAY #,# MITCHELL #,# MYLSTAR #,# NAMCO #,# NICHIBUTSU #,# NINTENDO #,# NMK #,# OMORI #,# ORCA #,# PGM #,# PHILKO #,# PLAYMARK #,# PSIKYO #,# SAMMY #,# SEGA #,# SEIBU #,# SEMICOM #,# SETA #,# SIGMA #,# SNK #,# SUN #,# SUNA #,# SUNSOFT #,# TAD #,# TAITO #,# TATSUMI #,# TECFRI #,# TECHMOS #,# TECMO #,# TEHKAN #,# TOAPLAN #,# UNICO #,# UNIVERSAL #,# UPL #,# VENTURE #,# VIDEOSYSTEM #,# VISCO #"

python3 sbfrm.py raise_subcollection $srcdir/mastersystem $destdir/ -img_src $imgsrc -marq_src $marqsrc -thumb_src thumbnails -vid_src $vidsrc -subcol_list "# MARK III (JP) #,# TECTOY #"

python3 sbfrm.py raise_subcollection $srcdir/megadrive $destdir/ -img_src $imgsrc -marq_src $marqsrc -thumb_src thumbnails -vid_src $vidsrc -subcol_list "# GENESIS (JP) #,## HACKS ##,# PT-BR #"

python3 sbfrm.py raise_subcollection $srcdir/n64 $destdir/ -img_src $imgsrc -marq_src $marqsrc -thumb_src thumbnails -vid_src $vidsrc -subcol_list "## HACKS ##"

python3 sbfrm.py raise_subcollection $srcdir/neogeo $destdir/ -img_src $imgsrc -marq_src $marqsrc -thumb_src thumbnails -vid_src $vidsrc -subcol_list "## HACKS ##"

python3 sbfrm.py raise_subcollection $srcdir/nes $destdir/ -img_src $imgsrc -marq_src $marqsrc -thumb_src thumbnails -vid_src $vidsrc -subcol_list "# DYNAVISION #,## HACKS ##,# PT-BR #"

python3 sbfrm.py raise_subcollection $srcdir/psp $destdir/ -img_src $imgsrc -marq_src $marqsrc -thumb_src thumbnails -vid_src $vidsrc -subcol_list "# PSP MINIS #"

python3 sbfrm.py raise_subcollection $srcdir/snes $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subcol_list "## HACKS ##,# PT-BR #,# SUPER FAMICOM (JP) #"
