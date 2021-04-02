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

import qrcode # Beispieldaten erzeugen
def create_sample(filename):
    qr = qrcode.QRCode()
    qr.add_data("Dies ist ein Test!")
    img = qr.make_image(fill_color="blue", back_color="yellow").save(filename)
import qrcode.image.svg
def create_sample_svg(filename):
    img = qrcode.make("Dies ist ein Test", image_factory = qrcode.image.svg.SvgPathImage)
    img.save(filename)

def delete_files(filename):
#    input("Press Enter to Delete Files")
    if os.path.isfile(filename):
        os.remove(filename)
    if os.path.isfile("locked_" + filename):
        os.remove("locked_" + filename)
    if os.path.isfile(filename + ".key"):
        os.remove(filename + ".key")
    if os.path.isfile("unlocked_" + filename):
        os.remove("unlocked_" + filename)
    

filename = "Test.png"
create_sample(filename)
encrypt(filename)
input("Datei verschlüsselt")
decrypt(filename, filename)
input("Entschlüsselt")
delete_files(filename)


# Mit dem Schlüssel aus Datei A die Datei B erzeugen


def equalize(path_1, path_2):
    dat1 = open(path_1, "rb").read()    
    dat2 = open(path_2, "rb").read()
    l_dat1 = len(dat1)    
    l_dat2 = len(dat2)
    if l_dat1 > l_dat2:
        dat2 += os.urandom(l_dat1 - l_dat2)
    else:
        dat1 += os.urandom(l_dat2 - l_dat1)
    with open(path_1, "wb") as out:
        out.write(dat1)
    with open(path_2, "wb") as out:
        out.write(dat2)

def keygen2F(orig_path, enc_path, key_path):
    equalize(orig_path, enc_path)
    orignal = open(orig_path, "rb").read()
    encrypted = open(enc_path, "rb").read()
    key = bytes(a ^ b for (a, b) in zip(orignal, encrypted))    # Schlüssel erzeugen
    with open(key_path + "enc.key", "wb") as key_out:     # Datei speichern
        key_out.write(key)
    os.remove(orig_path)

def decrypt2F(enc_path, key_path, dec_path):
    key = open(key_path + "enc.key", "rb").read()
    encrypted = open(enc_path, "rb").read()
    decrypted = bytes(a ^ b for (a, b) in zip(key, encrypted))    # Schlüssel erzeugen
    with open("dec_" + dec_path, "wb") as decrypt_out:     # Datei speichern
        decrypt_out.write(decrypted)
    os.remove(key_path + "enc.key")
    os.remove(enc_path)


filename = "Tes.png"
create_sample(filename)
filename_svg = "Test.svg"
create_sample_svg(filename_svg)
input("Beispieldateien erzeugt")
keygen2F(filename, filename_svg, "")
input("Schüsseldatei erzeugt + png gelöscht")
decrypt2F(filename_svg,"", filename)
input("Png über den Schlüssel wieder erstellt -> Press Enter to Delete dec_Tes.png")
os.remove("dec_" + filename)


