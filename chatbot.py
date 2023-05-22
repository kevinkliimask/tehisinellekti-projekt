#!/usr/bin/env python
# coding: utf-8
# LTAT.01.003 Tehisintellekt (2023 kevad)
# Kodutöö nr 7. Tehisintellekti rakendamine

# Moodulite importimine
import re
import estnltk

# Defineerime erinevad filtrid ja jagame need tüüpide põhjal listidesse
filters = ["prill", "päikeseprill", "kübar", "kiiver", "nokamüts", "mask", "vunts", "deemon", "süda", "koer", "kloun", "pikachu", "karu"]
head_filters = ["kübar", "kiiver", "nokamüts", "süda", "deemon"]
eye_filters = ["prill", "päikeseprill"]
face_filters = ["mask", "vunts", "koer", "kloun", "pikachu", "karu"]

# Funktsioon tagastab kõik saadaolevad filtrid
def get_filters():
    return filters

# Funktsioon tagastab filtrid, mida saab kasutada pea peal
def get_head_filters():
    return head_filters

# Funktsioon tagastab filtrid, mida saab kasutada silmade peal
def get_eye_filters():
    return eye_filters

# Funktsioon tagastab filtrid, mida saab kasutada näo peal
def get_face_filters():
    return face_filters

# Funktsioon tagastab kõik filtrid morfoloogiliselt õiges vormis
def morph_filters():
    return ", ".join(estnltk.vabamorf.morf.synthesize(word, 'sg g')[0].strip() for word in filters[:len(filters) - 1]) \
        + f" ja {estnltk.vabamorf.morf.synthesize(filters[-1], 'sg g')[0].strip()}"

# Funktsioon kontrollib, kas kasutaja sisestas mõne filtri nime ja tagastab selle
def get_command(analysis, given_filters):
    for lemma in analysis.words.lemma:
        for word in lemma:
            if word in given_filters:
                return word

    return None

# Funktsioon tagastab algse tervitusteksti
def get_intro():
    return "Tere, millist filtrit te soovite?"

# Põhifunktsioon, mis genereerib vastuse kasutaja sisestatud teksti põhjal
def get_response(text, command):

    # Esialgne vastus - eeldame, et tehisintellekt ei saa kasutaja soovist aru.
    response = "Vabandust, ei saanud aru. Palun öelge uuesti."
    if text != "":
        # Koostame regulaaravaldise kõigi võimalike käskudega
        regex = "lõpetama|aitama|eemaldama|võtma|kustutama|filter|valima|" + "|".join(filters)

        # Analüüsime kasutaja sisendit
        analysis = estnltk.Text(text).tag_layer()

        # Kontrollime kasutaja sisendis mitmeid võimalikke käsklusi
        if any(any(re.search(regex, word) for word in lemma) for lemma in analysis.words.lemma):
            # Kasutaja soovib lõpetada
            if any(any(re.search("lõpetama", word) for word in lemma) for lemma in analysis.words.lemma):
                command = "exit"
                response = "Nägemist!"

            # Kasutaja soovib eemaldada filtri
            elif any(any(re.search("eemaldama|kustutama", word) for word in lemma) for lemma in analysis.words.lemma):
                command = ""
                response = "Eemaldasin Teilt filtri. Millist filtrit nüüd soovite?"

            # Kasutaja soovib peale panna pea filtri
            elif any(any(word in head_filters for word in lemma) for lemma in analysis.words.lemma):
                command = get_command(analysis, head_filters)
                response = f"Panen Teie pea peale {estnltk.vabamorf.morf.synthesize(command, 'sg g')[0].strip()} filtri. " \
                           f"Millist filtrit nüüd soovite?"
                
            # Kasutaja soovib peale panna silma filtri
            elif any(any(word in eye_filters for word in lemma) for lemma in analysis.words.lemma):
                command = get_command(analysis, eye_filters)
                response = f"Selge, panen Teie silmadele {estnltk.vabamorf.morf.synthesize(command, 'sg g')[0].strip()} filtri. " \
                           f"Millist filtrit nüüd soovite?"
                
            # Kasutaja soovib peale panna näo filtri
            elif any(any(word in face_filters for word in lemma) for lemma in analysis.words.lemma):
                command = get_command(analysis, face_filters)
                response = f"Teie näole tekib nüüd {estnltk.vabamorf.morf.synthesize(command, 'sg g')[0].strip()} filter. " \
                           f"Millist filtrit nüüd soovite?"
                
            # Kasutaja soovib kuvada filtrite valikut
            elif any(any(re.search("aitama|filter|valima", word) for word in lemma) for lemma in analysis.words.lemma):
                response = f"Te saate kasutada {morph_filters()} filtreid."

    return command, response
