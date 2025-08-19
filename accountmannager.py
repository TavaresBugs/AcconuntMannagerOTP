import json
import tkinter as tk
import otp
from PIL import Image, ImageTk

contas = []

def box_default(user_info, window, coluna,copy_image):
    # The main container for this account
    frame_box = tk.Frame(window, relief="solid", borderwidth=1)
    frame_box.grid(row=0, column=coluna, padx=10, pady=10) # Uses 'coluna'
    # The Service Name (Title)
    label_servico = tk.Label(frame_box, text=user_info["servico"], font=("Helvetica", 14, "bold"))
    label_servico.grid(row=0, column=0, columnspan=2, pady=5) # Grid inside frame starts at 0
    # The "Usuário:" text label
    label_usuario_title = tk.Label(frame_box, text="Usuário:")
    label_usuario_title.grid(row=1, column=0, sticky="w") # Grid inside frame starts at 0
    # The "Usuário:" button
    button_usuario = tk.Button(frame_box, image=copy_image,command=lambda:copiar_clipboard(window, user_info['usuario']))
    button_usuario.grid(row=1, column=2, sticky="e")
    # The Entry widget to display the username
    entry_usuario = tk.Entry(frame_box, width=30, justify='center') # No 'text=' parameter
    entry_usuario.insert(0, user_info["usuario"])
    entry_usuario.config(state="readonly")
    entry_usuario.grid(row=1, column=1) # Placed in the second column OF THE FRAME
    # The "Password:" text label
    label_password_title = tk.Label(frame_box, text="Password:")
    label_password_title.grid(row=2, column=0, sticky="w") # Grid inside frame starts at 0
    # The "Password:" button
    button_password = tk.Button(frame_box, image=copy_image,command=lambda:copiar_clipboard(window, user_info['senha']))
    button_password.grid(row=2, column=2, sticky="e") # Grid inside frame starts at 0
    # The Entry widget to display the password
    entry_password = tk.Entry(frame_box, width=30, justify='center') # No 'text=' parameter
    entry_password.insert(0, user_info["senha"])
    entry_password.config(state="readonly")
    entry_password.grid(row=2, column=1) # Placed in the second column OF THE FRAME
    # The "OTP:" text label
    label_OTP_title = tk.Label(frame_box, text="OTP:")
    label_OTP_title.grid(row=3, column=0, sticky="w") # Grid inside frame starts at 0
    # Generating OTP
    chave = user_info['chave_otp']
    otp_gerado = otp.gerar_totp(chave)
    # The Entry widget to display the OTP
    entry_OTP = tk.Entry(frame_box, width=30, justify='center') # No 'text=' parameter
    entry_OTP.insert(0, otp_gerado)
    entry_OTP.config(state="readonly")
    entry_OTP.grid(row=3, column=1) # Placed in the second column OF THE FRAME
    atualizar_otp(entry_OTP, chave)
    # The "OTP:" button
    button_OTP = tk.Button(frame_box, image=copy_image,command=lambda:copiar_clipboard(window, entry_OTP.get()))
    button_OTP.grid(row=3, column=2, sticky="e") # Grid inside frame starts at 0

def atualizar_otp(entry_widget, segredo):
    # Gera o código mais recente
    codigo_atual = otp.gerar_totp(segredo)

    # Atualiza o texto do Entry na tela
    entry_widget.config(state="normal")
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, codigo_atual)
    entry_widget.config(state="readonly")

    # Agenda a si mesma para rodar de novo em 1 segundo (1000 ms)
    entry_widget.after(1000, lambda: atualizar_otp(entry_widget, segredo))

def alternar_visibilidade_senha(entry_da_senha):
    # Pega o estado atual da propriedade 'show'
    estado_atual = entry_da_senha.cget("show")

    if estado_atual == "*":
        # A senha está escondida. O que fazemos para MOSTRAR o texto?
        entry_da_senha.config(show="")
    else:
        # A senha está visível. O que fazemos para ESCONDER com asteriscos?
        entry_da_senha.config(show="*")
    
# Coloque esta função junto com as outras (fora da main)
def copiar_clipboard(janela_principal, texto_a_copiar):
    janela_principal.clipboard_clear()
    janela_principal.clipboard_append(texto_a_copiar)
    print(f"Texto '{texto_a_copiar}' copiado!")

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
    copy = Image.open("copy.png")
    copy_redimencionado = copy.resize((36,36), Image.Resampling.LANCZOS)
    janela.imagem_copiar = ImageTk.PhotoImage(copy_redimencionado)
    for index, conta in enumerate(contas):
        box_default(conta,janela,index,janela.imagem_copiar)
    janela.mainloop()



main()