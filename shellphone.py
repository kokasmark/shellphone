from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

from parser import PlayerParser
from display import Display

from io import BytesIO
import os
def decrypt_file(path, encryption_key="h3y_gUyZ"):
    with open(path, "rb") as f:
        encrypted_data = f.read()

    key = encryption_key.encode("utf-16le")

    if len(key) != 16:
        raise ValueError("Key must be 16 bytes long after UTF-16 encoding.")

    cipher = AES.new(key, AES.MODE_CBC, iv=key)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

def encrypt_file(path, data,encryption_key="h3y_gUyZ"):

    key = encryption_key.encode("utf-16le")

    if len(key) != 16:
        raise ValueError("Key must be 16 bytes long after UTF-16 encoding.")

    cipher = AES.new(key, AES.MODE_CBC, iv=key)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))

    with open(path,"wb") as f:
        f.write(encrypted_data)

def find_player_files():
    """Searches for .plr files in the user's Terraria player directory."""
    documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
    terraria_player_folder = os.path.join(documents_folder, "My Games", "Terraria", "Players")
    tmodloader_player_folder = os.path.join(documents_folder, "My Games", "Terraria", "tModLoader", "Players")
    if not os.path.exists(terraria_player_folder):
        print("Terraria player folder not found!")
        return []

    return [os.path.join(terraria_player_folder, f) for f in os.listdir(terraria_player_folder) if f.endswith(".plr")] + [
            os.path.join(tmodloader_player_folder, f) for f in os.listdir(tmodloader_player_folder) if f.endswith(".plr")
        ]

def render_select_player(display):
    player_files = find_player_files()
    if not player_files:
        print("No .plr files found!")
        return None

    parsers = []
    for file in player_files:
        decrypted_data = decrypt_file(file)
        parser = PlayerParser(decrypted_data,file)
        parser.deserialize()
        parsers.append(parser)

    return display.render_player_select(player_files, parsers)

if __name__ == "__main__":
    display = Display()
    while True:
        parser,selected_file = render_select_player(display)

        save = display.render(parser.deserialized)

        if save:
            serilalized = parser.serialize(parser.deserialized)

            encrypted_file = encrypt_file(selected_file,serilalized)

        


    


