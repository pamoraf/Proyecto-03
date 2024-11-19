import getpass
from shamir_scheme import encrypt, decrypt, read_evaluations
from file_manager import (
    read_binary_file,
    read_text_file,
    write_binary_file,
    write_text_file
)

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
    evaluations_path = input("Ingresa el nombre del archivo para guardar las evaluaciones del polinomio: ")
    n = int(input("Ingresa el número total de evaluaciones : "))
    t = int(input("Ingresa el número mínimo de puntos necesarios para descifrar el archivo: "))
    clear_file_path = input("Ingresa el nombre del archivo con el documento claro: ")
    password = getpass.getpass("Ingresa la contraseña : ")
    text = read_text_file(clear_file_path)
    bytes, total_evaluations = encrypt(text, password, n, t)
    encrypt_file_path = clear_file_path[:len(clear_file_path) - 4] + ".ecr"
    write_binary_file(encrypt_file_path, bytes)
    write_text_file(evaluations_path, total_evaluations)

def decrypt_file_menu():
    print("\n--- Descifrar un Archivo ---")
    polynomial_evaluations_file = input("Ingresa el nombre del archivo con las evaluaciones del polinomio: ")
    encrypt_file_path = input("Ingresa el nombre del archivo cifrado: ")
    polynomial_evaluations = read_evaluations(polynomial_evaluations_file)
    clear_file_path = encrypt_file_path[:len(encrypt_file_path) - 4] + ".txt"
    text = decrypt(polynomial_evaluations_file, polynomial_evaluations)
    write_text_file(clear_file_path, text)

if __name__ == "__main__":
    display_menu()