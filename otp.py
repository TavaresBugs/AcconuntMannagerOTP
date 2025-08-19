import time
import hmac
import hashlib
import struct
import base64

def gerar_totp(secret_base32, interval=30, digits=6):
    # Decodifica a chave Base32 (fornecida pelo servidor)
    key = base64.b32decode(secret_base32.upper())
    
    # Pega o tempo atual dividido pelo intervalo
    counter = int(time.time()) // interval

    # Converte o contador para bytes (8 bytes big-endian)
    msg = struct.pack(">Q", counter)

    # Cria o HMAC-SHA1
    hmac_sha1 = hmac.new(key, msg, hashlib.sha1).digest()

    # Truncamento dinâmico (extrai parte do HMAC)
    offset = hmac_sha1[-1] & 0x0F
    code = struct.unpack(">I", hmac_sha1[offset:offset+4])[0] & 0x7FFFFFFF

    # Reduz para o número de dígitos (6 ou 8 normalmente)
    return str(code % (10 ** digits)).zfill(digits)

# 🔐 INSIRA AQUI A CHAVE BASE32 DADA PELO SERVIDOR
meu_segredo = "##########"  # <--- Substitua isso pela sua chave
def main ():
    # 📲 Gera o código TOTP atual
    codigo = gerar_totp(meu_segredo)
    print("Seu código TOTP:", codigo)

if __name__ == "__main__":
    main()


