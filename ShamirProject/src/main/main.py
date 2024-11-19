import getpass
from shamir_scheme import encrypt_file
from shamir_scheme import decrypt_file

def display_menu():
    """
    Displays user input menu.
    """
    print("Bienvenido al Sistema de Compartición de Secretos de Shamir")
    menu_active = True
    while menu_active:
        print("\nPor favor, elige una opción:")
        print("(c) Cifrar un archivo")
        print("(d) Descifrar un archivo")
        print("(x) Regresar")
        choice = input("Ingresa tu elección (c/d/x): ").strip()
        if choice == 'c':
            encrypt_file_menu()
        elif choice == 'd':
            decrypt_file_menu()
        elif choice == 'x':
            print("Saliendo del programa. ¡Hasta luego!")
            menu_active = False
        else:
            print("Elección inválida, por favor intenta de nuevo.")

def encrypt_file_menu():
    print("\n--- Cifrar un Archivo ---")
    output_file = input("Ingresa el nombre del archivo para guardar las evaluaciones del polinomio: ")
    total_evaluations = int(input("Ingresa el número total de evaluaciones : "))
    points_needed_to_decrypt = int(input("Ingresa el número mínimo de puntos necesarios para descifrar el archivo: "))
    clear_document_file = input("Ingresa el nombre del archivo con el documento claro: ")
    password = getpass.getpass("Ingresa la contraseña : ")
    encrypt_file(output_file, total_evaluations, points_needed_to_decrypt, clear_document_file, password)

def decrypt_file_menu():
    print("\n--- Descifrar un Archivo ---")
    polynomial_evaluations_file = input("Ingresa el nombre del archivo con las evaluaciones del polinomio: ")
    encrypted_document_file = input("Ingresa el nombre del archivo cifrado: ")
    decrypt_file(polynomial_evaluations_file, encrypted_document_file)

if __name__ == "__main__":
    display_menu()