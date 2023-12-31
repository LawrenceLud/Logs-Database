import tkinter as tk
from tkinter import messagebox
import pandas as pd
import logging
import mysql.connector

logging.basicConfig(filename="logs.txt", level=logging.INFO, format='%(asctime)s - %(message)s - %(levelname)s')

def executar_script():
    try:
        db_connection = mysql.connector.connect(
            host="",
            user="",
            password="",
            database=""
        )

        cliente = entry_cliente.get()
        avaliacao = entry_avaliacao.get()

        data = {'Clientes': [cliente],
                'Avaliação Para Os Clientes Especificados': [int(avaliacao)]}

        df = pd.DataFrame(data)

        print("Dados programados: ")
        logging.info(df)
        logging.warning("Logs de Clientes, Apenas Administradores podem ter acesso!")
        print(df)

        media_avaliacao = df['Avaliação Para Os Clientes Especificados'].mean()
        print("\nMédia: ", media_avaliacao)

        cursor = db_connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tabela_de_avaliacoes (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            cliente VARCHAR(255) NOT NULL,
                            avaliacao INT NOT NULL)''')

        for index, row in df.iterrows():
            cliente = row['Clientes']
            avaliacao = row['Avaliação Para Os Clientes Especificados']
            query = "INSERT INTO tabela_de_avaliacoes (cliente, avaliacao) VALUES (%s, %s)"
            values = (cliente, avaliacao)
            cursor.execute(query, values)

        db_connection.commit()
        cursor.close()
        db_connection.close()

        messagebox.showinfo("Sucesso", "Foi Registrado as Logs no Banco de Dados com Sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

root = tk.Tk()
root.title("Registrar Logs")
root.geometry("500x200")

label_cliente = tk.Label(root, text="Nome Do Cliente")
label_cliente.pack()
entry_cliente = tk.Entry(root)
entry_cliente.pack()

label_avaliacao = tk.Label(root, text="Avaliação")
label_avaliacao.pack()
entry_avaliacao = tk.Entry(root)
entry_avaliacao.pack()

executar_button = tk.Button(root, text="Registrar logs no banco de dados", command=executar_script)
executar_button.pack()

root.mainloop()
