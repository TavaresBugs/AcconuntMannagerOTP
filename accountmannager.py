import json
import tkinter as tk

contas = []

def box_default(user_info,window,coluna):
    frame_box = tk.Frame(window)
    frame_box.grid(row=0, column=coluna)
    label_servico = tk.Label(frame_box, text=user_info["servico"])
    label_usuario = tk.Label(frame_box, text=user_info["usuario"])
    label_usuario.grid(row=1, column=coluna)
    label_servico.grid(row=0, column=coluna)


def carregar_contas():
    with open('contas.json', 'r') as read:
        contas = json.load(read)
        return contas

def encontrar_conta(lista_de_contatos, servico_procurado):
    for conta in lista_de_contatos:
        if conta["servico"] == servico_procurado:
            return conta
    return None

def add_contas(contas):
    servico = input("Esse OTP refere a qual servico: ")
    user = input("Nome do usuario cadastrado: ")
    password = input("Senha do usuario: ")
    otp = input("Senha OTP: ") 
    newuser = {
        "servico":servico,
        "usuario":user,
        "senha":password,
        "chave_otp":otp
        }
    contas.append(newuser)
    print("Usuario adicionado com Sucesso.")
    return contas

def salvar_contas(lista_de_contas):
    with open('contas.json', 'w') as f:
        json.dump(lista_de_contas, f, indent=4)
        print("Alteracoes Salvas")


### Main Antiga usando o Console ###
'''
def main():
    contas = carregar_contas()
    while True:
        try:
            print("1. Add Contatos / 2. Encontrar Conta / 3. Salvar Contas")
            resposta = input()
            if int(resposta) == 1:
                add_contas(contas)
            elif int(resposta) == 2:
                servico = input("Qual servico desejado ? ")
                encontrada = encontrar_conta(contas, servico)
                if encontrada:
                    print("--- Conta Encontrada ---")
                    print(encontrada)
                else:
                        print("--- Serviço não encontrado. ---")
            elif int(resposta) == 3:
                salvar_contas(contas)
                print("Contas salvas com sucesso. Adeus!")
                break
            else:
                    print("Erro: Opção inválida. Por favor, escolha uma das opções.")
        except ValueError:
            print("Erro: Por favor, digite apenas o número da opção (1, 2 ou 3).")
'''

def main():
    contas = carregar_contas()
    janela = tk.Tk()
    janela.title("Gerenciador de Contas e OTP")
    for index, conta in enumerate(contas):
        box_default(conta,janela,index)


    janela.mainloop()



main()