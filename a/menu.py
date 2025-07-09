# Menu principal
from assinatura_digital import assinar_arquivo, gerar_chaves, verificar_assinatura

def menu():
    while True:
        print("\n=== MENU ASSINATURA DIGITAL ===")
        print("1. Gerar chaves")
        print("2. Assinar arquivo")
        print("3. Verificar assinatura")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            gerar_chaves()
        elif opcao == "2":
            assinar_arquivo()
        elif opcao == "3":
            verificar_assinatura()
        elif opcao == "0":
            print("👋 Encerrando...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()