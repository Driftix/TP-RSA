# TP-RSA Guilhem Schira

## Dépendences :
Sympy est utilisée pour la simplification de la génération de nombre premiers (j'utilise seulement isprime)
```
pypy3 -m pip install sympy
```

## Documentation :

```usage: script.py [-h] [-f FICHIER] [-s SIZE] [-i INPUT] [-o OUTPUT] {keygen,crypt,decrypt,help} [cle] [texte]

Script monRSA par Guilhem Schira

positional arguments:
  {keygen,crypt,decrypt,help}
                        Commande à exécuter
  cle                   Fichier contenant la clé publique ("crypt") ou privée ("decrypt"). Clé par défaut: default_key
  texte                 Phrase à chiffrer ("crypt") ou déchiffrer ("decrypt")

options:
  -h, --help            show this help message and exit
  -f FICHIER, --fichier FICHIER
                        Noms des fichiers de clé générés (par défaut: monRSA.pub monRSA.priv)
  -s SIZE, --size SIZE  Tailles des clé générées (par défaut: 10)
  -i INPUT, --input INPUT
                        Accepte un fichier texte à la place d'une chaine (path)
  -o OUTPUT, --output OUTPUT
                        Sauvegarde le resultat de cryptage ou decryptage dans un fichier nommé (path)
```

## Exemples :
*Dans un cas où vous utilisez une archi arch (comme la mienne) vous devrez utiliser pypy3 sinon il sera remplacé par python3*

### Documentation :
Affichage de la documentation
```console
pypy3 script.py --help
```

### Génération de clés RSA :
Crée une clé publique et une clé privée avec un nom "nomfichier" et une taille "taille" définie
```console
pypy3 script.py keygen -f nomfichier -s taille
```
## Crypt et Decrypt
*DANS CETTE VERSION IL N'Y A PLUS BESOIN DE SPECIFIER L'EXTENTION DES CLÉ (.pub,.priv)*
### Crypt :
Chiffre un en entrée texte à partir d'une clée publique en entrée puis affiche le résultat en ligne de commande
```console
pypy3 script.py crypt nomcle "texte à chiffrer"
```
### Decrypt :
Déchiffre le texte donné en entré en utilisant la clé privée
```console
pypy3 script.py decript nomcle "resultat du texte chiffré"
```
### Paramètres supplémentaires:
```console
pypy3 script.py crypt/decrypt nomcle -i ./pathtotext.txt -o ./outputpath.txt
```