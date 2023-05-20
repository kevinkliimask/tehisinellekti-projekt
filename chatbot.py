#!/usr/bin/env python
# coding: utf-8
# LTAT.01.003 Tehisintellekt (2023 kevad)
# Kodutöö nr 7. Tehisintellekti rakendamine
import re

import estnltk

filters = ["prill", "päikeseprill", "kübar"]
head_filters = ["kübar"]
eye_filters = ["prill", "päikeseprill"]


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
            response = f"Selge, paneme Teie pea peale {estnltk.vabamorf.morf.synthesize(command, 'sg g')[0].strip()} filtri. "

        if any(any(word in eye_filters for word in lemma) for lemma in analysis.words.lemma):
            command = get_command(analysis, eye_filters)
            response = f"Panen Te silmadele {estnltk.vabamorf.morf.synthesize(command, 'sg g')[0].strip()} filtri. "

    return command, response
