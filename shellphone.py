from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

from parser import PlayerParser
from display import Display

from io import BytesIO

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

if __name__ == "__main__":
    display = Display()
    while True:
        selected_file = display.render_select_player()
        decrypted_data = decrypt_file(selected_file)

        parser = PlayerParser(decrypted_data)
        deserialized = parser.deserialize()

        save = display.render(deserialized)

        if save:
            serilalized = parser.serialize(deserialized)

            encrypted_file = encrypt_file(selected_file,serilalized)

    


