import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

rawdocs = """The QWERTY layout depicted in Sholes's 1878 patent is slightly different from the modern layout, most notably in the absence of the numerals 0 and 1, with each of the remaining numerals shifted one position to the left of their modern counterparts. The letter M is located at the end of the third row to the right of the letter L rather than on the fourth row to the right of the N, the letters X and C are reversed, and most punctuation marks are in different positions or are missing entirely.[6] 0 and 1 were omitted to simplify the design and reduce the manufacturing and maintenance costs; they were chosen specifically because they were "redundant" and could be recreated using other keys. Typists who learned on these machines learned the habit of using the uppercase letter I (or lowercase letter L) for the digit one, and the uppercase O for the zero.[7]

The 0 key was added and standardized in its modern position early in the history of the typewriter, but the 1 and exclamation point were left off some typewriter keyboards into the 1970s."""
def summarizer(rawdocs):

    stopwords = list(STOP_WORDS)

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)

# Word tokenization
    tokens = [token.text for token in doc]
    word_freq = {}

    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

# Sentence tokenization
    sent_tokens = [sent for sent in doc.sents]
    sent_scores = {}

    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

# Summarization
    select_len = int(len(sent_tokens) * 0.4)
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))
