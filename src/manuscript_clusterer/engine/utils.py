"""Utilities for the computation of the silhouettes.
"""
import re


def expand_nomina_sacra(text):
    """Expand the nominal sacra in the text.
    """
    # Dictionary mapping nomina sacra to their expanded forms
    nomina_sacra_dict = {
        # Nominative forms
        'θς': 'θεος', 'κς': 'κυριος', 'ἰης': 'ιησους', 'δαυ': 'δαυιδ', 'ις': 'ιησους',
        'πνα': 'πνευμα', 'ισρλ': 'ισραηλ', 'χσ': 'χριστος', 'ισαακ': 'ισαακ','ισλ': 'ισραηλ','ἰσ': 'ιησους',
        "ιηλ": "ισραηλ",
        # Genitive forms
        'θυ': 'θεου', 'κυ': 'κυριου', 'ἰησ': 'ιησου', 'δαυ': 'δαυιδ',
        'πνυ': 'πνευματος', 'ισρλ': 'ισραηλ', 'χυ': 'χριστου', 'ισαακ': 'ισαακ', 'ουνου': 'ουρανου',
        'ιυ': 'ιησου',  # Additional form for Jesus
        # Accusative forms
        'θν': 'θεον', 'κν': 'κυριον', 'ἰησ': 'ιησους', 'δαυ': 'δαυιδ',
        'πνα': 'πνευμα', 'ισρλ': 'ισραηλ', 'χν': 'χριστον', 'ισαακ': 'ισαακ',
        # Dative forms
        'θω': 'θεω', 'κω': 'κυριω', 'ἰης': 'ιησου', 'δαυ': 'δαυιδ',
        'πνα': 'πνευματι', 'ισρλ': 'ισραηλ', 'χω': 'χριστω', 'ισαακ': 'ισαακ', 'ανων': 'ανδροπον',
        'ιυ': 'ιησου',  # Additional form for Jesus
        # Vocative forms
        'κε': 'κυριε'
    }

    # Regular expression pattern to match nomina sacra
    pattern = r'\b(' + '|'.join(re.escape(ns)
                                for ns in nomina_sacra_dict.keys()) + r')\b'

    # Function to replace nomina sacra with their expanded forms
    def replace_nomina_sacra(match):
        return nomina_sacra_dict[match.group(0)]

    # Perform the replacement
    return re.sub(pattern, replace_nomina_sacra, text)