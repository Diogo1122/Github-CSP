import psycopg2 as ps
from matplotlib import pyplot as plt

# query responsavel pela insercao na base de dados, tabela lpv
Sql_Statement = """SELECT lpv FROM PUBLIC."LPV" 
WHERE machine_id = %s AND channel = %s AND extration_date >= %s AND extration_date <= %s """

records = [input('escolha a máquina:'), input('escolha o canal:'), input('escolha a data inicial: yyyy-mm-dd'),
           input('escolha a data final: yyyy-mm-dd')]
print(records)


def visualize_data_(_records, hostname, dbname, _port, _user, _password):
    try:
        # connectar á base de dados
        conn = ps.connect(host=hostname,
                          database=dbname,
                          port=_port, user=_user,
                          password=_password)
        print("Connected to Database")
        cur = conn.cursor()
        # operacao para inserir os dados na base de dados
        cur.execute(Sql_Statement, _records)
        lpv_records = cur.fetchall()
        cur.close()
    except (Exception, ps.DatabaseError) as error:
        print("Error pushing Data")
        print(error)
    finally:
        if conn is not None:
            # fecha conexao com base de dados
            conn.close()
    return lpv_records


lpv_numbers = visualize_data_(records, "localhost", "Prototipo Cork V01", "5432", "postgres", "password")

plt.plot(lpv_numbers)
plt.title('LPV NUMBERS on MACHINE {} CHANNEL {} BETWEEN {} AND {}'.format(records[0], records[1], records[2], records[3]))
plt.show()