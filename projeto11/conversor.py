def metros_para_quilometros(metros):
    quilometros = metros / 1000
    return quilometros

def quilometros_para_metros(quilometros):
    metros = quilometros * 1000
    return metros

def celsius_para_fahrenheit(celsius):
    fahrenheit = celsius * 9/5 + 32
    return fahrenheit

def fahrenheit_para_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5/9
    return celsius

def main():
    print("Conversor de medidas:")
    print("1 - Metros para Kilometros")
    print("2 - Kilometros para Milhas")
    print("3 - Celsius para Fahrenheit")
    print("4 - Fahrenheit para Celsius")
    print("0 - Sair")

    while True:
        escolha = int(input("Escolha uma opção: "))

        if escolha == 0:
            print("Saindo...Obrigado por utilizar o conversor de medidas. ^^")
            break

        elif escolha == 1:
            metros = float(input("Insira a quantidade de metros: "))
            resultado = metros_para_quilometros(metros)
            print(f"{metros} metros equivalem a {resultado:.2f} quilometros.")
        
        elif escolha == 2:
            quilometros = float(input("Insira a quantidade de quilometros: "))
            resultado = quilometros_para_metros(quilometros)
            print(f"{quilometros} quilometros equivalem a {resultado:.2f} metros.")

        elif escolha == 3:
            celsius = float(input("Insira a temperatura em Celsius: "))
            resultado = celsius_para_fahrenheit(celsius)
            print(f"{celsius}°C equivalem a {resultado:.2f}°F.")

        elif escolha == 4:
            fahrenheit = float(input("Insira a temperatura em Fahrenheit: "))
            resultado = fahrenheit_para_celsius(fahrenheit)
            print(f"{fahrenheit}°F equivalem a {resultado:.2f}°C.")
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()