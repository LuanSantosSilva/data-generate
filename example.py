from classes.generator import Generator

teste = Generator(15)

teste.ids_generate()
teste.names_generate()
teste.cpfs_generate()
teste.datas_generate(2001, 2002)
teste.random_generate(85,85)
teste.telefones_generate()
teste.emails_generate()

teste.arquivo_generate('teste',teste.ids, teste.names, teste.cpfs, teste.datas, teste.numeros, teste.telefones, teste.emails)
