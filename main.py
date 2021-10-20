import psycopg2 as ps
import easygui

# escolher ficheiro
File = open(easygui.fileopenbox(), 'r')
# Tratamento do ficheiro
filename = File.name
FileProp = filename.split('\\')
# ver Fileprop, posicoes podem mudar dependendo de onde se encontra o ficheiro
Date = FileProp[6]
Machine = int(FileProp[7][3:4])
NameProp = FileProp[7].split("_")
if NameProp[6][0:4] == "prod":
    Operation = "Production"
else:
    Operation = "Empty"
Cycle = 0
Content = File.read().split(',')
data_list = []
# Passar dados para lista para serem enviados para a database
for i in range(len(Content)):
    Channel = i % 8 + 1
    if i % 8 == 0:
        Cycle += 1

    Value = Content[i]
    # junta no final da lista uma entrada com estes parametros
    data_list.append([Machine, Channel, Cycle, Date, Value, Operation])
    i += 1

# query responsavel pela insercao na base de dados, tabela lpv
Sql_Statement = """INSERT INTO PUBLIC."LPV" (machine_id, channel, cicle, extration_date, lpv, operation)
 VALUES (%s,%s,%s,%s,%s,%s) RETURNING record_id """


def transfer_data_to_db(list, hostname, dbname, _port, _user, _password):
    transfer_list = list
    try:
        # connectar á base de daddos
        conn = ps.connect(host=hostname,
                          database=dbname,
                          port=_port, user=_user,
                          password=_password)
        print("Connected to Database")
        cur = conn.cursor()
        # operacao para inserir os dados na base de dados
        cur.executemany(Sql_Statement, transfer_list)
        conn.commit()
        cur.close()
        print("Data Pushed into Database")
    except (Exception, ps.DatabaseError) as error:
        print("Error pushing Data")
        print(error)
    finally:
        if conn is not None:
            # fecha conexao com base de dados
            conn.close()


# executar funcao
transfer_data_to_db(data_list, "localhost", "Prototipo Cork V01", "5432", "postgres", "Joanabonita7@")
