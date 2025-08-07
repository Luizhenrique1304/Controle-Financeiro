import csv
import os
from datetime import datetime
import platform
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

ARQUIVO = 'dados.csv'

if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["Data", "Tipo", "Descrição", "Valor"])

def adicionar_transacao(tipo, descricao, valor):
    with open(ARQUIVO, mode="a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow([datetime.now().strftime("%d/%m/%Y"), tipo, descricao, valor])
    print(f"{tipo} adicionada com sucesso!")

def exibir_extrato():
    saldo = 0
    print("\n=== Extrato Financeiro ===")
    with open(ARQUIVO, mode="r", encoding="utf-8") as f:
        leitor = csv.reader(f)
        next(leitor)
        for linha in leitor:
            data, tipo, descricao, valor = linha
            valor = float(valor)
            if tipo == "Receita":
                saldo += valor
            else:
                saldo -= valor
            print(f"{data} | {tipo} | {descricao} | R$ {valor:.2f}")
        print(f"\nSaldo atual: R$ {saldo:.2f}")

def abrir_csv():
    if platform.system() == "Windows":
        os.startfile(ARQUIVO)
    elif platform.system() == "Darwin":
        subprocess.call(["open", ARQUIVO])
    else:
        subprocess.call(["xdg-open", ARQUIVO])

def gerar_grafico():
    if os.path.getsize(ARQUIVO) == 0:
        print("Nenhum dado disponivel para gerar gráficos.")
        return
    
    df = pd.read_csv(ARQUIVO)

    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")
    df["Mes"] = df["Data"].dt.strftime("%Y-%m")

    resumo = df.groupby(["Mes", "Tipo"])["Valor"].sum().unstack(fill_value=0)

    resumo.plot(kind="bar", figsize=(10,5))
    plt.title("Receitas x Despesas por Mês")
    plt.ylabel("Valor (R$)")
    plt.xlabel("Mês")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def menu():
    while True:
        print("\n=== Controle Financeiro ===")
        print("1. Adicionar Receita")
        print("2. Adicionar Despesa")
        print("3. Ver Extrato")
        print("4. Abrir CSV no Excel")
        print("5. Gerar Gráfico")
        print("6. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            descricao = input("Descrição da Receita: ")
            valor = float(input("Valor: "))
            adicionar_transacao("Receita", descricao, valor)
        elif opcao == "2":
            descricao = input("Descrição da Despesa: ")
            valor = float(input("Valor: "))
            adicionar_transacao("Despesa", descricao, valor)
        elif opcao == "3":
            exibir_extrato()
        elif opcao == "4":
            abrir_csv()
        elif opcao == "5":
            gerar_grafico()
        elif opcao == "6":
            print("Saindo... até mais!")
            break
        else:
            print("Opção inválida!")
menu()