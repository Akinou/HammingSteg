from PIL import Image
import numpy as np
import random

# La fonction suivante convertit une chaîne de caractères en une liste de bits
def str_to_bits(text):
    return [bin(ord(c))[2:].zfill(8) for c in text]

# La fonction suivante convertit une liste de bits en une chaîne de caractères
def bits_to_str(bits):
    return ''.join([chr(int(b, 2)) for b in bits])

# La fonction suivante cache le texte dans l'image en modifiant les bits de couleur des pixels de manière aléatoire
def hide_text(image_file, text):
    img = Image.open(image_file)
    pixels = img.load()
    width, height = img.size
    bits = str_to_bits(text)
    bit_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if bit_index < len(bits):
                # Modification des bits de couleur des pixels de manière aléatoire
                r = (r & 254) | random.randint(0, 1)
                g = (g & 254) | random.randint(0, 1)
                b = (b & 252) | random.randint(0, 3)
                pixels[x, y] = (r, g, b)
                bit_index += 1
            else:
                break
        if bit_index >= len(bits):
            break
    img.save(image_file)

# La fonction suivante récupère le message caché dans l'image en effectuant une extraction aléatoire
def extract_bits(image_file):
    img = Image.open(image_file)
    pixels = img.load()
    width, height = img.size
    bits = []
    for i in range(len(pixels)):
        # Sélection aléatoire de pixels pour extraire les bits
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        r, g, b = pixels[x, y]
        bits.append(str(r & 1))
        bits.append(str(g & 1))
        bits.append(str(b & 3))
    return bits

# La fonction suivante applique l'algorithme de décodage de Hamming pour corriger les erreurs dans les bits du message caché
def hamming_decode(bits):
    # Table de syndromes pour l'algorithme de décodage de Hamming
    syndromes = {
        '0000': 0,
        '0001': 7,
        '0010': 6,
        '0011': 1,
        '0100': 5,
        '0101': 2,
        '0110': 3,
        '0111': 4,
        '1000': 4,
        '1001': 3,
        '1010': 2,
        '1011': 5,
        '1100': 1,
        '1101': 6,
        '1110': 7,
        '1111': 0
    }
    n = len(bits) // 11
    data_bits = []
    for i in range(n):
        # Extraire les bits de données et de contrôle de parité du bloc
        block = bits[i*11:i*11+11]
        p1 = block[0]
        p2 = block[1]
        d1 = block[2]
        p3 = block[3]
        d2 = block[4]
        d3 = block[5]
        d4 = block[6]
        p4 = block[7]
        d5 = block[8]
        d6 = block[9]
        d7 = block[10]
        # Calculer les syndromes
        s1 = int(p1) ^ int(d1) ^ int(d2) ^ int(d4) ^ int(d5) ^ int(d7)
        s2 = int(p2) ^ int(d1) ^ int(d3) ^ int(d4) ^ int(d6) ^ int(d7)
        s3 = int(p3) ^ int(d2) ^ int(d3) ^ int(d4)
        s4 = int(p4) ^ int(d5) ^ int(d6) ^ int(d7)
        syndrome = str(s4) + str(s3) + str(s2) + str(s1)
        # Corriger les erreurs dans les bits de données
        if syndrome != '0000':
            error_index = syndromes[syndrome] - 1
            block[error_index] = str(1 - int(block[error_index]))
        data_bits += block[2:8]
    return bits_to_str([''.join(data_bits[i:i+8]) for i in range(0, len(data_bits), 8)])

# Exemple d'utilisation : cacher le texte 'Hello World!' dans l'image 'image.png'
hide_text('image.png', 'Hello World!')

# Exemple d'utilisation : extraire le texte caché dans l'image 'image.png' et le décoder avec l'algorithme de décodage de Hamming
bits = extract_bits('image.png')
text = hamming_decode(bits)
print(text)
