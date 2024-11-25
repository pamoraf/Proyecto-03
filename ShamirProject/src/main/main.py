import argparse
import getpass
from shamir_scheme import generate_shares, reconstruct_secret
from cipher import encrypt, decrypt, get_key
from io_manager import (
    read_binary_file,
    read_text_file,
    write_binary_file,
    write_text_file
)

def is_valid_file_type(file_path, valid_extensions):
    """Check if the file has a valid extension."""
    return any(file_path.endswith(ext) for ext in valid_extensions)

def main():
    """
    Main function to handle command-line arguments and execute the appropriate
    encryption or decryption function based on the provided command.
    """
    parser = argparse.ArgumentParser(description="Shamir's Secret Sharing Scheme")
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')
    encrypt_parser = subparsers.add_parser('c', help='Encrypt a file')
    encrypt_parser.add_argument('eval_file', type=str, help='Path to save the polynomial evaluations (.frg)')
    encrypt_parser.add_argument('n', type=int, help='Total number of evaluations (n > 2)')
    encrypt_parser.add_argument('t', type=int, help='Minimum number of points needed to decrypt (1 < t ≤ n)')
    encrypt_parser.add_argument('input_file', type=str, help='File with the clear document (.txt)')
    decrypt_parser = subparsers.add_parser('d', help='Decrypt a file')
    decrypt_parser.add_argument('eval_file', type=str, help='File with at least t of the n polynomial evaluations (.frg)')
    decrypt_parser.add_argument('encrypted_file', type=str, help='File with the encrypted document (.aes)')
    args = parser.parse_args()
    if args.command == 'c':
        if not is_valid_file_type(args.eval_file, ['.frg']):
            raise ValueError("The evaluation file must have a .frg extension.")
        if not is_valid_file_type(args.input_file, ['.txt']):
            raise ValueError("The input file must have a .txt extension.")
        encrypt_file(args.eval_file, args.n, args.t, args.input_file)
    elif args.command == 'd':
        if not is_valid_file_type(args.eval_file, ['.frg']):
            raise ValueError("The evaluation file must have a .frg extension.")
        if not is_valid_file_type(args.encrypted_file, ['.aes']):
            raise ValueError("The encrypted file must have a .aes extension.")
        decrypt_file(args.eval_file, args.encrypted_file)
    else:
        parser.print_help()

def encrypt_file(eval_path : str, n : int, t : int, input_path : str):
    """
    Encrypts a file and generates polynomial evaluations for Shamir's Secret Sharing Scheme.

    Args:
        eval_file (str): File to save the polynomial evaluations.
        n (int): Total number of evaluations (n > 2).
        t (int): Minimum number of points needed to decrypt (1 < t ≤ n).
        input_file (str): File with the clear document.
    """
    try:
        if n <= 2 or t <= 1 or t > n:
            print("Invalid values for n and t. Ensure that n > 2 and 1 < t ≤ n.")
            return
        password = getpass.getpass("Enter password: ")
        text = read_text_file(input_path)
        encrypted_content = encrypt(text, password)
        write_binary_file(input_path.replace(".txt", ".aes"), encrypted_content)
        shares = generate_shares(int.from_bytes(get_key(password), 'big'), n, t)
        write_text_file(eval_path, shares)
        print(f"File encrypted and saved as: {input_path.replace(".txt", ".aes")}")
        print(f"Evaluations saved in: {eval_path}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except ValueError as e:
        print(f"Invalid value: {e}")

def decrypt_file(eval_path : str, encrypted_path : str):
    """
    Decrypts a file using polynomial evaluations from Shamir's Secret Sharing Scheme.

    Args:
        eval_file (str): File with at least t of the n polynomial evaluations.
        encrypted_file (str): File with the encrypted document.
    """
    try:
        shares = read_text_file(eval_path)
        k = reconstruct_secret(shares)
        encrypted_content = read_binary_file(encrypted_path)
        decrypted_content = decrypt(encrypted_content, k.to_bytes((k.bit_length() + 7) // 8, 'big'))
        output_file = encrypted_path.replace(".aes", "_revealed.txt")
        write_text_file(output_file, decrypted_content)
        print(f"File decrypted and saved as: {output_file}")    
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except ValueError as e:
        print(f"Invalid value: {e}")

if __name__ == "__main__":
    main()