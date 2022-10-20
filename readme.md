## Objetivo
Desenvolver um pipeline de dados ETL(Extract, transform, load) que se conecta a API do google sheets, acessa o google planilhas, coleta os dados transformando-os em dataframe python, em seguida, trata e transforma esses dados, e finalmente carrega os dados em um sistema gerenciador de banco de dados relacional.

## Solução proposta
<b>Stacks:</b> 
- Python (gspread, oauth2client.service_account, pandas, psycopg2, time, sqlalchemy, smtplib, email.mime.multipart, email.mime.text, smtplib)
- Google Sheets API
- Google Planilhas
- PostgreSQL

<b>Arquitetura:</b>  Após feita toda a preparação de ativar o Google Sheets API para a conta google e de configurar as permissões de acesso devidamente. No programa, a função "main" inicialmente utilizara a biblioteca "psycopg2" pare coletar a instância de conexão e o cursor do banco de dados Postgres , após isso é chamada a função que se conecta a API do Google Sheets, essa função transforma todas as colunas e linhas presentes em um dataframe, em seguida, é realizado a modelagem do dataframe apagando algumas colunas indesejadas, em seguida, o programa fara uma limpeza nos nomes de colunas e também fara a alteração de tipos de dados que deveriam ter sido reconhecidos como tipos numéricos, no caso inteiros, assim para ser possível fazer a inserção dos dados no banco de dados com a tipagem correta, já que inicialmente esses tipos não foram reconhecidos automaticamente, após todo o tratamento para se obter a modelagem de dados correta, o programa se conectara ao banco de dados Postgres e fara a deleção de todos os registros antigos que já estavam cadastrados anteriormente, após isso, ainda em nosso banco de dados Postgres, é feita inserção do nosso dataframe já tratado e com dados atualizados, ao finalizar todo o processo, é chamada uma função que enviara um e-mail com o tempo total de execução do programa e seus status de execução sendo como "sucesso" se tudo ocorrer bem ou como "fallha" caso algo der errado.


## Resultados
<b>Problemas resolvidos:</b> Houve uma complexidade na hora de realizar as permissões de acesso corretamente, pois para que o programa consiga se conectar é necessário fazer uma chave de acesso de formato json,  e a também foi um desafio fazer a configuração do script para acessar a planilha corretamente, já que se utiliza bibliotecas novas que eu ainda possuía conhecimento, mas com a pesquisa e leitura de conteúdos, foi possível solucionar os problemas e finalizar o desenvolvimento com sucesso.
Fontes de conhecimento para todo o desenvolvimento do programa, com a parte técnica de configuração, ativação da API, e a geração de permissões necessária para o possível acesso à planilha:
https://ichi.pro/pt/como-ativar-o-acesso-do-python-ao-planilhas-google-250853149332571 - chave de acesso json
https://pt.linkedin.com/pulse/manipulando-planilhas-do-google-usando-python-renan-pessoa - configuração de acesso script
https://www.iperiusbackup.net/pt-br/como-habilitar-a-api-do-google-drive-e-obter-credenciais-de-cliente/ - ativação da Google Sheets API


<b>Resultado final:</b>
Por questões de segurança, nos dois arquivos aqui disponíveis, ambos estão sem as credências de acesso utilizadas no desenvolvimento, mas o processo ETL foi finalizado com sucesso, o script possui comentários explicativos, assim facilitando e possibilitando a replicação deste projeto em outro problema de negócio. Basta seguir conteúdos mencionados para criação de chave de acesso json e ativação da Google Sheets API. 
Obrigado.
