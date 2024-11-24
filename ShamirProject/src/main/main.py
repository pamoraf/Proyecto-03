import argparse
import getpass
from shamir_scheme import generate_shares, reconstruct_secret
from cipher import encrypt, decrypt
from io_manager import (
    read_binary_file,
    read_text_file,
    write_binary_file,
    write_text_file,
    format_evaluations,
)

def main():
    """
    Función principal para manejar los argumentos de línea de comandos y ejecutar la función
    de encriptación o desencriptación apropiada basada en el comando proporcionado.
    """
    parser = argparse.ArgumentParser(description="Esquema de Compartición de Secretos de Shamir")
    subparsers = parser.add_subparsers(dest='command', help='Ayuda de sub-comando')

    # Sub-parser para el comando de encriptar
    encrypt_parser = subparsers.add_parser('c', help='Encriptar un archivo')
    encrypt_parser.add_argument('eval_file', type=str, help='Ruta para guardar las evaluaciones del polinomio')
    encrypt_parser.add_argument('n', type=int, help='Número total de evaluaciones (n > 2)')
    encrypt_parser.add_argument('t', type=int, help='Número mínimo de puntos necesarios para desencriptar (1 < t ≤ n)')
    encrypt_parser.add_argument('input_file', type=str, help='Archivo con el documento a encriptar')

    # Sub-parser para el comando de desencriptar
    decrypt_parser = subparsers.add_parser('d', help='Desencriptar un archivo')
    decrypt_parser.add_argument('eval_file', type=str, help='Archivo con al menos t de las n evaluaciones del polinomio')
    decrypt_parser.add_argument('encrypted_file', type=str, help='Archivo con el documento encriptado')

    args = parser.parse_args()

    try:
        if args.command == 'c':
            encrypt_file(args.eval_file, args.n, args.t, args.input_file)
        elif args.command == 'd':
            decrypt_file(args.eval_file, args.encrypted_file)
        else:
            parser.print_help()
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def encrypt_file(eval_file, n, t, input_file):
    """
    Encripta un archivo y genera evaluaciones polinomiales para el Esquema de Compartición de Secretos de Shamir.

    Args:
        eval_file (str): Archivo para guardar las evaluaciones del polinomio.
        n (int): Número total de evaluaciones (n > 2).
        t (int): Número mínimo de puntos necesarios para desencriptar (1 < t ≤ n).
        input_file (str): Archivo con el documento claro.
    """
    try:
        if n <= 2 or t <= 1 or t > n:
            print("Valores inválidos para n y t. Asegúrate de que n > 2 y 1 < t ≤ n.")
            return

        password = getpass.getpass("Introduce la contraseña: ")
        text = read_text_file(input_file)
        encrypted_content = encrypt(text, password)
        write_binary_file(input_file + ".enc", encrypted_content)

        secret = int.from_bytes(encrypted_content, 'big')
        shares = generate_shares(secret, n, t)
        formatted_shares = format_evaluations(shares)
        write_text_file(eval_file, formatted_shares)
        print(f"Archivo encriptado y guardado en: {input_file}.enc")
        print(f"Evaluaciones guardadas en: {eval_file}")
    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {e}")
    except PermissionError as e:
        print(f"Error de permisos: {e}")
    except ValueError as e:
        print(f"Valor inválido: {e}")
    except Exception as e:
        print(f"Ocurrió un error durante la encriptación: {e}")

def decrypt_file(eval_file, encrypted_file):
    """
    Desencripta un archivo usando evaluaciones polinomiales del Esquema de Compartición de Secretos de Shamir.

    Args:
        eval_file (str): Archivo con al menos t de las n evaluaciones del polinomio.
        encrypted_file (str): Archivo con el documento encriptado.
    """
    try:
        shares = read_text_file(eval_file)
        password = reconstruct_secret(shares)
        encrypted_content = read_binary_file(encrypted_file)
        decrypted_content = decrypt(encrypted_content, password)
        output_file = encrypted_file.replace(".enc", "")
        write_text_file(output_file, decrypted_content)
        print(f"Archivo desencriptado y guardado en: {output_file}")
    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {e}")
    except PermissionError as e:
        print(f"Error de permisos: {e}")
    except ValueError as e:
        print(f"Valor inválido: {e}")
    except Exception as e:
        print(f"Ocurrió un error durante la desencriptación: {e}")

if __name__ == "__main__":
    main()