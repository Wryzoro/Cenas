import random
import string

def generate_password(comprimento):
    caracteres_possiveis = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(caracteres_possiveis) for _ in range(comprimento))
    return senha


comprimento = int(input("Digite o comprimento da senha: "))

senha_gerada = generate_password(comprimento)

print(f"Sua senha gerada é: {senha_gerada}")