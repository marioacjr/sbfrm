#######################  README  #######################
# Este exemplo faz uma busca em todas as roms da       #
# imagem CobaltoV4_PI4_128GB_7.1.1.IMG do Galisteo e   #
# atualiza a sua coleção com os jogos, imagens e       #
# videos que você ainda não possui.                    #
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

# Aqui voce deve alterar os caminhos para a pasta de
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

python3 sbfrm.py update_subcollection $srcdir/atari2600 $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subcol_list "## HACKS ##"
python3 sbfrm.py update_subcollection $srcdir/fbneo $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subcol_list "## HACKS ##"
python3 sbfrm.py update_subcollection $srcdir/gba $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subcol_list "# Japan #,# PT-BR #"
python3 sbfrm.py update_subcollection $srcdir/mastersystem $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subcol_list "# MARK III (JP) #,# TECTOY #"
python3 sbfrm.py update_subcollection $srcdir/megadrive $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subcol_list "# GENESIS (JP) #,## HACKS ##,# PT-BR #"
python3 sbfrm.py update_subcollection $srcdir/n64 $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subcol_list "## HACKS ##"
python3 sbfrm.py update_subcollection $srcdir/nes $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subcol_list "# DYNAVISION #,## HACKS ##,# PT-BR #"
python3 sbfrm.py update_subcollection $srcdir/psp $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subcol_list "# PSP MINIS #"
python3 sbfrm.py update_subcollection $srcdir/snes $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subcol_list "## HACKS ##,# PT-BR #,# SATELLAVIEW #,# SUPER FAMICOM (JP) #"
