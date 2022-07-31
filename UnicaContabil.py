import pandas as pd
import smtplib
from pathlib import Path
import os
from email.message import EmailMessage

print('Iniciando...\n')

# deseja iniciar a versao de teste ou a de producao

def EnviarEmail(destino, assunto, mensagem):
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login('NotaFiscal@unicacontabil.com', 'nfunica123')

    email= EmailMessage()
    email['From'] = 'NotaFiscal@unicacontabil.com'
    email['To'] = destino
    # email['To'] = 'evelyn@unicacontabil.com'
    email['Cc'] = 'fiscal@unicacontabil.com; evelyn@unicacontabil.com'
    email['Subject'] = assunto

    email.set_content(mensagem)

    server.send_message(email)
    print('E-mail para {} enviado com sucesso!' .format(destino))

print('Carregando variaveis de sistema...\n')

#Dicionarios Auxiliares
dMeses = {
    1:  ['Janeiro',     [1,3,4]],
    2:  ['Fevereiro',   [1,5,6]],
    3:  ['Março',       [1,7,8]],
    4:  ['Abril',       [1,9,10]],
    5:  ['Maio',        [1,11,12]],
    6:  ['Junho',       [1,13,14]],
    7:  ['Julho',       [1,15,16]],
    8:  ['Agosto',      [1,17,18]],
    9:  ['Setembro',    [1,19,20]],
    10: ['Outubro',     [1,21,22]],
    11: ['Novembro',    [1,23,24]],
    12: ['Dezembro',    [1,25,26]],
}

d = {
    'ANEXO 1' : ['Comércio', 'Alíquota ICMS: '],
    'ANEXO 2' : ['Industria', 'Alíquota ICMS: '],
    'ANEXO 3' : ['Serviço (III)', 'Alíquota ISS: '],
    'ANEXO 4' : ['Serviço (IV)', 'Alíquota ISS: '],
    'ANEXO 5' : ['Serviço (V)', 'Alíquota ISS: '],
    'FATOR R' : ['Serviço', 'Alíquota ISS: ']
}


print('Selecione o Mes de Referencia...\n')

# Main
for x,y in dMeses.items():
    print('ID: {} - Mes: {}' .format(x, y[0]))

mes = None
while mes is None:
    try:
        iMes = input('Digite o ID do mes selecionado: ')
        mes = dMeses[int(iMes)][0]
        cols = dMeses[int(iMes)][1]
    except:
        pass


path_download = os.path.join(Path.home(), "Downloads")
arq = os.path.join(path_download, 'ALÍQUOTAS MENSAIS.xlsx')

print('Carregando {}...\n' .format(arq))

df = pd.read_excel(arq, header=2)
df2 = df.query("OBSERVAÇÕES != 'NÃO ENVIAR POR E-MAIL'").iloc[:, 0:29]
df2.set_index('CNPJ', inplace=True)

print('Carregado com Sucesso!')
print('Iniciando tratamento dos dados...\n')

#Empresas Unicas
campos = "EMPRESA;EMAIL 01".split(';')
df3 = df2[campos].drop_duplicates(keep="first")

#Seleciona qual mes sera enviado o Email
df4 = df2.iloc[:,cols]

selecao = df3['EMAIL 01'].isnull()
df3 = df3[~selecao]
df3["EMAIL 01"].replace(',' , ';' , regex=True, inplace=True)

# Montar a Mensagem
ano = 2022
msgHead = """
Bom Dia,

Segue abaixo a alíquota do mês de {}/{}.
""" .format(mes, ano)

msgFooter = """


Atenciosamente;

Única Contábil
Departamento Fiscal
(62) 3212-1200 | (62) 98228-0118 
"""   

print('Iniciando o envio dos emails...')
#Loop
for index, row1 in df3.iterrows(): 
    dfTemp = df4[(df4.index == index)]

    Title = 'ALÍQUOTA MENSAL ({}/{}) - ' .format(mes, ano) + row1["EMPRESA"] + "\n"
    EmailList = row1['EMAIL 01'] + "\n"

    msgBody = ""
    for index, row in dfTemp.iterrows(): 
        msgBody = msgBody + "\n"
        msgBody = msgBody + d[row['ANEXO SIMPLES']][0] + "\n"
        msgBody = msgBody + d[row['ANEXO SIMPLES']][1] + '{0:.2f}%'.format(row.iloc[1]*100) + "\n"
        msgBody = msgBody + 'Alíquota efetiva total: ' '{0:.2f}%'.format(row.iloc[2]*100) + "\n" 

    msgBody = msgBody.replace(".", ",")

    #Inicia o procedimento de envio de email
    msg = msgHead + msgBody + msgFooter
    EnviarEmail(EmailList, Title, msg)