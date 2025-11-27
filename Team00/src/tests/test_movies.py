import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from movielens_analysis import Movies


@pytest.fixture
def mock_movies_file(tmp_path):
    content = (
        "movieId,title,genres\n"
        "1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy\n"
        "2,Jumanji (1995),Adventure|Children|Fantasy\n"
        "3,Grumpier Old Men (1995),Comedy|Romance\n"
        "4,Waiting to Exhale (1995),Comedy|Drama\n"
        "5,Father of the Bride Part II (1995),Comedy\n"
        "6,Movie With Most Genres (1996),Action|Adventure|Animation|Children|Comedy|Crime\n"
    )
    path = tmp_path / "movies.csv"
    path.write_text(content)
    return str(path)


@pytest.fixture
def movies_instance(mock_movies_file):
    return Movies(mock_movies_file)


def test_dist_by_release(movies_instance):
    result = movies_instance.dist_by_release()
    assert isinstance(result, dict)
    assert result["1995"] == 5
    assert result["1996"] == 1


def test_dist_by_genres(movies_instance):
    result = movies_instance.dist_by_genres()
    assert isinstance(result, dict)
    assert result["Comedy"] == 5
    assert result["Fantasy"] == 2
    assert result["Crime"] == 1


def test_most_genres(movies_instance):
    result = movies_instance.most_genres(1)
    assert isinstance(result, dict)
    assert list(result.keys())[0] == "Movie With Most Genres (1996)"
    assert list(result.values())[0] == 6
