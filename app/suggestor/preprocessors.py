import os
import pathlib
import re
import string

import numpy as np
import pandas as pd

# from nltk.corpus import stopwords
import spacy
from lxml import html
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import FunctionTransformer
from spacy.lang.en import stop_words

ARTIFACT_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(),
                             'artifacts')

replacements = {
    'c#': 'c_sharp', 'f#': 'f_sharp',
    'c++': 'c_plusplus', 'h++': 'h_plusplus',
    'obj-c++': 'obj_c_plusplus', 'objective-c++': 'objective_c_plusplus',
    ' .net': ' dot_net'
}
reverse_replacements = {v: k for k, v in replacements.items()}


def filter_c_family(_data: str) -> str:
    for pattern, replacement in replacements.items():
        _data = re.sub(re.escape(pattern), replacement, _data)
    return _data


def unfilter_c_family(_tags: list) -> list:
    def replace_tags(text):
        for pattern, replacement in reverse_replacements.items():
            text = re.sub(re.escape(pattern), replacement, text)
        return text

    _data = pd.Series(_tags).map(lambda x: " ".join(x))
    _data = _data.map(replace_tags)
    return [x.split(" ") for x in _data]


class TextPreprocessor:
    def __init__(self):
        self.lem_allowed_postags = ['NOUN']
        self.stop_words = stop_words.STOP_WORDS
        self.lem_model = spacy.load("en_core_web_md",
                                    disable=['parser', 'ner'])

    def extract_sentences_from_body_transformer(self, _df: np.array):
        _df = _df.map(lambda x: self.extract_sentences_from_body(str(x)))
        return _df.values.reshape(-1, 1)

    def extract_sentences_from_body(self, _data: str) -> str:
        doc = html.fromstring(_data)
        paragraphes = doc.cssselect('p')
        if len(paragraphes) == 0:
            return ""
        return " ".join([p.text_content()
                         for p in paragraphes
                         if p.text_content() is not None])

    def clean_sentence_transformer(self, _df: np.array) -> pd.DataFrame:
        _df = pd.DataFrame(_df)
        _df = _df.iloc[:, 0]
        _df = _df.map(lambda x: self.clean_sentence(str(x)))
        _df = _df.values.reshape(-1, 1)
        return _df

    def clean_sentence(self, sentence: str) -> str:
        # Convert to lowercase
        sentence_cleaned = sentence.lower()

        # Combine multiple regex substitutions into one
        sentence_cleaned = re.sub(
            r'[^\x00-\x7F]+|'  # Non-ASCII characters
            r'\s[0-9]+|'  # Numbers preceded by whitespace
            r'(&*;)|'  # HTML entities
            r'(<code.*code>)|'  # Code tags
            r'https?:\/\/.*[\r\n]*|'  # URLs
            r'\S*@\S*\s?|'  # Email addresses
            r'\n',  # Newlines
            ' ',
            sentence_cleaned
        )

        # Apply custom transformation
        sentence_cleaned = filter_c_family(sentence_cleaned)

        # Remove punctuation (except underscores) and extra spaces
        sentence_cleaned = re.sub(
            rf"[{string.punctuation.replace('_', '')}]|\s+",
            ' ',
            sentence_cleaned
        ).strip()

        return sentence_cleaned

    def tokenize_for_bow(self, sentence: list) -> str:
        # Define the set of useless words for faster lookup
        useless_words_set = {"use", "get", "create", "way", "find",
                             "return", "add", "work",
                             "error", "issue", "file",
                             "code", "try", "want", "follow", "need",
                             "run", "problem", "know",
                             "value", "make", "fix"}
        # # Split the sentence into words
        # words = sentence.split()
        # Filter out stop words
        filtered_words = [word for word in sentence
                          if word not in self.stop_words]
        # Lemmatize the filtered words
        doc = self.lem_model(" ".join(filtered_words))
        # Filter lemmatized words
        # based on part of speech and other criteria
        processed_words = [
            token.lemma_ for token in doc
            if token.pos_ in self.lem_allowed_postags
            if token.lemma_ not in useless_words_set
            if 2 <= len(token.lemma_) <= 25
        ]
        # Join the processed words into a single string
        processed_words = ' '.join(processed_words)
        return processed_words

    def vectorize(self, _data):
        import joblib
        vectorizer = joblib.load(
            pathlib.Path(ARTIFACT_PATH, "cv.pkl"))
        transformer = joblib.load(
            pathlib.Path(ARTIFACT_PATH, "tfidf.pkl"))
        _data = _data.split(" ")
        _data_vect = vectorizer.transform(_data)
        _data_vect = transformer.transform(_data_vect)
        return _data_vect

    def get_pipeline(self):
        # Clean Title
        title_transformer = FunctionTransformer(
            self.clean_sentence_transformer,
            validate=False)

        # Clean Body
        body_transformer = make_pipeline(
            FunctionTransformer(
                self.extract_sentences_from_body_transformer,
                validate=False),
            FunctionTransformer(
                self.clean_sentence_transformer,
                validate=False),
        )

        # Preprocess Title + Body
        _preprocessor = ColumnTransformer([
            ('title_transformer', title_transformer, 'Title'),
            ('body_transformer', body_transformer, 'Body')
        ])

        def combine_fn(_data: np.ndarray):
            _data = [' '.join(map(str, row)) for row in _data]
            return _data

        # Combine Title + Body
        combine_transformer = FunctionTransformer(
            combine_fn
            # lambda x: [' '.join(map(str, row)) for row in x]
        )

        # Tokenize Title + Body
        tokenize_transformer = FunctionTransformer(
            self.tokenize_for_bow,
            validate=False)

        # Vectorize Title + Body
        vectorize_transformer = FunctionTransformer(
            self.vectorize,
            validate=False)

        # Final pipeline
        pipeline_x = Pipeline([
            ("preprocess", _preprocessor),
            ("combine", combine_transformer),
            ("tokenize", tokenize_transformer),
            ("vectorize", vectorize_transformer),
        ])

        return pipeline_x

    def preprocess_text(self, _title: str, _body: str) -> pd.DataFrame:
        x_texts = pd.DataFrame([[_title, _body]],
                               columns=["Title", "Body"])
        texts_preprocessed = self.get_pipeline().fit_transform(x_texts)
        return texts_preprocessed


if __name__ == "__main__":
    test = TextPreprocessor().tokenize_for_bow(["How to use a Flutter?"])
    print(test)
