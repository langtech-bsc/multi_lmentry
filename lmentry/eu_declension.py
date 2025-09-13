def r_phonotactics(declension_func):
    def inner(word):
        if word.endswith('r'):
            word = word + 'r'
        return declension_func(word)
    return inner


@r_phonotactics
def ergative_undetermined(word: str) -> str:
    # tresna => tresnak, etxe => etxek, arto => artok, hitz => hitzek, negar => negarrek
    if not word.endswith(('a', 'e', 'i', 'o', 'u')):
        word = word + 'e'
    return word + 'k'


@r_phonotactics
def absolutive_singular(word: str) -> str:
    # tresna => tresna, etxe => etxea, arto => artoa, hitz => hitza, negar => negarra
    if not word.endswith('a'):
        word = word + 'a'
    return word


@r_phonotactics
def absolutive_plural(word: str) -> str:
    # tresna => tresnak, etxe => etxeak, arto => artoak, hitz => hitzak, negar => negarrak
    if word.endswith('a'):
        word = word[:-1]
    return word + 'ak'


@r_phonotactics
def comitative_undetermined(word: str) -> str:
    # tresna => tresnarekin, etxe => etxerekin, arto => artorekin, hitz => hitzekin, negar => negarrekin
    if word.endswith(('a', 'e', 'i', 'o', 'u')):
        word = word + 'r'
    return word + 'ekin'


@r_phonotactics
def comitative_singular(word: str) -> str:
    # tresna => tresnarekin, etxe => etxearekin, arto => artoarekin, hitz => hitzarekin, negar => negarrarekin
    if word.endswith('a'):
        word = word[:-1]
    return word + 'arekin'


@r_phonotactics
def comitative_plural(word: str) -> str:
    # tresna => tresnekin, etxe => etxeekin, arto => artoekin, hitz => hitzekin, negar => negarrekin
    if word.endswith('a'):
        word = word[:-1]
    return word + 'ekin'


@r_phonotactics
def instrumental_undetermined(word: str) -> str:
    # tresna => tresnataz, etxe => etxetaz, arto => artoz, hitz => hitzetaz, negar => negarretaz
    if not word.endswith(('a', 'e', 'i', 'o', 'u')):
        word = word + 'e'
    return word + 'taz'


@r_phonotactics
def instrumental_singular(word: str) -> str:
    # tresna => tresnaz, etxe => etxeaz, arto => artoaz, hitz => hitzaz, negar => negarraz
    if word.endswith('a'):
        word = word[:-1]
    return word + 'az'


@r_phonotactics
def possessive_genitive_undetermined(word: str) -> str:
    # tresna => tresnaren, etxe => etxeren, arto => artoren, hitz => hitzen, negar => negarren
    if word.endswith(('a', 'e', 'i', 'o', 'u')):
        word = word + 'r'
    return word + 'en'


@r_phonotactics
def possessive_genitive_singular(word: str) -> str:
    # tresna => tresnaren, etxe => etxearen, arto => artoaren, hitz => hitzaren, negar => negarraren
    if word.endswith('a'):
        word = word[:-1]
    return word + 'aren'


@r_phonotactics
def local_genitive_undetermined(word: str) -> str:
    # tresna => tresnatako, etxe => etxetako, arto => artotako, hitz => hitzetako, negar => negarretako
    if not word.endswith(('a', 'e', 'i', 'o', 'u')):
        word = word + 'e'
    return word + 'tako'


@r_phonotactics
def local_genitive_singular(word: str) -> str:
    # tresna => tresnako, etxe => etxeko, arto => artoko, hitz => hitzeko, negar => negarreko
    if not word.endswith(('a', 'e', 'i', 'o', 'u')):
        word = word + 'e'
    return word + 'ko'
