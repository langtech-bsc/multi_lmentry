<div align="center">

# Multi-LMentry: Can Multilingual LLMs Solve Elementary Tasks Across Languages?

[![Conference](https://img.shields.io/badge/EMNLP-2025-4b44ce)](https://2025.emnlp.org/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Hugging Face Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Dataset-FCD21D)](https://huggingface.co/datasets/BSC-LT/multi_lmentry)
</div>

<div align="center"> A repository containing the original code and outputs for the EMNLP 2025 paper "Multi-LMentry: Can Multilingual LLMs Solve Elementary Tasks Across Languages?" by Luca Moroni, Javier Aula-Blasco, Simone Conia, Irene Baucells, Naiara Perez, Silvia Paniagua Suárez, Anna Sallés, Malte Ostendorff, Júlia Falcão, Guijin Son, Aitor Gonzalez-Agirre, Roberto Navigli, Marta Villegas. </div>

<br><br>

**Multi-LMentry** is a multilingual extension of **LMentry (Efrat et al., 2023)**, which evaluates LLMs on tasks that are trivial for humans but often challenging for models. It covers nine languages:

- Catalan - *code:* ca
- Spanish - *code:* es
- German - *code:* de
- Basque - *code:* eu
- Galician - *code:* gl
- Korean - *code:* ko
- Italian - *code:* it
- Brazilian Portuguese - *code:* pt_br
- English (original LMentry dataset) - *code:* en


The dataset enables systematic evaluation of core model abilities across low-, mid-, and high-resource languages. Tasks were recreated manually with the help of native speakers, ensuring linguistic and cultural appropriateness rather than relying on direct translation.



## 🛠️ Installation

Installation from source:

```bash
git clone https://github.com/langtech-bsc/multi_lmentry.git
cd multi_lmentry
conda create -n multi_lmentry python==3.12
conda activate multi_lmentry
pip install -e .
```

## Data Creation

Under `resources` folder are present all the annotated resources for each nine langauges needed to build samples in the Multi-LMentry benchmark.

To evaluate models on Multi-LMentry, you need locally recreate, from annotated resources, the benchmark samples. 

```python
python recreate_tasks.py
```

For further research and analysis, we release all the created data under <a href="https://huggingface.co/datasets/BSC-LT/multi_lmentry">huggingface repository</a>.

## Model Generation 

To generate predictions over the Multi-LMentry benchmark you can execute:

```python
python execute_generation.py \
    --lang "lang_id" \
    --model_list "model_name_1 model_name_2 ..."
```

The `execute_generation.py` script will save results under `evaluation` folder.

The `lang` parameter should be one of the available lang identificators.

The `model_list` parameter should be a list of model's names, defined in the `lmentry/constants.py` file. To add a new model you have to define there, using the following template.

```json
paper_models = {
    "model_name" : {"short_name": "...", "paper_name": "huggingface name", "predictor_name": "huggingface name"},
    ...
}
```

## Model Evaluation

Once you have generated all the predictions, is possible to evaluate the outputs using the scorers:

```python
python execute_eval.py \
    --lang "lang_id" \
    --num_proc "xx"
```

The `execute_eval.py` script will save overwrite the files under `evaluation` folder, and then it will create summary statistics under `results` folder.

The `lang` parameter should be one of the available lang identificators.

The `num_proc` parameter should a strictly positive integer.

## Cite this work

If you use any part of this work, please consider citing the paper as follows:

```bibtex
@inproceedings{,
  title={}, 
  author={},
  booktitle={},
  pages={},
  year={2025}
}
```

## 🪪 License

The data and software are licensed under [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Acknowledgements
We gratefully acknowledge the support of Future AI Research ([PNRR MUR project PE0000013-FAIR](https://fondazione-fair.it/en/)).

The authors gratefully acknowledge the support of the AI Factory IT4LIA project and the CINECA award FAIR_NLP under the ISCRA initiative for granting access high-performance computing resources.

This work is funded by the Ministerio para la Transformación Digital y de la Función Pública and Plan de Recuperación, Transformación y Resiliencia - Funded by EU – NextGenerationEU within the framework of the project ILENIA with references 2022/TL22/00215337, 2022/TL22/00215336 and 2022/TL22/00215335, and within the framework of the project Desarrollo Modelos ALIA.

This work has been promoted and financed by the Generalitat de Catalunya through the Aina project.

