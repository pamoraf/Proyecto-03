import getpass
from shamir_scheme import encrypt_file
from shamir_scheme import decrypt_file


def main_menu():
    print("Bienvenido al Sistema de Compartición de Secretos de Shamir")
    while True:
        print("\nPor favor, elige una opción:")
        print("1. Cifrar un archivo")
        print("2. Descifrar un archivo")
        print("3. Salir")

        choice = input("Ingresa tu elección (1/2/3): ")

        if choice == '1':
            encrypt_file_menu()
        elif choice == '2':
            decrypt_file_menu()
        elif choice == '3':
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Elección inválida, por favor intenta de nuevo.")

def encrypt_file_menu():
    print("\n--- Cifrar un Archivo ---")
    output_file = input("Ingresa el nombre del archivo para guardar las evaluaciones del polinomio: ")
    total_evaluations = int(input("Ingresa el número total de evaluaciones : "))
    points_needed_to_decrypt = int(input("Ingresa el número mínimo de puntos necesarios para descifrar el archivo: "))
    clear_document_file = input("Ingresa el nombre del archivo con el documento claro: ")
    password = getpass.getpass("Ingresa la contraseña : ")

    # Llama a la función de cifrado (debemos implementar esto pablo o gibran)
    encrypt_file(output_file, total_evaluations, points_needed_to_decrypt, clear_document_file, password)

def decrypt_file_menu():
    print("\n--- Descifrar un Archivo ---")
    polynomial_evaluations_file = input("Ingresa el nombre del archivo con las evaluaciones del polinomio: ")
    encrypted_document_file = input("Ingresa el nombre del archivo cifrado: ")

    # Llama a la función de descifrado (debemos implementar esto pablo o gibran)
    decrypt_file(polynomial_evaluations_file, encrypted_document_file)

if __name__ == "__main__":
    main_menu()