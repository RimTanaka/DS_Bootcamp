import pytest
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from movielens_analysis import Tags


@pytest.fixture
def mock_tags_file(tmp_path):
    content = (
        "userId,movieId,tag,timestamp\n"
        "1,1,funny,1139045764\n"
        "2,2,action packed,1139045765\n"
        "3,3,very emotional scene,1139045766\n"
        "4,4,heart warming,1139045767\n"
        "5,5,funny,1139045768\n"
        "6,6,deep thought provoking masterpiece,1139045769\n"
        "7,7,funny scenes,1139045770\n"
        "8,8,not so good,1139045771\n"
    )
    path = tmp_path / "tags.csv"
    path.write_text(content)
    return str(path)


@pytest.fixture
def tags_instance(mock_tags_file):
    return Tags(mock_tags_file)


def test_most_words(tags_instance):
    result = tags_instance.most_words(2)
    assert isinstance(result, dict)
    top_tag = list(result.keys())[0]
    assert result[top_tag] == max(result.values())


def test_longest(tags_instance):
    result = tags_instance.longest(2)
    assert isinstance(result, list)
    assert all(isinstance(tag, str) for tag in result)
    assert len(result[0]) >= len(result[1])


def test_most_words_and_longest(tags_instance):
    result = tags_instance.most_words_and_longest(5)
    assert isinstance(result, list)
    assert all(isinstance(tag, str) for tag in result)


def test_most_popular(tags_instance):
    result = tags_instance.most_popular(2)
    assert isinstance(result, dict)
    assert result.get("funny") == 2


def test_tags_with(tags_instance):
    result = tags_instance.tags_with("funny")
    assert isinstance(result, list)
    assert "funny" in result or any("funny" in tag for tag in result)
    assert result == sorted(result)
