# The Vagueness of Vagueness in Noun Phrases

Natural language text has a great potential to feed knowledge bases. However, natural language is not always precise - and sometimes intentionally so. In this work, we study vagueness in noun phrases. We manually analyze the frequency of vague noun phrases in a Wikipedia corpus, and find that 1/4 of noun phrases exhibit some form of vagueness. We report on their nature and propose a categorization. We then conduct a literature review and present different definitions of vagueness, and different existing methods to deal with the detection and modeling of vagueness. We find that, despite its frequency, vagueness has not yet be addressed in its entirety.

## Content

All data are located in the `data` directory:

- `articles`: this folder contains the 30 original Wikipedia articles.
- `annotation guideline.md`: this file describes the process we followed to annotate the Wikipedia articles.
- `annotations`: this folder contains the annotations of articles from the `articles` folder.
- `stats`: this folder contains the stats we computed. You can check both the annotations and the code we used to compute those stats.

The `analysis.py` script can be executed to compute the stats corresponding to our annotations.

## To go further

To learn more about our work, read (and cite) our paper:

[Pierre-Henri Paris](https://phparis.net), Syrine El Aoud, and [Fabian M. Suchanek](https://suchanek.name) : “[The Vagueness of Vagueness in Noun Phrases](https://suchanek.name/work/publications/akbc-2021-vagueness.pdf)”, AKBC 2021

## Acknowledgments

This work was partially funded by the grant ANR-20-CHIA-0012-01 ("NoRDF").
