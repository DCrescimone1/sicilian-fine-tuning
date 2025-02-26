---
license: odc-by
language:
- en
- scn
task_categories:
- translation
pretty_name: Good Sicilian in the NLLB
size_categories:
- 100K<n<1M
---
# Good Sicilian in the NLLB

"Language models are few shot learners" ([Brown et al. 2020](https://arxiv.org/abs/2005.14165)).  And after drinking a few shots, several prominent translation models now slur their speech and garble a very strange version of Sicilian, one that does not appear in the NLLB dataset or anywhere in the Sicilian literary tradition. 

Waking up the next morning, we all have a headache, so in lieu of aspirin, [Project Napizia](https://www.napizia.com/) supplies this "Good Sicilian" data package to the NLP community.  We hope it will help language models learn "Good Sicilian."

## What is "Good Sicilian"?

[Arba Sicula](https://arbasicula.org/) has been translating Sicilian poetry and prose into English since 1979.  They have translated so much Sicilian language text that Project Napizia trained a [neural machine Sicilian translation model](https://translate.napizia.com/) with their bilingual journal ([Wdowiak 2021](https://arxiv.org/abs/2110.01938) and [Wdowiak 2022](https://doi.org/10.1007/978-3-031-10464-0_50)). In addition to the journal, Arba Sicula also publishes books on Sicilian language, literature, culture and history.  And they organize poetry recitals, concerts, cultural events and an annual tour of Sicily.

"Good Sicilian" presents an 800-year literary tradition.  "Good Sicilian" is the literary language described in the three grammar textbooks that Arba Sicula has published.

## The NLLB team's search for "Good Sicilian"

"Good Sicilian" is what Facebook sought to collect during the [No Language Left Behind project (2022)](https://arxiv.org/abs/2207.04672).  Project Napizia wishes that the NLLB team had contacted Arba Sicula.  Instead, the NLLB team consulted people who made Sicilian one of "the more difficult languages" to work with.  As the NLLB team explains on page 23 of their paper, their consultants provided seed data and validation data with "lower levels of industry-wide standardization."

In particular, the seed data reflected a strange new orthographic proposal that first appeared in 2017, while the lion's share of Sicilian text was written prior to 2017.  The dissimilarity between seed data and available data caused the NLLB project to collect poor-quality Sicilian language data.

And because the validation data also reflects the strange new orthographic proposal, the dissimilarity of the validation data is not very helpful when evaluating a model trained on the NLLB data (or any Sicilian language data).

## The "Good Sicilian" in the NLLB dataset

The purpose of this data package is to identify "Good Sicilian" translations in the NLLB dataset.

Upon visual inspection of the original collection, someone acquainted with the Sicilian language will immediately notice a "rhapsody of dialects."  The surprise occurs because some of the good translations are not "Good Sicilian."  In those cases, the Sicilian reflects a regional or local pronunciation -- what Sicilians and Italians call "dialect." Those sentences come from the Sicilian folklore  tradition.  It's "good Sicilian folklore," but for language modelling, we need "good Sicilian language." Fortunately, most of the NLLB data reflects the Sicilian literary tradition -- what people call "language."

The purpose of this data package is to identify the good translations that are "Good Sicilian," so that the NLP community can train better language models for the Sicilian language.  For that purpose, Project Napizia used one of its translation models to score the pairs on the task of English-to-Sicilian translation and sorted the pairs by score.

Like golf, a low score is a better score.  Napizia's scores come from [Sockeye](https://awslabs.github.io/sockeye/)'s scorer, which presents the negative log probability that the target subword sequence is a translation of the source subword sequence.  So a score close to zero implies a probability close to one.  A low score is a better score.

Napizia plays golf.  Facebook plays basketball.  Facebook's score measures similarity between sentences.  At Facebook, a high score is a better score.  We present both Facebook's score and Napizia's score.  And we apologize in advance for the inevitable confusion.

Finally, for a convenient way to examine the best pairs, we provide a tab-separated CSV spreadsheet of the 50,000 pairs with the best Napizia score.

We hope researchers and practitioners will use this rescored NLLB data will help language models learn "Good Sicilian."  We'll update this project with more public collections of "Good Sicilian."

And along with "Good Sicilian," we'll serve the NLP community a giant plate full of cannoli too!  ;-)

# Dataset Card -- scored English-Sicilian from NLLB-200vo

## Dataset Summary

This dataset is a subset created from [metadata](https://github.com/facebookresearch/fairseq/tree/nllb) for mined bitext released by Meta AI.  The original contains bitext for 148 English-centric and 1465 non-English-centric language pairs using the stopes mining library and the LASER3 encoders ([Heffernan et al, 2022](https://arxiv.org/abs/2205.12654)).

Subsequently, Allen AI prepared bilingual collections for Hugging Face and for OPUS.  The dataset presented here contains 1,057,469 pairs from the OPUS collection scored by Napizia on the task of English-to-Sicilian translation.

## Licensing Information

The dataset is released under the terms of [ODC-BY](https://opendatacommons.org/licenses/by/1-0/). By using this, you are also bound to the respective Terms of Use and License of the original source.

## Sources

A. Fan et al (2020). "[Beyond English-Centric Multilingual Machine Translation](https://arxiv.org/abs/2010.11125)."

K. Hefferman et al (2022). "[Bitext Mining Using Distilled Sentence Representations for Low-Resource Languages](https://arxiv.org/abs/2205.12654)."

NLLB Team et al (2022). "[No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672)."

H. Schwenk et al (2021). "[CCMatrix: Mining Billions of High-Quality Parallel Sentences on the Web](https://aclanthology.org/2021.acl-long.507/)."

J. Tiedemann (2012). "[Parallel Data, Tools and Interfaces in OPUS](https://www.aclweb.org/anthology/L12-1246/)."

E. Wdowiak (2021). "[Sicilian Translator: A Recipe for Low-Resource NMT](https://arxiv.org/abs/2110.01938)."

E. Wdowiak (2022). "[A Recipe for Low-Resource NMT](https://doi.org/10.1007/978-3-031-10464-0_50)."
