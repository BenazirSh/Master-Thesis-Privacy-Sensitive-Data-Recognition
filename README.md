## Introduction

The repository contains the source code for the implementation of 
 Master Thesis for 'Generating Synthetic CV Data with GPT4 for Privacy Sensitive Data Recognition'.

## Instructions

### Running the CV PSI detection and anonymization program

#### Important
This repository also contains the trained model in the `bert-ner-fine-tuned-with-educational-institutions`,
which has the model files that are around ~450MB, thus requiring Git LFS (Git Large-File-System) to be installed.

#### Execution steps
1. Make sure to install Git LFS to your computer: https://git-lfs.com/.
2. Make sure Python is installed if not already: https://www.python.org/ 
3. Clone the repository.
4. Run `git lfs pull` to pull the model files.
5. Create Python virtual environment by running: `python3 -m venv .venv`
6. Activate the Virtual environment (https://docs.python.org/3/library/venv.html):
   * Windows: `.\venv\Scripts\activate`
   * Linux: `source .venv/bin/activate`
   * macOS: `source .venv/bin/activate`
7. To install dependencies: `pip3 install -r requirements.txt`
8. To run the psi_custom_ner_extractor.py (the main python file of the program),
either run the file through IDE or run `python3 psi_custom_ner_extractor.py`.
9. To run the psi_extractor_main.py,
either run the file through IDE or run `python3 psi_extractor_main.py`.

### Model training

Model training was done on Google Colab (https://colab.research.google.com/), and the code is written in Jupyter Notebook, 
please see the file `Model_Training_BERT_NER_Educational_Institutions.ipynb`.

Preferred method to run the training process is via Google Colab (https://colab.research.google.com/).

#### Execution steps
1. Open Google Colab https://colab.research.google.com/.
2. Click File => Upload Notebook, and select the file.
3. Once the notebook is opened, you can click Runtime => Run all, that will handle everything including:
   * installing dependencies
   * relabeling the dataset
   * training the model
   * evaluating the model metrics
   * saving the model
---
**Master thesis:** Generating Synthetic CV Data with GPT4 for Privacy Sensitive Data Recognition

**Author:** Benazir Sharipova, Matriculation No.: 8010153

**Advisor:** Sascha Löbner

**Year:** 2024

Submitted to Prof. Dr. Kai Rannenberg

Chair of Business Administration, especially Business Informatics, Mobile Business and Multilateral Security, Johann Wolfgang Goethe-Universität Frankfurt

