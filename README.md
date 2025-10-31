<div align="center">

# Multi-LMentry: Can Multilingual LLMs Solve Elementary Tasks Across Languages?

[![Conference](https://img.shields.io/badge/EMNLP-2025-4b44ce)](https://2025.emnlp.org/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Hugging Face Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Dataset-FCD21D)](https://huggingface.co/datasets/BSC-LT/multi_lmentry)
</div>

<p align="center">
  <img src="https://github.com/Andrew-Wyn/images/blob/master/multi_lmentry/LMentry-LOGO-no_bgrd.png"
       width="400">
</p>

<div align="center"> A repository containing the original code and data for the EMNLP 2025 paper "Multi-LMentry: Can Multilingual LLMs Solve Elementary Tasks Across Languages?" by Luca Moroni, Javier Aula-Blasco, Simone Conia, Irene Baucells, Naiara Perez, Silvia Paniagua Suárez, Anna Sallés, Malte Ostendorff, Júlia Falcão, Guijin Son, Aitor Gonzalez-Agirre, Roberto Navigli, Marta Villegas. </div>

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
pip install flash-attn
```

## Model Generation 

To generate predictions over the Multi-LMentry benchmark you can execute:

```python
python execute_generation.py \
    --lang "lang_id" \
    --model_name "model_name_1" \
    --use_vll \
    --max_new_tokens \
    --batch_size
```

The `execute_generation.py` script will save results under `evaluation` folder.

The `lang` parameter should be one of the available lang identificators.

The `model_name` parameter should a model's name, defined in the `lmentry/models.py` file. To add a new model you have to define there one name, using the following template.

The `use_vllm` parameter is a boolean flag, needed to activate the vllm engine instead of the default HF generation pipeline.

The `max_new_tokens` parameter is the maximum number of tokens to generate for each sample, default is `1024`.

The `max_new_tokens` parameter is the number of sample to process in a single batch, default is `8`. It is not used when `use_vllm` is set.

```python
paper_models = {
    "model_name" : {"short_name": "short name of a model", "paper_name": "huggingface name", "predictor_name": "huggingface name"},
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

## Data Creation

Under `resources` folder are present all the annotated resources for each nine langauges needed to build samples in the Multi-LMentry benchmark.

The Multi-LMentry benchmark can be create from annotated resources, to have the seme data as the ones uploaded on HuggingFace.

```python
python recreate_tasks.py
```

We release all the created data under <a href="https://huggingface.co/datasets/BSC-LT/multi_lmentry">huggingface repository</a>.

## Cite this work

If you use any part of this work, please consider citing the paper as follows:

```bibtex
@inproceedings{moroni-etal-2025-multilmentry,
  title = "Multi-LMentry: Can Multilingual LLMs Solve Elementary Tasks Across Languages?",
  author = "Moroni, Luca  and
      Aula-Blasco, Javier  and
      Conia, Simone  and
      Baucells, Irene  and
      Perez, Naiara  and
      Paniagua Suárez, Silvia  and
      Sallés, Anna  and
      Ostendorff, Malte  and
      Falcão, Júlia  and
      Son, Guijin  and
      Gonzalez-Agirre, Aitor  and
      Navigli, Roberto and
      Villegas, Marta",
  booktitle = "Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing",
  pages= "xx-yy",
  year= "2025",
}
```

## 🪪 License

The data and software are licensed under [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Acknowledgements
We gratefully acknowledge the support of Future AI Research ([PNRR MUR project PE0000013-FAIR](https://fondazione-fair.it/en/)).

The authors gratefully acknowledge the support of the AI Factory IT4LIA project and the CINECA award FAIR_NLP under the ISCRA initiative for granting access high-performance computing resources.

This work is funded by the Ministerio para la Transformación Digital y de la Función Pública and Plan de Recuperación, Transformación y Resiliencia - Funded by EU – NextGenerationEU within the framework of the project ILENIA with references 2022/TL22/00215337, 2022/TL22/00215336 and 2022/TL22/00215335, and within the framework of the project Desarrollo Modelos ALIA.

This work has been promoted and financed by the Generalitat de Catalunya through the Aina project.

