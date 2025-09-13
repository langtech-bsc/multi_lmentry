import re

from lmentry.scorers.es.scorer import LMentryScorer


class AllWordsFromCategoryScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, answer, category):

        all_words = r"(todas estas palabras|todas esas palabras|todas las palabras|todas ellas|todas)"
        listed = r"(listadas|en la lista|de la lista)"
        belong = r"(representan|son tipos de|hacen referencia a|se refieren a|son ejemplos de|contienen exclusivamente)"

        base_patterns = [
            rf"{answer}, la lista incluye exclusivamente {category}",
            rf"{answer}, la lista solo incluye {category}",
            rf"{answer}, las palabras {listed} {belong} {category}"
            rf"{answer}, {all_words}( {listed})? {belong} {category}",
            rf"^{answer}\b",
        ]

        return base_patterns + self.get_shared_patterns(target=answer)

    @staticmethod
    def category_regex(category):
        if category == "animal":
            category = rf"({category}|animales|tipos de animal)"
        elif category == "categoría gramatical":
            category = rf"({category}|categorías gramaticales)"
        elif category == "catástrofe natural":
            category = rf"({category}|catástrofes naturales)"
        elif category == "color":
            category = rf"({category}|colores)"
        elif category == "parte del cuerpo humano":
            category = rf"({category}|partes del cuerpo humano)"
        elif category == "deporte":
            category = rf"({category}|deportes|tipos de deporte)"
        elif category == "día de la semana":
            category = rf"({category}|días de la semana)"
        elif category == "palabra relacionada con la economía":
            category = rf"({category}|palabras relacionadas con la economía|conceptos de economía)"
        elif category == "palabra relacionada con espacio y cantidad":
            category = rf"({category}|palabras relacionadas con espacio y cantidad|conceptos de espacio y cantidad)"
        elif category == "relación familiar":
            category = rf"({category}|relaciones familiares|miembros de la familia)"
        elif category == "palabra relacionada con la geografía":
            category = rf"({category}|palabras relacionadas con la geografía|conceptos de geografía|conceptos geográficos)"
        elif category == "género de películas":
            category = rf"({category}|géneros de películas)"
        elif category == "herramienta":
            category = rf"({category}|herramientas)"
        elif category == "palabra relacionada con el hogar":
            category = rf"({category}|palabras relacionadas con el hogar|conceptos del hogar|componentes del hogar)"
        elif category == "instrumento musical":
            category = rf"({category}|instrumentos musicales)"
        elif category == "lugar de trabajo":
            category = rf"({category}|lugares de trabajo)"
        elif category == "material":
            category = rf"({category}|materiales)"
        elif category == "medida":
            category = rf"({category}|medidas)"
        elif category == "profesion":
            category = rf"({category}|profesiones)"
        elif category == "ropa":
            category = rf"({category}|prendas de ropa)"
        elif category == "palabra relacionada con la sociedad":
            category = rf"({category}|palabras relacionadas con la sociedad|conceptos de sociedad)"
        elif category == "sustantivo abstracto":
            category = rf"({category}|sustantivos abstractos)"
        elif category == "palabra relacionada con el transporte":
            category = rf"({category}|palabras relacionadas con el transporte|conceptos de transporte)"
        elif category == "verdura":
            category = rf"({category}|verduras)"
        elif category == "vida":
            category = rf"({category}|conceptos de la vida|conceptos del ciclo vital)"

        return category

    @staticmethod
    def negative_scorer(prediction, answer):
        score = None
        certainty = None

        opposite_answer = "no" if answer == "sí" else "sí"
        if re.match(rf"{opposite_answer}\.?$", prediction):
            score = 0
            certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        metadata = example["metadata"]
        answer = "sí" if metadata["num_distractors"] == 0 else "no"

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
