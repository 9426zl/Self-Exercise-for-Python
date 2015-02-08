import os, random, struct
from Crypto.Cipher import AES


class Application(object):
    def decrypt_file(self):
        "define the decrypt function"
        key = "12345678asdfghjk"
        in_filename = "InfoSaved.enc.txt"
        out_filename = "InfoSaved.txt"
        chunksize = 64*1024

        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)



app = Application()
app.decrypt_file()

