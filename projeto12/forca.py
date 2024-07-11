import random

palavras = ['abacaxi', 'sporting', 'casa', 'computador', 'futebol', 'música', 'caneta', 'livro', 'elefante', 'maravilha']

palavra_secreta = random.choice(palavras)

max_tentativas = 6

letras_adivinhadas = []

def exibir_palavra(palavra, letras_adivinhadas):
    resultado = ''
    for letra in palavra:
        if letra in letras_adivinhadas:
            resultado += letra + ' '
        else:
            resultado += '_ '
    return resultado.strip()


#Loop do jogo ate as max tentativas

while True:
    # Mostrar o estado atual do jogo (palavra com letras adivinhadas e traços)
    print("\nPalavra:", exibir_palavra(palavra_secreta, letras_adivinhadas))

    # Pedir ao jogador para fazer uma tentativa
    tentativa = input("Digite uma letra ou a palavra completa: ").lower()

    if tentativa == palavra_secreta:
        print("Parabéns! Você acertou a palavra secreta:", palavra_secreta)
        break
    elif tentativa in letras_adivinhadas:
        print("Você já tentou esta letra. Tente outra.")
    elif len(tentativa) == 1 and tentativa.isalpha():
        # A tentativa é uma letra válida
        letras_adivinhadas.append(tentativa)
        if tentativa not in palavra_secreta:
            max_tentativas -= 1
            print(f"Letra '{tentativa}' não está na palavra secreta. Tentativas restantes: {max_tentativas}")
    else:
        print("Entrada inválida. Por favor, digite apenas uma letra ou a palavra completa.")

    # Verificar se o jogador ganhou ou perdeu
    if ''.join(letras_adivinhadas) == palavra_secreta:
        print("\nParabéns! Você acertou a palavra secreta:", palavra_secreta)
        break
    elif max_tentativas == 0:
        print("\nGame Over! Você excedeu o número máximo de tentativas.")
        print("A palavra secreta era:", palavra_secreta)
        break