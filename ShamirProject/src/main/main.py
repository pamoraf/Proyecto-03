import argparse
import getpass
from shamir_scheme import generate_shares
from cipher import encrypt, decrypt
from io_manager import (
    read_binary_file,
    read_text_file,
    write_binary_file,
    write_text_file,
    format_evaluations,
    get_evaluations
)

def main():
    parser = argparse.ArgumentParser(description="Shamir's Secret Sharing Scheme")
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    # Sub-parser for the encrypt command
    encrypt_parser = subparsers.add_parser('c', help='Encrypt a file')
    encrypt_parser.add_argument('eval_file', type=str, help='File to save the polynomial evaluations')
    encrypt_parser.add_argument('n', type=int, help='Total number of evaluations (n > 2)')
    encrypt_parser.add_argument('t', type=int, help='Minimum number of points needed to decrypt (1 < t ≤ n)')
    encrypt_parser.add_argument('input_file', type=str, help='File with the clear document')

    # Sub-parser for the decrypt command
    decrypt_parser = subparsers.add_parser('d', help='Decrypt a file')
    decrypt_parser.add_argument('eval_file', type=str, help='File with at least t of the n polynomial evaluations')
    decrypt_parser.add_argument('encrypted_file', type=str, help='File with the encrypted document')

    args = parser.parse_args()

    if args.command == 'c':
        encrypt_file(args.eval_file, args.n, args.t, args.input_file)
    elif args.command == 'd':
        decrypt_file(args.eval_file, args.encrypted_file)
    else:
        parser.print_help()

def encrypt_file(eval_file, n, t, input_file):
    if n <= 2 or t <= 1 or t > n:
        print("Invalid values for n and t. Ensure that n > 2 and 1 < t ≤ n.")
        return

    password = getpass.getpass("Enter password: ")
    text = read_text_file(input_file)
    encrypted_content = encrypt(text, password)
    write_binary_file(input_file + ".enc", encrypted_content)

    secret = int.from_bytes(encrypted_content, 'big')
    shares = generate_shares(secret, n, t)
    formatted_shares = format_evaluations(shares)
    write_text_file(eval_file, formatted_shares)
    print(f"File encrypted and saved as {input_file}.enc")
    print(f"Polynomial evaluations saved in {eval_file}")

def decrypt_file(eval_file, encrypted_file):
    password = getpass.getpass("Enter password: ")
    shares = get_evaluations(read_text_file(eval_file))
    secret = interpolate(shares, len(shares))
    encrypted_content = secret.to_bytes((secret.bit_length() + 7) // 8, 'big')
    decrypted_content = decrypt(encrypted_content, password)
    output_file = encrypted_file.replace(".enc", "")
    write_text_file(output_file, decrypted_content)
    print(f"File decrypted and saved as {output_file}")

if __name__ == "__main__":
    main()