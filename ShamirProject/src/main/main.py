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

def has_valid_extension(file_path, valid_extensions):
    """Checks if the file has a valid extension."""
    return any(file_path.endswith(ext) for ext in valid_extensions)

def validate_file_exists(file_path, valid_extensions):
    """Checks if the file exists and has a valid extension."""
    if not has_valid_extension(file_path, valid_extensions):
        raise ValueError(f"The file must have one of the following extensions: {', '.join(valid_extensions)}.")
    try:
        with open(file_path, 'rb'):
            pass
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission error: {file_path}")

def validate_n_t(n, t):
    """Validates the values of n and t."""
    if n <= 2 or t <= 1 or t > n:
        raise ValueError("Invalid values for n and t. Ensure that n > 2 and 1 < t ≤ n.")

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

    try:
        if args.command == 'c':
            validate_file_exists(args.eval_file, ['.frg'])
            validate_file_exists(args.input_file, ['.txt'])
            validate_n_t(args.n, args.t)
            encrypt_file(args.eval_file, args.n, args.t, args.input_file)

        elif args.command == 'd':
            validate_file_exists(args.eval_file, ['.frg'])
            validate_file_exists(args.encrypted_file, ['.aes'])
            decrypt_file(args.eval_file, args.encrypted_file)

        else:
            parser.print_help()

    except ValueError as e:
        print(f"Error: {e}")
    except (FileNotFoundError, PermissionError) as e:
        print(f"File error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def encrypt_file(eval_path, n, t, input_path):
    """
    Encrypts a file and generates polynomial evaluations for Shamir's Secret Sharing Scheme.

    Args:
        eval_file (str): File to save the polynomial evaluations.
        n (int): Total number of evaluations (n > 2).
        t (int): Minimum number of points needed to decrypt (1 < t ≤ n).
        input_file (str): File with the clear document.
    """
    try:
        password = getpass.getpass("Enter password: ")
        text = read_text_file(input_path)
        encrypted_content = encrypt(text, password)
        write_binary_file(input_path.replace(".txt", ".aes"), encrypted_content)
        
        shares = generate_shares(int.from_bytes(get_key(password), 'big'), n, t)
        write_text_file(eval_path, shares)
        
        print(f"File encrypted and saved as: {input_path.replace('.txt', '.aes')}")
        print(f"Evaluations saved in: {eval_path}")
    except ValueError as e:
        print(f"Encryption error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def decrypt_file(eval_path, encrypted_path):
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
    except ValueError as e:
        print(f"Decryption error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
