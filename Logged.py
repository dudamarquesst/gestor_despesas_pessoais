from App import app
from datetime import datetime
from models.usuario import *
from models.categoria import *
from models.despesa import *

def display_logged_in_menu():
    # Atualizar versão mais recente do usuário
    app.active_user = get_usuario_by_id(app.active_user["id"])

    print("Menu - Selecione uma das opções abaixo:")
    print("0 - Sair")
    print("1 - Atualizar Meta Mensal")
    print("2 - Adicionar Categoria")
    print("3 - Cadastrar Despesa")
    print("4 - Listar Despesas")
    print("5 - Gerar relatório de despesas")

    option = input("Digite o número da opção desejada: ")
# Apresentar menu de opções para usuário logado
    match option:
        case "0":
            logout()
        case "1":
            update_monthly_goal()
        case "2":
            add_category()
        case "3":
            add_expense()
        case "4":
            list_expenses()
        case "5":
            generate_report()
   
def logout():
    # Deslogar usuário
    confirm = input("Deseja realmente sair? (S/N)")
    if confirm == "S" or confirm == "s":
        app.set_active_user(None)

def update_monthly_goal():
    # Alterar meta mensal do usuário
    print("Atualizar Meta Mensal")
    
    while True:
        # Loop infinito
        print("Meta mensal atual: R${:.2f}".format(app.active_user["meta_mensal"]))

        new_goal = float(input("Digite a nova meta de gastos mensal: (0 para sair) R$ "))
        # Receber do usuário nova meta mensal
        
        if(new_goal == 0):
            return

        if(new_goal > 0):
            # Condição para sair do loop
            break
            # Acabou o loop
        
        print("Valor inválido, tente novamente.")
            

    update_meta_mensal(app.active_user["id"], new_goal)

    print("Meta atualizada com sucesso!")

def add_category():
# Cadastrar categoria para o usuário atual
    print("Adicionar Categoria")
    
    category_name = input("Digite o nome da categoria: ")
 # Receber do usuário o nome da categoria
    inserir_categoria(category_name, app.active_user["id"])
    
    print("Categoria adicionada com sucesso!")
  
def add_expense():
    # Cadastrar despesas
    print("Cadastrar Despesa")

    # Receber descrição da despesa
    description = input("Digite a descrição da despesa: ")

    # Receber valor da despesa
    while True:
        value = float(input("Digite o valor da despesa: R$"))

        if(value <= 0):
            print("Valor inválido, tente novamente.")
        else:
            break

    active_user_categories = get_user_categories(app.active_user["id"])

    # Receber categoria da despesa
    while True:
        print("Categorias disponíveis:")

        for index, category in enumerate(active_user_categories):
            print(f"{index} - {category["nome_categoria"]}")

        try:
            category_index = int(input("Digite a categoria da despesa: "))

            if  category_index < 0 or category_index >= len(active_user_categories):
                print("Categoria inválida, tente novamente.")
            else:
                category = active_user_categories[category_index]['id']
                break
        except ValueError:
            print("Categoria inválida, tente novamente.")

    # Receber data da despesa
    while True:
        date = input("Digite a data da despesa (DD/MM/AAAA): ")

        try:
            datetime.strptime(date, "%d/%m/%Y")
            break
        except ValueError:
            print("Data inválida, tente novamente.")

    expense = {
        "usuario": app.active_user['id'],
        "categoria": category,
        "nome_despesa": description,
        "valor": value,
        "data": date
    }

    app.expenses.append(expense)
    inserir_despesa(**expense)
    print("Despesa cadastrada com sucesso!")

def list_expenses():
    # Listar despesas
    print("Listar Despesas")

    user_expenses = get_user_expenses(app.active_user['id'])

    if not user_expenses:
        print("Nenhuma despesa encontrada.")
        return

    print("Despesas cadastradas:")
    for expense in user_expenses:
        print(f"{expense['data']}: {expense['nome_despesa']} - R${expense['valor']:.2f}")

def generate_report():
    # Gerar relatório mensal
    print("Gerar relatório de despesas")

    # Listar meses com despesas disponíveis para o usuário ativo
    user_expenses = get_user_expenses(app.active_user['id'])
    if not user_expenses:
        print("Nenhuma despesa encontrada.")
        return

    months = set()
    for expense in user_expenses:
        expense_date = datetime.strptime(expense["data"], "%d/%m/%Y")
        months.add(expense_date.strftime("%m/%Y"))

    print("Meses disponíveis:")
    for month in months:
        print(month)

    # Receber mês para gerar relatório
    while True:
        selected_month = input("Digite o mês para gerar o relatório (MM/AAAA): ")
        try:
            datetime.strptime(selected_month, "%m/%Y")
            break
        except ValueError:
            print("Mês inválido, tente novamente.")

    # Listar despesas do mês selecionado
    selected_month_expenses = [
        expense for expense in user_expenses
        if datetime.strptime(expense["data"], "%d/%m/%Y").strftime("%m/%Y") == selected_month
    ]

    if not selected_month_expenses:
        print("Nenhuma despesa encontrada para o mês selecionado.")
        return

    print(f"Despesas para {selected_month}:")
    total_expenses = 0
    for expense in selected_month_expenses:
        print(f"{expense['data']}: {expense['nome_despesa']} - R${expense['valor']:.2f}")
        total_expenses += expense["valor"]

    # Calcular total de despesas do mês e comparar com a meta mensal
    print(f"Total de despesas: R${total_expenses:.2f}")

    if total_expenses > app.active_user["meta_mensal"]:
        print(f"Você excedeu sua meta mensal de R${app.active_user['meta_mensal']:.2f}!")
    else:
        print(f"Você está dentro da sua meta mensal de R${app.active_user['meta_mensal']:.2f}.")
