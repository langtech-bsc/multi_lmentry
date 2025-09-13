import re

from lmentry.scorers.pt_br.scorer import LMentryScorer

pt_br_plurals = { "adjetivo": "adjetivos", "advérbio": "advérbios", "animal": "animais", "catástrofe": "catástrofes", "natural": "naturais", "categoria": "categorias", "cômodo": "cômodos", "conjunção": "conjunções", "cor": "cores", "dia": "dias", "família": "famílias", "ferramenta": "ferramentas", "gênero": "gêneros", "cinematográfico": "cinematográficos", "geografia": "geografias", "instrumento": "instrumentos", "musical": "musicais", "legume": "legumes", "local": "locais", "material": "materiais", "medida": "medidas", "mês": "meses", "numeral": "numerais", "ordinal": "ordinais", "parte": "partes", "peça": "peças", "pessoa": "pessoas", "preposição": "preposições", "profissão": "profissões", "pronome": "pronomes", "substantivo": "substantivos", "termo": "termos", "transporte": "transportes", "verbo": "verbos", "verdura": "verduras", "etapa": "etapas" }

class AllWordsFromCategoryScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, answer, category):

        all_words = r"(todas estas palavras|todas essas palavras|todas as palavras|todas elas|todas)"
        listed = r"(listadas|na lista|da lista|dessa lista|nessa lista)"
        belong = r"(representam|são tipos de|fazem referência a|se referem a|são exemplos de|contém exclusivamente)"

        base_patterns = [
            rf"{answer}, a lista inclui exclusivamente {category}",
            rf"{answer}, a lista só inclui {category}",
            rf"{answer}, a lista inclui somente {category}",
            rf"{answer}, as palavras {listed} {belong} {category}"
            rf"{answer}, {all_words}( {listed})? {belong} {category}",
            rf"^{answer}\b",
        ]

        return base_patterns + self.get_shared_patterns(target=answer)

    @staticmethod
    def category_regex(category):
        if category == "peça de roupa":
            category = rf"({category}|roupas|vestimentas|vestuário)"
        elif category == "cômodo da casa ou mobília":
            category = rf"({category}|cômodo|móvel|móveis)"

        category_plural = None
        for singular, plural in pt_br_plurals.items():
            category_plural = re.sub(rf"\b({singular})\b", plural, (category_plural or category))

        if category_plural:
            category = rf"({category}|{category_plural})"

        return category

    @staticmethod
    def negative_scorer(prediction, answer):
        score = None
        certainty = None

        opposite_answer = "não" if answer == "sim" else "sim"
        if re.match(rf"{opposite_answer}\.?$", prediction):
            score = 0
            certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        metadata = example["metadata"]
        answer = "sim" if metadata["num_distractors"] == 0 else "não"

        score, certainty = self.negative_scorer(prediction, answer)
        if score is not None:
            return score, certainty

        score, certainty = self._simple_scorer(prediction, answer)
        if score:
            return score, certainty

        category = metadata["category"]
        category = AllWordsFromCategoryScorer.category_regex(category)

        base_patterns = self.get_base_patterns(answer, category)
        score, certainty = self.certainty_scorer(prediction, base_patterns)

        return score, certainty
