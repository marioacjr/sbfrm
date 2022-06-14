#######################  README  #######################
# Este exemplo faz uma busca em todas as roms da       #
# imagem Cobalto_GA_Batocera5.25_16GB.img do Galisteo e          #
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
# roms da imagem do Batocera e para a pasta onde
# está a sua coleção.
srcdir="/media/mario/SHARE/roms"
destdir="/media/mario/SHARE1/roms"

# Aqui não deve ser alterado, pois nesta imagem do
# Batocera as pastas de imagens e vídeos tem
# essa padronização de nomes. Caso você use
# este exemplo em outra coleção, atualize esses
# nomes conforme necessário.
imgsrc="images"
vidsrc="videos"

# Este comando executa a varredura na coleção inteira
# e atualiza as roms, imagens e videos que não existem
# na sua coleção.
python3 sbfrm.py update_collection $srcdir/ $destdir/ -img_src $imgsrc -vid_src $vidsrc

srcdir="/media/mario/SHARE/roms/gx4000"
destdir="roms_dest/gx4000"
vidsrc="media/videos"
python3 sbfrm.py update_system $srcdir/ $destdir/ -vid_src $vidsrc

srcdir="/media/mario/SHARE/roms/n64"
destdir="roms_dest/n64"
vidsrc="downloaded_images"
python3 sbfrm.py update_system $srcdir/ $destdir/ -vid_src $vidsrc

srcdir="/media/mario/SHARE/roms/naomi"
destdir="roms_dest/naomi"
vidsrc="media/videos"
python3 sbfrm.py update_system $srcdir/ $destdir/ -vid_src $vidsrc

srcdir="/media/mario/SHARE/roms/pcengine"
destdir="roms_dest/pcengine"
vidsrc="media/videos"
python3 sbfrm.py update_system $srcdir/ $destdir/ -vid_src $vidsrc

srcdir="/media/mario/SHARE/roms/pcenginecd"
destdir="roms_dest/pcenginecd"
vidsrc="media/videos"
python3 sbfrm.py update_system $srcdir/ $destdir/ -vid_src $vidsrc

srcdir="/media/mario/SHARE/roms/pokemini"
destdir="roms_dest/pokemini"
imgsrc="downloaded_images"
python3 sbfrm.py update_system $srcdir/ $destdir/ -img_src $imgsrc

srcdir="/media/mario/SHARE/roms/saturn"
destdir="roms_dest/saturn"
vidsrc="media/videos"
python3 sbfrm.py update_system $srcdir/ $destdir/ -vid_src $vidsrc

srcdir="/media/mario/SHARE/roms/sega32x"
destdir="roms_dest/sega32x"
vidsrc="downloaded_images"
python3 sbfrm.py update_system $srcdir/ $destdir/ -vid_src $vidsrc

srcdir="/media/mario/SHARE/roms/wswan"
destdir="roms_dest/wswan"
vidsrc="downloaded_images"
python3 sbfrm.py update_system $srcdir/ $destdir/ -vid_src $vidsrc

srcdir="/media/mario/SHARE/roms/wswanc"
destdir="roms_dest/wswanc"
vidsrc="downloaded_images"
python3 sbfrm.py update_system $srcdir/ $destdir/ -vid_src $vidsrc
