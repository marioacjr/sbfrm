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

# Aqui voce deve alterar os caminhos para a pasta de
# roms da imagem do Galisteo e para a pasta onde
# está a sua coleção.
srcdir="/media/mario/EEROMS"
destdir="/media/mario/SHARE/roms"

# Aqui não deve ser alterado, pois nesta imagem do
# Galisteo as pastas de imagens e vídeos tem
# essa padronização de nomes. Caso você use
# este exemplo em outra coleção, atualize esses
# nomes conforme necessário.
imgsrc="downloaded_images"
marqsrc="downloaded_wheels"
vidsrc="downloaded_videos"

subsystems="# Japan #,## HACKS ##,# MARK III (JP) #,# TECTOY #,# GENESIS (JP) #,# PT-BR #,# DYNAVISION #,# SATELLAVIEW #,# SUPER FAMICOM (JP) #"


# Este comando executa a varredura na coleção inteira
# e atualiza as roms, imagens e videos que não existem
# na sua coleção.
python3 sbfrm.py update_collection $srcdir/ $destdir/ -img_src $imgsrc -marq_src $marqsrc -vid_src $vidsrc -subsyslist "$subsystems" -verbose 1

# openbor ports scummvm
