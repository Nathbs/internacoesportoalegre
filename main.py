import pandas as pd  # importei a biblioteca pandas que fornece ferramente de análise dos dados
pd.options.mode.chained_assignment = None  # default='warn' acredito que estava dando um falso positivo

dfdadosinternacoes = pd.read_csv(r'./gerint_solicitacoes_mod.csv',  encoding='utf-8', delimiter= ';')  # funcao para
# leitura da tabela que foi fornecida pela PUCRS, declaro que o parametro para troca de coluna é ponto e virgula

print(dfdadosinternacoes.head())  # imprime cabeçalho das 5 primeiras linhas e da primeira e ultima coluna para verificar se está lendo corretamente
print(dfdadosinternacoes.isnull().any())  # imprime verificação se na tabela há dados não preenchidos na coluna
print(dfdadosinternacoes.info())  # imprime quantos dados estão preenchidos em cada linha
dfdadosinternacoes = dfdadosinternacoes.dropna(subset=['idade'])  # deleta as linhas que não contem dados na coluna idade
dfdadosinternacoes = dfdadosinternacoes.dropna(subset=['data_alta'])  # deleta as linhas que não contem dados na coluna data_alta
print(dfdadosinternacoes.isnull().any())  # imprime nova verificação da tabela se há dados não preenchidos nas colunas
print(dfdadosinternacoes.info())  # imprime quantos dados estão preenchidos em cada linha
print(dfdadosinternacoes.columns.values)  # imprime os nomes das minhas colunas para eu poder selecionar as que eu quero
colunaselecionadas = ['id_usuario', 'central_regulacao_origem', 'data_solicitacao', 'sexo', 'idade',
                      'municipio_residencia', 'solicitante', 'municipio_solicitante', 'data_autorizacao',
                      'data_internacao', 'data_alta', 'executante', 'horas_na_fila']# declaração da variável com a seleção de quais colunas irei utilizar

dadosinternacoesselecionados = dfdadosinternacoes.filter(items=colunaselecionadas)  # declaração de uma nova variável com novo dataframe somente com as columas selecionadas
dadosinternacoesselecionados.head()  # imprime a minha nova dataframe para verificar se está realizou minha seleção


def bemvindo():
    print("Olá, seja Bem-Vinde ao Programa de Análises das Internações do Estado do Rio Grande dos Sul entre os anos de"
          " 2018-2021.\n Há algumas opções sobre dados das informações veja qual a que você está buscando! \n")
    print("Opção 1- Consultar média de idade dos pacientes por municipio de moradia. \n Tal opção irá filtrar o "
          "município de origem e informar o número total de pacientes do município, a média de idade dos pacientes "
          "separados por gênero, \n e a média de idade de todos os pacientes.")
    print("\n Opção 2- Consultar internações por ano por município de moradia. \n Tal opção irá filtrar através do municpio "
          " e de origem e informar uma listagem com os anos de 2018 a 2021 a quantidade de pacientes internados naquele ano.")
    print("\n Opção 3- Consultar hospitais. \n Tal opção irá filtrar a partir do Nome do Estabelecimento de saúde que realizou internação"
          " e irá informar todos os pacientes que foram internados, \n sua idade, o município residencial e solicitante "
          "de cada um deles, as datas de autorização, de internação e alta e o executante")
    print("\n Opção 4- Calcular tempo de internação \n Tal opção irá digitar o Nome do Estabelecimento de Saúde referente ao local de trabalho"
          " do profissional solicitante. E irá informar uma lista com todos os pacientes, \n o nome dos hospitais que realizaram a internação"
          " e também número de dias que os pacientes permaneceram internados desde a data solicitação até a alta deste paciente.")
    print("\n Opção 5- O programa irá mostrar os cinco casos com maior tempo de espera na fila no Rio Grande do Sul.")
    print("\n Opção 6 - Deseja encerrar o programa")


def opcaomenu():
    escolhaopcao = int(input("Escolha sua opção: "))  #transformei a string em número inteiro para poder fazer a verificação
    escolhavalida = False
    while escolhavalida==False:
        if (escolhaopcao==1 or escolhaopcao==2 or escolhaopcao==3 or escolhaopcao==4 or escolhaopcao==5 or escolhaopcao==6):
            escolhavalida = True
        else:
           escolhaopcao = int(input("Opção Inválida, por favor digite uma opção válida: ")) # TODO receber string também sem quebrar
    return escolhaopcao  # guardando o número que o usuário digitou para executar a tarefa


def escolha1():
    escolhacidade1 = str.upper(input("Por favor, digite o município residencial de interesse: "))  # colocando em caixa
    # alta para que consiga fazer a verificação
    dfescolha1 = dadosinternacoesselecionados.loc[dadosinternacoesselecionados['municipio_residencia']==escolhacidade1]
    # puxa todas as linhas com os parametros que foram definidos
    numerointernados = len(dfescolha1)  # contagem das linhas/dados com base no municipio de residencia escolhido
    if numerointernados > 0:
        print("A) O número total de internados do municipio residencial escolhido é: " + str(numerointernados))
    else:  # caso não tenha número de pessoas acima de zero ele irá informar que não
        print("A) Não há internados do municipio residencial escolhido")
    colunaselecionadas = ['sexo', 'idade']  # estou selecionando as colunas que vou querer utilizar para as demais funções
    dfescolha1sexoidade = dfescolha1.filter(items=colunaselecionadas)  # dataframe com as colunas selecionadas para poder
    # utilizar nas minhas funções
    mediasexoidade = dfescolha1sexoidade.groupby('sexo').mean()  # variável para que faça a media de cada gênero, agrupando pelo sexo
    print("B) A media de idade dos pacientes separados por gênero é: \n" + str(mediasexoidade))  #converto em string
    # para que possa imprimir a coluna
    mediatotalidade = dfescolha1sexoidade['idade'].mean()  #função do pandas que calcula a media da coluna determinada
    print("C) A media de idade do total de pacientes é: " + str(mediatotalidade) + " anos.")


def escolha2():
    escolhacidade2 = str.upper(input("Por favor, digite o município residencial de interesse: "))
    dfescolha2 = dadosinternacoesselecionados.loc[dadosinternacoesselecionados['municipio_residencia']==escolhacidade2]
    #puxa todas as linhas com os parametros que foram definidos
    colunaselecionadas = ['data_internacao']  # estou selecionando as colunas que vou querer utilizar para as demais funções
    dfescolha2data = dfescolha2.filter(items=colunaselecionadas)
    dfescolha2data['data_internacao'] = pd.to_datetime(dfescolha2data['data_internacao'])
    dfescolha2data = dfescolha2data[dfescolha2data.data_internacao.dt.year > 2017]  # estou filtrando por ano e também
    # colocando criterio pois há dados de 2017
    dfescolha2data = dfescolha2data['data_internacao'].groupby([dfescolha2data.data_internacao.dt.year]).agg('count')
    #metodo de agregaçao por soma
    print("O número de pessoas internadas por ano dessa cidade é:" + str(dfescolha2data))


def escolha3():
    escolhaexecutante = str.upper(input("Por favor, digite o Nome do Estabelecimento de saúde que realizou internação "
                                        "(executante) de interesse: "))
    dfescolha3 = dadosinternacoesselecionados.loc[dadosinternacoesselecionados['executante']==escolhaexecutante]
    colunaselecionadas3 = ['id_usuario', 'data_solicitacao', 'idade','municipio_residencia', 'municipio_solicitante',
                           'data_autorizacao', 'data_internacao', 'data_alta', 'executante']  # estou selecionando as
    # colunas que vou querer utilizar para as demais funções
    dffinal3 = dfescolha3.filter(items=colunaselecionadas3)  # dataframe com as colunas selecionadas para poder imprimir
    # somente o que foi solicitado
    print(dffinal3) # TODO imprimir todas as colunas solicitadas


def escolha4():
    escolhasolicitante = str.upper(input("Por favor, digite o Nome do Estabelecimento de Saúde referente ao local de "
                                         "trabalho do profissional solicitante (solicitante) de interesse: "))
    dfescolha4 = dadosinternacoesselecionados.loc[dadosinternacoesselecionados['solicitante'] == escolhasolicitante]
    dfescolha4['data_alta'] = pd.to_datetime(dfescolha4.data_alta)
    dfescolha4['data_solicitacao'] = pd.to_datetime(dfescolha4.data_solicitacao)
    dfescolha4['dias_internado'] = dfescolha4['data_alta'] - dfescolha4['data_solicitacao']
    print("A, B e C) A lista com todos os pacientes, o hospital executante e o número de dias é internados:\n")
    print(dfescolha4[['id_usuario', 'executante', 'dias_internado']])


def escolha5():  # irá imprimir os 5 casos de todos os casos que ficaram mais tempo na fila
    print(" Os cinco casos com maior tempo de espera na fila são:")
    print(dadosinternacoesselecionados.nlargest(5, 'horas_na_fila'))  # funçao para localizar os 5 maiores numeros na coluna horas na fila
    # TODO imprimir todas as colunas para mostrar o resultado


def funcaomain():
    bemvindo()
    escolhaopcao = opcaomenu()
    if escolhaopcao == 1:
        escolha1()
    if escolhaopcao == 2:
        escolha2()
    if escolhaopcao == 3:
        escolha3()
    if escolhaopcao == 4:
        escolha4()
    if escolhaopcao == 5:
        escolha5()
    if escolhaopcao ==6:
        print("Obrigada, até a próxima!")
    menuprincipal = str.upper(input("Você deseja buscar mais alguma informação? Digite S para voltar ao menu principal,"
                                    " ou qualquer outro botão para sair: "))
    if menuprincipal == 'S':
        funcaomain()
    else:
        print("Obrigada, até a próxima!")


# MAIN NOVO
funcaomain()