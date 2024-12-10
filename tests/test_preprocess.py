import numpy as np
import pandas as pd
import pytest

from app.suggestor.preprocessors import (
    TextPreprocessor,
    filter_c_family,
    unfilter_c_family,
)


# Tests for filter_c_family and unfilter_c_family
def test_filter_c_family():
    test_input = "This is c# and c++ code with .net"
    expected = "This is c_sharp and c_plusplus code with dot_net"
    assert filter_c_family(test_input) == expected


def test_unfilter_c_family():
    test_input = [["c_sharp", "dot_net", "c_plusplus"]]
    expected = [["c#", ".net", "c++"]]
    assert unfilter_c_family(test_input) == expected


# Tests for TextPreprocessor class
@pytest.fixture
def text_preprocessor():
    return TextPreprocessor()


def test_extract_sentences_from_body(text_preprocessor):
    html_content = "<p>This is a test paragraph</p><p>Another paragraph</p>"
    expected = "This is a test paragraph Another paragraph"
    result = text_preprocessor.extract_sentences_from_body(html_content)
    assert result == expected


def test_extract_sentences_from_empty_body(text_preprocessor):
    html_content = "<div>No paragraphs here</div>"
    expected = ""
    result = text_preprocessor.extract_sentences_from_body(html_content)
    assert result == expected


def test_clean_sentence(text_preprocessor):
    test_cases = [
        ("Hello World!", "hello world"),
        ("C# and .NET", "c_sharp and dot_net"),
        ("test@email.com", ""),
        ("Windows10 World", "windows10 world"),
        ("<code>some code</code>", ""),
        ("https://example.com", ""),
    ]
    for input_text, expected in test_cases:
        assert text_preprocessor.clean_sentence(input_text) == expected


def test_tokenize_for_bow(text_preprocessor):
    input_text = "How to use a Flutter?"
    result = text_preprocessor.tokenize_for_bow([input_text])
    assert isinstance(result, str)
    assert "flutter" in result


def test_preprocess_text(text_preprocessor):
    title = "How to use Python?"
    body = "<p>I want to learn Python programming</p>"
    result = text_preprocessor.preprocess_text(title, body).todense()
    assert isinstance(result, np.ndarray)


def test_get_pipeline(text_preprocessor):
    pipeline = text_preprocessor.get_pipeline()
    assert pipeline is not None
    assert hasattr(pipeline, 'fit_transform')


# Test the transformer functions with DataFrame inputs
def test_clean_sentence_transformer(text_preprocessor):
    test_df = np.array([["Hello World!", "Test 123"]])
    result = text_preprocessor.clean_sentence_transformer(test_df)
    assert isinstance(result, np.ndarray)
    assert result.shape[1] == 1


def test_extract_sentences_from_body_transformer(text_preprocessor):
    test_df = pd.Series(["<p>Test paragraph</p>"])
    result = text_preprocessor.extract_sentences_from_body_transformer(test_df)
    assert isinstance(result, np.ndarray)
    assert result.shape[1] == 1
