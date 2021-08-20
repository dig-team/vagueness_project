# Text Annotation Guideline

This is our guideline for the manual annotation of noun phrases in natural language text.

For a given text document, we produce an annotation file of the same file name as the text document, but in TSV format (Tab separated value). The columns are
- expression: the noun phrase
- plurality: an indicator that specifies if the noun phrase is plural or singular
- Yago4: the top-level class of YAGO4
- manifestation: the form that the head noun and its determiner take
- modifiers: the terms that modify the head noun
- vagueness: an indicator for the type of vagueness, if any

Each column (except plurality and Yago4) can take one or several space-separated values. Each value must come from a predefined list of values, which we detail next.

## Expression

This column contains the noun phrase. We take the longest possible sequence of words that constitutes a noun phrase, including adjectives, verbs, adverbs, prepositions, and nouns, but excluding sub-ordinate phrases. The noun phrases are extracted by a script, and have to be verified and corrected by hand.

## Plurality

This column indicates whether the noun phrase is plural or singular. Two values are permitted:
- instance: for singular phrases
- class: for plural phrases

We are interested here in the syntacic surface form, not the semantic plurality. Thus, the following are all instances: “A committee” (even if it is a group of persons), “a bird”, "the set of integers", “Europe” (even if it a group of countries), and “intelligence” (even if it is a mass noun). “Men”, “soldiers”, and “groups”, in contrast, are classes.

## Yago4 Class

This column can hold a single top-level class of the Yago taxonomy. The choice depends on the context: “America” can be a place (in sentences where it is the location where something happens), but also an organization (in sentences where it is a state actor). The classes are:

1. CreativeWork: anything that can be conceived and created by the human mind, including art works, books, ideas, theories, names, and languages: *Mulholland Drive (movie)*, *political philosophy*, *The radiocarbon work of Jonathan Haas*, *his campaign slogan*, *a graphic adventure puzzle video game*, *Climate engineering techniques*
1. Action: any activity that can be pursued or engaged in by one or several humans, when it is considered in its generality (independently of a specific instance): *smoking*, *comeback attempts*, *sexual abuse*, *the emission of greenhouse gases*, *geoengineering*
1. Event: any time period, as well as anything that did, will, or could happen: *his death*, *the last decades*, *in 2000*, *the 5th century BCE*, *the Age of Enlightenment*, *the early years of the Nazi regime*, *wildfires*, *heat waves*, *the resulting large-scale shifts in weather patterns*
1. Organization: any group of people that act together under a common name and head for an extended period of time: *Sun Records*, *multiple music halls of fame*, *a company*, countries (if used in the sense of a state actor)
1. Place: any location, in particular also countries when they are used in a geographical context: *various sites*, *That coastal strip*, *the lands of Anjou in France*
1. Person: any person or group of persons: *Elvis*, *a commitee*
1. Taxon: any living being except humans: *all non-avian dinosaurs*, *birds*
1. MedicalEntity: any entity that is an object of the field of medicine, including illnesses and parts of the body: *nasopharyngeal cancer*, *the disease*
1. Product: any physical object not yet covered by the above: *six million CDs*, *the food supplies*, *computers*, *city trains*, *an asteroid*
1. Intangible: any non-physical object not yet covered by the above: *freezing temperatures*, *A distinct national identity*, *Canada's allegiance*, *The painting's influence*, *the geological feature*

These categories should be checked in this order, using the first one that applies.

## Manifestation

This column indicates the nature of the head noun and its determiner. It can contain one of the following values:

- determined: generally “the XYZ”, or anything that is otherwise uniquely determined. Proper names do not need this value.
- undetermined: generally “a(n) XYZ”, or plural words without determiner
- qualified by anaphora: a noun phrase whose determiner is a possessive pronoun or demonstrative: *his men*, *this literature*, *their start in video game development*. However, in "Haas's dates", *dates* is not qualified by an anaphora.
- numbered: a noun phrase with a quantity (by a number or adverbial phrases): *80 women*, *a few occasions*, *some of the problems*, *Many different flags*, *much of this water*

In addition, and independently of the above, the column can contain one or several of the following values:
- anaphora: a reference to a previously mentioned entity (except by full name): *she*, *the volume*, *the battle*
- named: a proper name, usually with a capitalized head noun: *his brother John*. This does not apply if the noun phrase merely contains a noun, as in *Mongol forces*
- mass noun: anything that cannot be counted without adding a unit: *water*, *addition* (some words are mass nouns only in specific contexts)

## Modifiers

This column specified how the head noun is modified. Zero or more values are allowed:
- adjective: the head noun is accompanied by one or several adjectives: *the big city*
- preposition: the head noun is accompanied by one or several prepositions: *the vote in the city*
- noun: the head noun is accompanied by one or several preceding nouns: *vaccination movement*
- contains_name: the noun phrase as a whole contains a named entity: *the vote in the US*, *Robert Kennedy's assassination*
  
## Vagueness

This column indicates the type of vagueness. Possible values are:

1. degree (scalar): a threshold (even unknown or relative) can be used to determine if the expression is true. An example is the Heap paradox. Others are: *the highland areas of the Andes* (highland > T), *the first book-length attempt* (book-length > T).
2. portions (quantitative): the number, the portion, or the quantity of the entity is unspecified: *observers*, *some scripts*, *more than 100 people*
3. subjective: the concept is vague by nature. It can apply to a certain degree, and there is no consensus on how to measure this degree: *The painting's influence*, *beautiful painting*

Several cases may be more difficult to determine. We would therefore like to draw the reader's attention to these:

- Quantitative vagueness: the annotator must determine whether the noun phrase is for all entities or only a part of them. In the first case, we do not consider the noun phrase vague, but in the second case, it will be. For example, "Computer scientists believe that AES encryption is safe" is about a portion of computer scientists while "Computer scientists did not exist in the Middle Ages" is about all computer scientists.
- Subjective or scalar vagueness? One must ask whether there is only one way to measure vagueness. If so, then the noun phrase has scalar vagueness. If not, then it has subjective vagueness. Another way is to think about laws. If the concept is clear enough to be in a law, then it is scalar vagueness, otherwise it is subjective.
