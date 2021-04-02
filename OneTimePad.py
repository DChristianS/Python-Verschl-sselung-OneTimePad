# OneTimePad Verschlüsselung

import os

def encrypt(filename):
    to_encrypt = open(filename, "rb").read()            # Datei einlesen
    size = len(to_encrypt)                              # Größen bestimmen
    key = os.urandom(size)                              # Key erzeugen
    with open (filename + ".key", "wb") as key_out:     # Key speichern
        key_out.write(key)                              
    encrypted = bytes(a ^ b for (a, b) in zip(to_encrypt, key) )    # verschlüsseln
    with open("locked_" + filename, "wb") as encrypted_out:     # Datei speichern
        encrypted_out.write(encrypted)

def decrypt(filename, key):
    file = open("locked_" + filename, "rb").read()
    key = open(key + ".key", "rb").read()
    decrypted = bytes(a ^ b for (a, b) in zip(file, key) )    # entschlüsseln
    with open("unlocked_" + filename, "wb") as decrypted_out:     # Datei speichern
        decrypted_out.write(decrypted)

import qrcode
def createSample(filename):
    qr = qrcode.QRCode()
    qr.add_data("Dies ist ein Test!")
    img = qr.make_image(fill_color="blue", back_color="yellow").save(filename)

def delete_files(filename):
    input("Press Enter to Delete Files")
    if os.path.isfile(filename):
        os.remove(filename)
    if os.path.isfile("locked_" + filename):
        os.remove("locked_" + filename)
    if os.path.isfile(filename + ".key"):
        os.remove(filename + ".key")
    if os.path.isfile("unlocked_" + filename):
        os.remove("unlocked_" + filename)
    

filename = "Test.png"
createSample(filename)
encrypt(filename)
decrypt(filename, filename)
delete_files(filename)


