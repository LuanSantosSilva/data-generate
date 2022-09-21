import random
import string
from faker import Faker
import re
from random import randint

class Generator(object):
    def __init__(self, quantity):
        self.quantity = quantity
        self.cpfs = {}
        self.cnpjs = {}
        self.names = {}
        self.contatos = {}
        self.emails = {}
        self.rgs = []
        self.inscricoes = []
        self.telefones = []
        self.datas = []
        self.numeros = []
        self.ids = []

    def cpfs_generate(self):
        cpfs = {}
        for keyNum in range(self.quantity):
            #  Gera os primeiros nove dígitos (e certifica-se de que não são todos iguais)
            while True:
                cpf = [randint(0, 9) for i in range(9)]
                if cpf != cpf[::-1]:
                    break

            #  Gera os dois dígitos verificadores
            for i in range(9, 11):
                value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
                digit = ((value * 10) % 11) % 10
                cpf.append(digit)

            #  Retorna o CPF como string
            cpf = ''.join(map(str, cpf))
            cpfs[keyNum] = '| '+f'{cpf[:3]}{cpf[3:6]}{cpf[6:9]}{cpf[9:]}'+' '
        self.cpfs = cpfs
        return self.cpfs


    def cnpjs_generate(self):
        cnpjs = {}
        for key in range(self.quantity):
            n = [random.randrange(10) for i in range(8)] + [0, 0, 0, 1]
            v = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5, 6]
            # calcula dígito 1 e acrescenta ao total
            s = sum(x * y for x, y in zip(reversed(n), v))
            d1 = 11 - s % 11
            if d1 >= 10:
                d1 = 0
            n.append(d1)
            # idem para o dígito 2
            s = sum(x * y for x, y in zip(reversed(n), v))
            d2 = 11 - s % 11
            if d2 >= 10:
                d2 = 0
            n.append(d2)
            
            cnpjs[key] = '| '+str("%d%d%d%d%d%d%d%d%d%d%d%d%d%d" % tuple(n))+' '
        self.cnpjs = cnpjs
        return self.cnpjs


    def names_generate(self):
        names = {}
        caracterNames = {}
        fake = Faker(['pt_BR', 'en_US'])

        for keyNum in range(self.quantity):
            names[keyNum] = fake.name()
            caracterNames[keyNum] = len(names[keyNum])

        maiorNome = caracterNames[max(caracterNames, key = caracterNames.get)]

        for keyTxt in range (self.quantity): 
            spaceNome = len(names[keyTxt])
            spaceDiferencaNome = maiorNome - spaceNome

            for inicio in range(spaceDiferencaNome):
                names[keyTxt] = str(names[keyTxt] + " ")
            names[keyTxt] = "| " + names[keyTxt] + " "
        self.names = names
        return self.names


    def contatos_generate(self):
        if(len(self.names) == 0):
            self.names_generate()

        contatos = {}
        contato = {}
        caracterContatos = {}

        for keyNum in range(len(self.names)):
            contatos[keyNum] = self.names[keyNum].split(" ", 2)
            if(len(contatos[keyNum][0]) <= 4):
                contato[keyNum] = f'{contatos[keyNum][0]} {contatos[keyNum][1]}'
            else:
                contato[keyNum] = contatos[keyNum][0]

            caracterContatos[keyNum] = len(contato[keyNum])

        maiorContato = caracterContatos[max(caracterContatos, key = caracterContatos.get)]

        for chave in range(len(self.names)):
            spaceContato = len(contato[chave])
            spaceDiferencaContato = maiorContato - spaceContato
            for inicio2 in range(spaceDiferencaContato):
                contato[chave] = str(contato[chave]) + " "
            if(len(self.names) == 1 and spaceContato < 7):
                spaceDiferencaContato = 7 - spaceContato
                for inicioif in range(spaceDiferencaContato):
                    contato[chave] = str(contato[chave]) + " "
        self.contatos = contato
        return self.contatos


    def emails_generate(self):
        if(len(self.names) == 0):
            self.names_generate()
        
        contatos = {}
        contato = {}
        emails = {}
        caracterContatos = {}
        caracterEmails = {}
        letras = {0 : 'ã', 1 : 'ç', 2 : 'á', 3 : 'õ', 4 : 'ô', 5 : 'â', 6 : 'í', 7 : 'ê', 8 : 'ú', 9 : 'é', 10 : 'ó'}
        letrasC = {0 : 'a', 1 : 'c', 2 : 'a', 3 : 'o', 4 : 'o', 5 : 'a', 6 : 'i', 7 : 'e', 8 : 'u', 9 : 'e', 10 : 'o'}

        for keyNum in range(len(self.names)):
            name = self.names[keyNum].replace('| ','')
            contatos[keyNum] = name.replace(".","").lower()
            contatos[keyNum] = contatos[keyNum].split(" ")
            
            if(len(contatos[keyNum][0]) <= 4):
                contato[keyNum] = f'{contatos[keyNum][0]} {contatos[keyNum][1]}'
            else:
                contato[keyNum] = contatos[keyNum][0]

            caracterContatos[keyNum] = len(contato[keyNum])

            emails[keyNum] = contato[keyNum]
            emails[keyNum] = re.sub(r"\s+", "", emails[keyNum])
            
            for letra in letras:
                emails[keyNum] = emails[keyNum].replace(str(letras[letra]), str(letrasC[letra]))
            emails[keyNum] = emails[keyNum] + "@gmail.com"
            caracterEmails[keyNum] = len(emails[keyNum])

        maiorEmail = caracterEmails[max(caracterEmails, key = caracterEmails.get)]

        for chave in range(len(self.names)):
            spaceEmail = len(emails[chave])
            spaceDiferencaEmail = maiorEmail - spaceEmail
            emails[chave] = ' '+str(emails[chave])

            for inicio3 in range(spaceDiferencaEmail):
                emails[chave] = str(emails[chave]) + " "

            emails[chave] = '| '+ emails[chave] + ' '
        self.emails = emails
        return self.emails
        

    def rgs_generate(self):
        rgs = []
        num_soma = [2, 3, 4, 5, 6, 7, 8, 9]
        for keyNum in range(self.quantity):
            resto = 1
            while (resto == 1):
                soma = 0
                string = ''
                rgs_teste = [randint(0, 9) for i in range(8)]
                rg = [rgs_teste[num]*num_soma[num] for num in range(len(rgs_teste))]
                for num_rg in rg:
                    soma = soma + num_rg
                resto = soma%11

            if(resto != 1 and resto != 0):
                verificador = 11 - resto
            elif(resto == 0):
                verificador = 0

            for num_rg in rgs_teste:
                string = string + str(num_rg)
            rg = string + str(verificador)
            rgs.append(rg)
        self.rgs = rgs
        return self.rgs


    # UM GERADOR DE NÚMERO DE INSCRIÇÕES, NO MOMENTO APENAS PARA O ESTADO DO CEARÁ
    def ninscricoes_generate(self):
        inscricoes = []
        pesos = {0 : 9, 1 : 8, 2 : 7, 3 : 6, 4 : 5, 5 : 4 , 6 : 3, 7 : 2}
    
        
        for chave in range(self.quantity):
            inscricao = ""
            numbers = {}
            mult = {}
            soma = 0
            for r in range(8):
                numbers[r] = randint(0,9)
                mult[r] = pesos[r] * numbers[r]
                soma = soma + mult[r]
            
            for i in range(9):
                if(i < 8):
                    inscricao = inscricao + str(numbers[i])
                else:
                    digito = 11 - soma%11
                    if(digito == 10 or digito == 11):
                        digito = 0
                        inscricao = inscricao + str(digito)
                    else:
                        inscricao = inscricao + str(digito)
            inscricoes.append('| '+inscricao+' ')
        self.inscricoes = inscricoes
        return self.inscricoes


    def telefones_generate(self):
        telefones = []
        for key in range(self.quantity): 
            phone = str(randint(1111, 9999))
            number = str(randint(1111, 9999))
            telefone = '9' + phone + number
            telefones.append("| "+str(telefone)+ " ")
        self.telefones = telefones
        return self.telefones


    def datas_generate(self, ano1=2019, ano2=2021):
        data = []
        for key in range(self.quantity):
            dia = randint(1,28)
            dia = "0"+str(dia) if len(str(dia)) == 1 else dia
            mes = randint(1,12)
            mes = "0"+str(mes) if len(str(mes)) == 1 else mes
            ano = randint(ano1, ano2)
            data.append(f'{"| "+str(dia) + "/" + str(mes) + "/" + str(ano)+" "}')
        self.datas = data
        return self.datas


    # UM GERADOR DE NÚMERO ALEATÓRIO, CASO SEJA PRECISO
    def random_generate(self, number1=10, number2=100):
        spaceN = len(str(number2))
        numeros = []
        for key in range(self.quantity):
            numeros.append(str(randint(number1, number2)))
            spaceDiferencaNUM = spaceN - len(str(numeros[key]))
            numeros[key] = '| '+numeros[key]+' '
            if(spaceN == 1):
                numeros[key] = str(numeros[key])+' '
            for inicio in range(spaceDiferencaNUM):
                numeros[key] = str(numeros[key]) + ' '
        self.numeros = numeros
        return self.numeros


    def ids_generate(self):
        spaceID = len(str(self.quantity))
        id = []
        for keyNum in range(self.quantity):
            id.append(keyNum + 1)
            spaceDiferencaID = spaceID - len(str(id[keyNum]))
            id[keyNum] = '| '+str(id[keyNum])+' '
            if(spaceID == 1):
                id[keyNum] = str(id[keyNum]) + " "
            for inicio in range(spaceDiferencaID):
                id[keyNum] = str(id[keyNum]) + " "
        self.ids = id
        return self.ids


    def arquivo_generate(self, name_file='generated', *array):
        array = array
        arrays = {}
        linha = {}
        file = open(name_file+'.txt', 'a')
        file.close()
        arquivo = open(name_file+'.txt', 'r')
        line = arquivo.readlines()
        arquivo.close()

        cont = len(array)
        for ind in range(cont):
            arrays[ind] = array[ind]

        quantidade = len(arrays[0])
        for x in range(quantidade):
            linha[x] = ''

        for x in range(len(arrays)):
            for l in range(quantidade):
                linha[l] = str(linha[l]) + ' ' +str(arrays[x][l])

        for num_line in linha:
            info = linha[num_line] + ' |\n'
            line.insert(num_line, info)
            arquivo = open(name_file+'.txt', 'w')
            arquivo.writelines(line)
            arquivo.close()
