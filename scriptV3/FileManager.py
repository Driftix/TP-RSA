import os

class FileManager():

    def save_key(self, filename, fileType, key):
        if fileType == "public key":
            file = filename + ".pub"
        elif fileType == "private key":
            file = filename + ".priv"
        else:
            raise SystemExit("FileType invalid")

        with open(file,'w') as f:
            f.write(f'---begin {filename} {fileType}---\n')
            f.write(key + '\n')
            f.write(f'---end {filename} key---\n')

    def load_key(self, filename, fileType):
        if fileType == "public key":
            file = filename + ".pub"
        elif fileType == "private key":
            file = filename + ".priv"
        else:
            raise SystemExit("FileType invalid")

        with open(file ,'r') as f:
            line = f.readlines()
            verification_line = line[0]
            if verification_line  == f'---begin {filename} {fileType}---\n':
                return line[1].strip()
            else:
                raise SystemExit("Format de fichier non valide")
            
    def readText(self, path):
        try : 
            f = open(path, 'r')
            text = f.read()
            f.close()
            return text
        except Exception:
            raise SystemExit("Path en entrée invalide")

    def writeText(self, path, text):
        try :
            f = open(path,'w')
            f.write(text)
            f.close()
        except Exception:
            raise SystemExit("Path en entrée invalide")



