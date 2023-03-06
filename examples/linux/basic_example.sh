#######################  README  #######################
# Este exemplo faz uma busca em todas as roms do       #
# diretório fonte e atualiza a coleção destino com os  #
# jogos, imagens e videos. Ao final do processo, cada  #
# coleção possuirá um relatório com a totalização de   #
# arquivos e lista de imagens e vídeos ausentes.       #
########################################################


# Este comando executa a varredura na coleção inteira e atualiza as roms,
# imagens e videos da sua coleção.
python3 sbfrm.py update_collection "test/roms_src/" "test/roms_dest/"


# # Este comando executa uma atualização em apenas um sistema.
python3 sbfrm.py update_system "test/roms_src/system_one" "test/roms_dest/system_one"
