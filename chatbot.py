#!/usr/bin/env python
# coding: utf-8
# LTAT.01.003 Tehisintellekt (2023 kevad)
# Kodutöö nr 7. Tehisintellekti rakendamine
import re

import estnltk

filters = ["prill", "päikeseprill", "kübar", "kiiver", "nokamüts", "mask", "vunts", "deemon", "süda", "koer", "kloun", "pikachu", "karu"]
head_filters = ["kübar", "kiiver", "nokamüts", "süda", "deemon"]
eye_filters = ["prill", "päikeseprill"]
face_filters = ["mask", "vunts", "koer", "kloun", "pikachu", "karu"]


def get_filters():
    return filters


def get_head_filters():
    return head_filters


def get_eye_filters():
    return eye_filters


def get_face_filters():
    return face_filters


def morph_filters():
    return ", ".join(estnltk.vabamorf.morf.synthesize(word, 'sg g')[0].strip() for word in filters[:len(filters) - 1]) \
        + f" ja {estnltk.vabamorf.morf.synthesize(filters[-1], 'sg g')[0].strip()}"


def get_command(analysis, given_filters):
    for lemma in analysis.words.lemma:
        for word in lemma:
            if word in given_filters:
                return word

    return None


def get_intro():
    return "Tere, millist filtrit te soovite?"


def get_response(text, command):
    response = "Vabandust, ei saanud aru. Palun öelge uuesti."
    if text != "":
        regex = "lõpetama|aitama|eemaldama|võtma|kustutama|filter|valima|" + "|".join(filters)

        analysis = estnltk.Text(text).tag_layer()

        if any(any(re.search(regex, word) for word in lemma) for lemma in analysis.words.lemma):
            if any(any(re.search("lõpetama", word) for word in lemma) for lemma in analysis.words.lemma):
                command = "exit"
                response = "Nägemist!"

            elif any(any(re.search("eemaldama|kustutama", word) for word in lemma) for lemma in analysis.words.lemma):
                command = ""
                response = "Eemaldasin Teilt filtri. Millist filtrit nüüd soovite?"

            elif any(any(word in head_filters for word in lemma) for lemma in analysis.words.lemma):
                command = get_command(analysis, head_filters)
                response = f"Panen Teie pea peale {estnltk.vabamorf.morf.synthesize(command, 'sg g')[0].strip()} filtri. " \
                           f"Millist filtrit nüüd soovite?"

            elif any(any(word in eye_filters for word in lemma) for lemma in analysis.words.lemma):
                command = get_command(analysis, eye_filters)
                response = f"Selge, panen Teie silmadele {estnltk.vabamorf.morf.synthesize(command, 'sg g')[0].strip()} filtri. " \
                           f"Millist filtrit nüüd soovite?"

            elif any(any(word in face_filters for word in lemma) for lemma in analysis.words.lemma):
                command = get_command(analysis, face_filters)
                response = f"Teie näole tekib nüüd {estnltk.vabamorf.morf.synthesize(command, 'sg g')[0].strip()} filter. " \
                           f"Millist filtrit nüüd soovite?"

            elif any(any(re.search("aitama|filter|valima", word) for word in lemma) for lemma in analysis.words.lemma):
                response = f"Te saate kasutada {morph_filters()} filtreid."

    return command, response
