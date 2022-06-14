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
srcdir="/media/mario/SHARE1/roms"
destdir="/media/mario/SHARE/roms"

# Aqui não deve ser alterado, pois nesta imagem do
# Batocera as pastas de imagens e vídeos tem
# essa padronização de nomes. Caso você use
# este exemplo em outra coleção, atualize esses
# nomes conforme necessário.
imgsrc="images"
marqsrc="marquee"
thumsrc="thumbs"
vidsrc="videos"

# Este comando executa a varredura na coleção inteira
# e atualiza as roms. imagens e videos que não existem
# na sua coleção.
python3 sbfrm.py update_collection $srcdir/ $destdir/ -img_src $imgsrc -marq_src $marqsrc -thumb_src $thumsrc -vid_src $vidsrc
