#!/usr/bin/env python
# coding: utf-8
# LTAT.01.003 Tehisintellekt (2023 kevad)
# Kodutöö nr 7. Tehisintellekti rakendamine
import re

import estnltk

filters = ["prill", "päikeseprill", "kübar", "kiiver", "nokamüts", "mask", "vunts"]
head_filters = ["kübar", "kiiver", "nokamüts"]
eye_filters = ["prill", "päikeseprill"]
face_filters = ["mask", "vunts"]


def get_filters():
    return filters


def get_command(analysis, filters):
    for lemma in analysis.words.lemma:
        for word in lemma:
            if word in filters:
                return word

    return None


def get_response(input):
    command = ""
    response = "Vabandust, ei saanud aru. Palun öelge uuesti."
    if input == "_____":
        return "", "Tere, millist filtrit te soovite? "

    regex = "lõpetama|aitama|" + "|".join(filters)

    analysis = estnltk.Text(input).tag_layer()

    if any(any(re.search(regex, word) for word in lemma) for lemma in analysis.words.lemma):
        if any(any(re.search("lõpetama|aitama", word) for word in lemma) for lemma in analysis.words.lemma):
            command = "exit"
            response = "Nägemist!"

        if any(any(word in head_filters for word in lemma) for lemma in analysis.words.lemma):
            command = get_command(analysis, head_filters)
            response = f"Selge, panen Teie pea peale {estnltk.vabamorf.morf.synthesize(command, 'sg g')[0].strip()} filtri. " \
                       f"Millist filtrit nüüd soovite?"

        if any(any(word in eye_filters for word in lemma) for lemma in analysis.words.lemma):
            command = get_command(analysis, eye_filters)
            response = f"Selge, panen Teie silmadele {estnltk.vabamorf.morf.synthesize(command, 'sg g')[0].strip()} filtri. " \
                       f"Millist filtrit nüüd soovite?"

        if any(any(word in face_filters for word in lemma) for lemma in analysis.words.lemma):
            command = get_command(analysis, face_filters)
            response = f"Selge, panen Teie näole {estnltk.vabamorf.morf.synthesize(command, 'sg g')[0].strip()} filtri. " \
                       f"Millist filtrit nüüd soovite?"

    return command, response
