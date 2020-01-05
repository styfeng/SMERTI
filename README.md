# SMERTI for Semantic Text Exchange
Code for the SMERTI pipeline designed for Semantic Text Exchange, presented in [*Keep Calm and Switch On! Preserving Sentiment and Fluency in Semantic Text Exchange*](https://www.aclweb.org/anthology/D19-1272/) published at EMNLP-IJCNLP 2019.


## Following is a brief description of what each file does:

Data Preprocessing and Preparation:
- Dataset_preprocessing_(reviews) and Dataset_preprocessing_(news) are for preprocessing the reviews (e.g. Yelp and Amazon) and news headlines, respectively, generating training and testing splits, and writing them to .txt files.
- Dataset_masking_(reviews) and Dataset_masking_(news) are for generating masked versions of the training and testing data from step 1. for reviews and news headlines, respectively, and writing them to .txt files.

Text Infilling Module (TIM) Training:
- RNN_training and Transformer_training are to train the TIM for SMERTI-RNN and SMERTI-Transformer, respectively, based on the .txt files generated from steps 1. and 2. above.
- RNN_final_pipeline and Transformer_final_pipeline are the final pipelines for SMERTI-RNN and SMERTI-Transformer, respectively. This includes the ERM, SMM, and TIM components of each pipeline variation. Also note that the bottom of each file includes a section to generate and write output to .txt files, based on the evaluation lines generated from step 5. below, to be used in metric calculations in step 6.

Evaluation:
- Evaluation_setup is to generate the evaluation lines for the datasets and includes choosing nouns, choosing evaluation lines per noun, and writing them to .txt files.
- Final_evaluation is to calculate metrics including SPA, BLEU, Perplexity, and SLOR using SMERTI's output from the evaluation lines, and includes functions to write results to .txt files.
- SLOR_normalization is to normalize all SLOR values (81,000 in our case) calculated from step 6. above to a [0,1] interval.