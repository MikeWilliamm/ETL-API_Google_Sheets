import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import psycopg2 
import time
from sqlalchemy import create_engine
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

#Variável para capturar o tempo de execução total do programa
start_time = time.time()
#Variável para definir a situação final de execução do programa
frase = ''

#Função para apagar todos os dados antigos antes de fazer a inserção dos novos
def conect():
    #Deinifir credencias de acesso ao Postgres
    host = ""
    dbname = ""
    user = ""
    password = ""
    sslmode = "allow"


    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string) 
    print("Conexao estabelecida")
    cursor = conn.cursor()

    return conn, cursor
    
#Função para acessar planilha online e transformá-la em um DataFrame
def planilha_to_df(): 
    #Escopo utilizado
    scope = ['https://spreadsheets.google.com/feeds']

    #Dados de autenticação
    credentials = ServiceAccountCredentials.from_json_keyfile_name(r'', scope)#Deve ser passado o diretório do arquivo json que contem as credenciais de acesso

    #Se autentica
    gc = gspread.authorize(credentials)

    #Abre a pasta de planilhas
    wks = gc.open_by_key('') #id da planilha encontra em sua URL de acesso

    #Seleciona a segunda planilha
    worksheet = wks.get_worksheet(2)

    #Transforma planilha em DataFrame
    df = pd.DataFrame(worksheet.get_all_records())
    print('Planilha transformada em DataFrame')
    return df

#Função para apagar colunas indesejadas
def apagaColunas(df):
    df = df.drop(columns=['id_loja_cliente'])
    df = df.drop(columns=['ramo'])
    df = df.drop(columns=['tipo'])
    df = df.drop(columns=[''])

    return df

#Função para alterar o nome das colunas e converter tipos de dados 
def altera(df):
    #Altera nome das colunas
    df = df.rename({"Store_id":"store_id"}, axis="columns")
    df = df.rename({"Store_Name":"store_name"}, axis="columns")
    df = df.rename({"EAN":"ean"}, axis="columns")
    df = df.rename({"Name_Produto":"name_product"}, axis="columns")
    df = df.rename({"Divisão":"divisao"}, axis="columns")
    df = df.rename({"Qtd Mininima tipo 1":"qtdmin"}, axis="columns")
    df = df.rename({"Qtd Mininima tipo 2":"qtdmin2"}, axis="columns")

    #Altera tipo de dado
    df['ean'] = pd.to_numeric(df['ean'], errors='coerce').astype('Int64')
    df['qtdmin2'] = pd.to_numeric(df['qtdmin2'], errors='coerce').astype('Int64')
    

    return df

#Função que faz a inserção do DataFrame final no banco de dados
def insert(df):
    engine = create_engine('postgresql://user:pass@host:port/database')

    df.to_sql(name='products', con=engine, if_exists='append', schema='sales', index = False)
    
    print('\nDados inseridos no banco!\n')

#Função que realiza o envio de e-mail com o status de execução final
def EmailNapp(frase):

  smtp_server = 'smtp.gmail.com' 
  sender_email = 'rotinas@gmail.com' 
  recipients = ['mike-william98@hotmail.com']
  password = 'Your Pass'
  port = 587
  
  subject = 'Title email'
  body = frase #Conteúdo do e-mail
  message = MIMEMultipart()
  message['From'] = sender_email
  message['To'] =  ', '.join(recipients)
  message['Subject'] = subject 
  mail_content = body
  message.attach(MIMEText(mail_content, 'plain'))

  server = smtplib.SMTP(smtp_server, port)
  server.starttls()
  server.login(sender_email, password)
  text = message.as_string()
  server.sendmail(sender_email, recipients, text)
  
  return '>> Email sent!'

#Função main, aqui se concentra a orquestração de execução do script
def main():
    try:
        conn, cursor = conect()

        df = planilha_to_df()

        df = apagaColunas(df)

        df = altera(df)

        try:
            insert(df)
            cursor.execute("TRUNCATE TABLE sales.products;")
            conn.commit()
            insert(df)
        except:
            conn.rollback()
            
        cursor.close()
        conn.close()

        end_time = time.time()
        time_f1 = end_time - start_time

        frase = ('Rotina de Produtos Executada com sucesso! \nTempo de Execução: {:.12f}'.format(time_f1) + ' segundos')
        
    except:
        frase = 'ERRO AO EXECUTAR ROTINA!!!'
    EmailNapp(frase)
        
    
        
    print('Email Enviado!')    
    print(frase)
    

    
main()



'''Fontes de conhecimento para todo o desenvolvimento do programa, com a parte técnica de configuração, ativação da API, e a geração de permissões necessária para o possível acesso à planilha:
https://ichi.pro/pt/como-ativar-o-acesso-do-python-ao-planilhas-google-250853149332571 - chave de acesso json
https://pt.linkedin.com/pulse/manipulando-planilhas-do-google-usando-python-renan-pessoa - configuração de acesso script
https://www.iperiusbackup.net/pt-br/como-habilitar-a-api-do-google-drive-e-obter-credenciais-de-cliente/ - ativação da Google Sheets API
'''






