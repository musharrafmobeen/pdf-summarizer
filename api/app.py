import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


# def text_process(mess):
#     nopunc = [char for char in mess if char not in punctuation]
#     nopunc = ''.join(nopunc)
#     return [word for word in nopunc.split() if word.lower() not in stop_words]

stop_words = list(STOP_WORDS)
punctuation = punctuation + "\n"
# spacy.cli.download("en_core_web_sm")


# text = """
# Topic sentences are similar to mini thesis statements. Like a thesis statement, a topic sentence has a specific main point. Whereas the thesis is the main point of the essay, the topic sentence is the main point of the paragraph. Like the thesis statement, a topic sentence has a unifying function. But a thesis statement or topic sentence alone doesn’t guarantee unity. An essay is unified if all the paragraphs relate to the thesis, whereas a paragraph is unified if all the sentences relate to the topic sentence. Note: Not all paragraphs need topic sentences. In particular, opening and closing paragraphs, which serve different functions from body paragraphs, generally don’t have topic sentences.
# """

text2 = """""What Are Articles? (with Examples)
The articles are the words "a," "an," and "the." They define whether something is specific or unspecific. There are two types of article:

(1) The Definite Article (The). "The" is called the definite article. It defines its noun as something specific (e.g., something previously mentioned or known, something unique, something being identified by the speaker).
This is the lake.
(This is a previously specified lake, i.e., one already known to the readers.)
(2) The Indefinite Article (A, An). "A" and "an" are called the indefinite articles. They define their noun as something unspecific (e.g., something generic, something mentioned for the first time).
This is a lake.
(This is a previously unspecified lake.)
"""


def summarize(text):
    nlp = spacy.load('en_core_web_sm')

    doc = nlp(text)

    tokens = [token.text for token in doc]

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stop_words:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency

    sentence_tokens = [sent for sent in doc.sents]

    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    select_length = int(len(sentence_tokens)*0.3)

    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)

    for x, sum in enumerate(summary):
        summary[x] = summary[x].text

    # print(summary)

    return summary


summarize(text2)
