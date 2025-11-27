import pytest
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from movielens_analysis import Ratings


@pytest.fixture
def mock_ratings_file(tmp_path):
    content = (
        "userId,movieId,rating,timestamp\n"
        "1,10,4.0,964982703\n"
        "1,20,2.0,964982703\n"
        "2,10,5.0,964981247\n"
        "2,30,3.0,964982703\n"
        "3,20,2.0,964982224\n"
        "4,20,2.0,964983815\n"
        "5,30,3.0,964982931\n"
        "6,30,4.0,964983815\n"
        "7,40,1.0,964982400\n"
        "8,40,5.0,964982224\n"
        "9,50,3.0,964982703\n"
        "10,50,3.0,964982224\n"
    )
    path = tmp_path / "ratings.csv"
    path.write_text(content)
    return str(path)


@pytest.fixture
def ratings_movies_instance(mock_ratings_file):
    ratings_df = pd.read_csv(mock_ratings_file)
    return Ratings.Movies(ratings_df)


@pytest.fixture
def ratings_users_instance(mock_ratings_file):
    df = pd.read_csv(mock_ratings_file)
    return Ratings.Users(df)


def test_ratings_constructor(mock_ratings_file):
    r = Ratings(mock_ratings_file)
    assert isinstance(r.data, pd.DataFrame)
    assert "rating" in r.data.columns


def test_dist_by_year(ratings_movies_instance):
    result = ratings_movies_instance.dist_by_year()
    assert isinstance(result, dict)
    assert all(isinstance(k, int) for k in result)


def test_dist_by_rating(ratings_movies_instance):
    result = ratings_movies_instance.dist_by_rating()
    assert isinstance(result, dict)
    assert result[1.0] == 1
    assert result[5.0] == 2


def test_top_by_num_of_ratings(ratings_movies_instance):
    result = ratings_movies_instance.top_by_num_of_ratings(2)
    assert isinstance(result, dict)
    assert len(result) == 2


def test_top_by_ratings_average(ratings_movies_instance):
    result = ratings_movies_instance.top_by_ratings(2, metric="average")
    assert isinstance(result, dict)
    assert len(result) == 2


def test_top_by_ratings_median(ratings_movies_instance):
    result = ratings_movies_instance.top_by_ratings(2, metric="median")
    assert len(result) == 2


def test_top_by_ratings_invalid_metric(ratings_movies_instance):
    with pytest.raises(ValueError):
        ratings_movies_instance.top_by_ratings(2, metric="sum")


def test_top_controversial(ratings_movies_instance):
    result = ratings_movies_instance.top_controversial(2)
    assert isinstance(result, dict)
    assert len(result) == 2


def test_dist_by_num_of_ratings_users(ratings_users_instance):
    result = ratings_users_instance.dist_by_num_of_ratings()
    assert isinstance(result, dict)
    assert result[1] == 2


def test_users_rating_average(ratings_users_instance):
    result = ratings_users_instance.dist_by_rating("average")
    assert isinstance(result, dict)
    assert round(result[1], 2) == 3.0


def test_users_rating_median(ratings_users_instance):
    result = ratings_users_instance.dist_by_rating("median")
    assert isinstance(result, dict)
    assert round(result[1], 2) == 3.0


def test_users_rating_invalid_metric(ratings_users_instance):
    with pytest.raises(ValueError):
        ratings_users_instance.dist_by_rating("wrong")


def test_users_top_controversial(ratings_users_instance):
    result = ratings_users_instance.top_controversial(2)
    assert isinstance(result, dict)
    assert len(result) == 2


def test_users_most_active_users(ratings_users_instance):
    result = ratings_users_instance.most_active_users(3)
    assert isinstance(result, dict)
    assert len(result) == 3
    assert result[1] == 2
    assert all(v > 0 for v in result.values())
