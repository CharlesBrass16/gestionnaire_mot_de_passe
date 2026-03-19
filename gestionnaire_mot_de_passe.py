import json
import os
from argparse import ArgumentParser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64

# fichier JSON avec les infos
FILENAME = "trousse.json"

#  Clé AES de 16 octets (AES-128)
KEY_LENGTH = 16

# Plusieurs itérations de dérivations de clé pour augmenter la sécurité
PBKDF2_ITERATIONS = 100_000


# Charge les données du fichier JSON de la trousse
def load_data():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as file:
        return json.load(file)


# Sauvegarde les données passées en paramètre dans le fichier trousse.json, ou le crée au besoin
def save_data(data):
    with open(FILENAME, "w") as file:
        json.dump(data, file)


# Génère une clé cryptographique de 16 octets basée sur un mot de passe et un salt de 16 octets
def derive_key(password: str, salt: bytes) -> bytes:
    key = PBKDF2(password, salt, dkLen=KEY_LENGTH, count=PBKDF2_ITERATIONS)
    return key


# Encrypte des données passées en paramètre avec AES CBC et la clé passé en paramètre
def encrypt_field(data: str, key: bytes) -> (bytes, bytes):
    # Création de l'objet AES utilisé pour l'encryption
    cipher = AES.new(key, AES.MODE_CBC)
    # instancie l'IV lié à l'objet AES créé
    iv = cipher.iv
    # Instancie le texte chiffré
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
    return iv, ciphertext


# Décrypte les informations stockées basées sur l'IV du champ, le champ chiffré et la clé
def decrypt_field(iv: bytes, ciphertext: bytes, key: bytes) -> str:
    try:
        # Création de l'objet AES utilisé pour la decryption
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # Décrypte le champ en texte clair en utilisant la méthode "decrypt" de l'instance cipher, en s'assurant de
        # retirer le padding s'il y en a
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
        return plaintext
    except Exception as e:
        print(f"Error during decryption: {e}")
        return "*****"


def add_entry(password, url, user, pwd):
    # Génération du sel
    salt = get_random_bytes(16)
    # Dérivation de la clé
    key = derive_key(password, salt)

    # Chiffrement des champs d'URL de service
    iv_url, enc_url = encrypt_field(url, key)

    # Chiffrement des champs de nom d'utilisateur du compte
    iv_user, enc_user = encrypt_field(user, key)

    # Chiffrement des champs de mot de passe du compte
    iv_pwd, enc_pwd = encrypt_field(pwd, key)

    # Récupère les entrées deja dans le fichier JSON
    data = load_data()
    # Sauvegarde dans le fichier JSON
    data.append({
        "salt": base64.b64encode(salt).decode(),
        "url": base64.b64encode(enc_url).decode(),
        "iv_url": base64.b64encode(iv_url).decode(),
        "user": base64.b64encode(enc_user).decode(),
        "iv_user": base64.b64encode(iv_user).decode(),
        "pwd": base64.b64encode(enc_pwd).decode(),
        "iv_pwd": base64.b64encode(iv_pwd).decode(),
    })

    # sauvegarde nouvelle entry
    save_data(data)
    print("Entry successfully added.")


#  Liste les différentes entrées enregistrées dans le fichier trousse.json
def list_entries(password):
    # Récupère les données présentes
    data = load_data()
    for i, entry in enumerate(data, 1):
        try:
            # Affiche uniquement l'URL de l'entrée en gardant secret les nom utilisateurs et mot de passe
            key = derive_key(password, base64.b64decode(entry["salt"]))
            url = decrypt_field(base64.b64decode(entry["iv_url"]), base64.b64decode(entry["url"]), key)
        except:
            url = "*****"
        print(f"{i} {url} ***** *****")


def display_entry(password, index, show_user_param, show_pwd_param):
    # Récupère les données dans le fichier JSON
    data = load_data()

    # Valide un index présent
    if index < 1 or index > len(data):
        print("Invalid entry number.")
        return

    # Sélectionne l'entry lié à l'index
    entry = data[index - 1]

    # Récupération de l'URL
    salt = base64.b64decode(entry["salt"])
    key = derive_key(password, salt)
    url = decrypt_field(base64.b64decode(entry["iv_url"]), base64.b64decode(entry["url"]), key)

    # Si paramètre de commande n'autorise pas l'affichage du user
    if not show_user_param:
        user = "*****"
    # Si paramètre de commande autorise l'affichage du user
    else:
        # Déchiffre user
        iv_user = base64.b64decode(entry["iv_user"])
        encrypted_user = base64.b64decode(entry["user"])
        user = decrypt_field(iv_user, encrypted_user, key)

    # Si paramètre de commande n'autorise pas l'affichage du mot de passe
    if not show_pwd_param:
        pwd = "*****"
    # Si paramètre de commande autorise l'affichage du mot de passe
    else:
        # Déchiffre le mot de passe
        iv_pwd = base64.b64decode(entry["iv_pwd"])
        encrypted_pwd = base64.b64decode(entry["pwd"])
        pwd = decrypt_field(iv_pwd,encrypted_pwd,key)

    print(f"{index} {url} {user} {pwd}")



def main():
    parser = ArgumentParser(description="Password Manager")

    # Ajouter un enregistrement
    parser.add_argument("-a", action="store_true", help="Add a new entry")
    parser.add_argument("-url", type=str, help="URL of the service")
    parser.add_argument("-user", type=str, help="Username for the service")
    parser.add_argument("-pwd", type=str, help="Password for the service")
    parser.add_argument("MASTER_PWD", nargs="?", type=str, help="Master password")

    # Lister les enregistrements
    parser.add_argument("-l", type=str, metavar="MASTER_PWD", help="List all entries")

    # Afficher une entrée
    parser.add_argument("-d", action="store_true", help="Display a specific entry")
    parser.add_argument("-i", type=int, help="Index of the entry")
    # Afficher les infos du user ou du password optionnellement si elles sont présentes dans la commande
    parser.add_argument("--user", action="store_true", help="Decrypt and display the username")
    parser.add_argument("--pwd", action="store_true", help="Decrypt and display the password")

    args = parser.parse_args()
    print(args)

    # Si paramètre de commande "-a" est présent avec tous les paramètres nécessaires, ajoute l'entrée
    if args.a:
        if not all([args.MASTER_PWD, args.url, args.user, args.pwd]):
            print("Missing required fields for adding an entry: -url, -user, -pwd")
            return
        add_entry(args.MASTER_PWD, args.url, args.user, args.pwd)
    # Si paramètre de commande "-l" est présent, liste les entrées en cachant les informations du user et du mot de passe
    elif args.l:
        list_entries(args.l)

    # Si paramètre de commande "-d" avec le bon mot de passe et un index valide,
    # déchiffre les champs de user et ou du mot de passe dépendamment des options de la commande
    elif args.d:
        if args.i is None:
            print("Please specify the entry index with -i.")
            return
        if args.l:
            password = args.l
        else:
            password = args.MASTER_PWD
        # Affiche l'entrée avec les paramètres désirés
        display_entry(password, args.i, args.user, args.pwd)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()