import pytest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from links import Links


class TestLinks:
    @pytest.fixture
    def mock_links_file(self, tmp_path):
        path = tmp_path / "links.csv"
        content = "movieId,imdbId\n1,0114709\n2,0113497\n"
        path.write_text(content)
        return str(path)

    @pytest.fixture
    def links_instance(self, mock_links_file):
        return Links(mock_links_file)

    def test_get_imdb_id(self, links_instance):
        assert links_instance._Links__get_imdb_id(1) == "0114709"
        assert links_instance._Links__get_imdb_id(999) is None

    def test_links_data_loaded(self, links_instance):
        assert isinstance(links_instance.links_data, list)
        assert len(links_instance.links_data) == 2
        assert links_instance.links_data[0]["movieId"] == "1"

    # INIT
    def test_init_and_load_links_valid(self, tmp_path):
        csv_path = tmp_path / "links.csv"
        csv_path.write_text("movieId,imdbId\n1,tt1234567\n2,tt7654321\n")

        links = Links(str(csv_path))

        assert links.path == str(csv_path)
        assert isinstance(links.links_data, list)
        assert len(links.links_data) == 2
        assert links.links_data[0]["movieId"] == "1"

    @patch("builtins.open", side_effect=FileNotFoundError("File missing"))
    def test_load_links_file_not_found(self, mock_open):
        links = Links("fake/path/links.csv")

        assert links.links_data is None or links.links_data == []

    # END

    # __GET_IMDB
    @patch("movielens_analysis.Links._Links__get_soup")
    @patch("movielens_analysis.Links._Links__extract_field")
    def test_get_imdb(self, mock_extract_field, mock_get_soup, links_instance):
        mock_get_soup.return_value = MagicMock()
        mock_extract_field.side_effect = [
            "DirectorName",
            "$1000000",
            "$1500000",
            "1:30",
        ]

        result = links_instance.get_imdb(
            [1], ["Director", "Budget", "Cumulative Worldwide Gross", "Runtime"]
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0][0] == 1
        assert result[0][1] == "DirectorName"

    @patch("movielens_analysis.Links._Links__get_imdb_id")
    @patch("movielens_analysis.Links._Links__get_soup")
    @patch("movielens_analysis.Links._Links__extract_field")
    def test_get_imdb_soup_none(
        self, mock_extract_field, mock_get_soup, mock_get_imdb_id, links_instance
    ):
        mock_get_imdb_id.side_effect = lambda movie_id: {
            1: "0114709",
            2: "1234567",
        }.get(movie_id, None)

        soup_mock = MagicMock()
        mock_get_soup.side_effect = lambda imdb_id: (
            soup_mock if imdb_id == "0114709" else None
        )
        mock_extract_field.side_effect = [
            "Director One",
            "$1000000",
            "$1500000",
            "1:30",
        ]

        result = links_instance.get_imdb(
            movie_ids=[1, 2],
            list_of_fields=[
                "Director",
                "Budget",
                "Cumulative Worldwide Gross",
                "Runtime",
            ],
        )

        assert len(result) == 1
        assert result[0][0] == 1
        assert result[0][1:] == ["Director One", "$1000000", "$1500000", "1:30"]

    # END
    # MOST_EXPENSIVE

    @patch("movielens_analysis.Links._Links__get_soup")
    @patch("movielens_analysis.Links._Links__extract_field")
    def test_most_expensive(self, mock_extract_field, mock_get_soup, links_instance):
        mock_soup = MagicMock()
        mock_soup.find.return_value.text.strip.return_value = "Movie Title"
        mock_get_soup.return_value = mock_soup
        mock_extract_field.return_value = "$150,000,000"

        result = links_instance.most_expensive(1)
        assert isinstance(result, dict)
        assert "Movie Title" in result
        assert result["Movie Title"] == "$150,000,000"

    @patch("movielens_analysis.Links._Links__get_soup")
    @patch("movielens_analysis.Links._Links__extract_field")
    def test_most_expensive_all_continues(self, mock_extract_field, mock_get_soup):
        from movielens_analysis import Links

        links = Links.__new__(Links)
        links.links_data = [
            {"imdbId": "tt_null_soup"},
            {"imdbId": "tt_no_budget"},
            {"imdbId": "tt_no_digits"},
            {"imdbId": "tt_valid"},
        ]

        soups = {}

        for imdb_id in ["tt_no_budget", "tt_no_digits", "tt_valid"]:
            soup = MagicMock()
            h1 = MagicMock()
            h1.text.strip.return_value = "Mock Movie"
            soup.find.return_value = h1
            soups[imdb_id] = soup

        def get_soup_side_effect(imdb_id):
            if imdb_id == "tt_null_soup":
                return None
            return soups.get(imdb_id)

        mock_get_soup.side_effect = get_soup_side_effect

        def extract_field_side_effect(soup, label):
            if soup == soups["tt_no_budget"]:
                return None
            elif soup == soups["tt_no_digits"]:
                return "$ABC"
            elif soup == soups["tt_valid"]:
                return "$123,456,789"
            return None

        mock_extract_field.side_effect = extract_field_side_effect

        result = links.most_expensive(1)

        assert isinstance(result, dict)
        assert "Mock Movie" in result
        assert result["Mock Movie"] == "$123,456,789"

    # END

    @patch("movielens_analysis.Links._Links__get_soup")
    @patch("movielens_analysis.Links._Links__extract_field")
    def test_most_profitable(self, mock_extract_field, mock_get_soup, links_instance):
        mock_soup = MagicMock()
        mock_soup.find.return_value.text.strip.return_value = "Movie Title"
        mock_get_soup.return_value = mock_soup

        def extract_field_side_effect(soup, field):
            if field == "Budget":
                return "$1000000"
            elif field == "Cumulative Worldwide Gross":
                return "$5000000"
            return None

        mock_extract_field.side_effect = extract_field_side_effect

        result = links_instance.most_profitable(1)
        assert isinstance(result, dict)
        assert "Movie Title" in result
        assert result["Movie Title"] == 4000000

    @patch("movielens_analysis.Links._Links__get_soup")
    @patch("movielens_analysis.Links._Links__extract_field")
    def test_longest(self, mock_extract_field, mock_get_soup, links_instance):
        mock_soup = MagicMock()
        mock_soup.find.return_value.text.strip.return_value = "Movie Title"
        mock_get_soup.return_value = mock_soup
        mock_extract_field.return_value = "2:10"

        result = links_instance.longest(1)
        assert isinstance(result, dict)
        assert "Movie Title" in result
        assert result["Movie Title"] == 130

    # TOP_COST_PER_MINUTE

    @patch("movielens_analysis.Links._Links__get_soup")
    @patch("movielens_analysis.Links._Links__extract_field")
    def test_top_cost_per_minute(
        self, mock_extract_field, mock_get_soup, links_instance
    ):
        mock_soup = MagicMock()
        mock_soup.find.return_value.text.strip.return_value = "Movie Title"
        mock_get_soup.return_value = mock_soup

        def extract_field_side_effect(soup, field):
            if field == "Budget":
                return "$120000"
            elif field == "Runtime":
                return "2:00"
            return None

        mock_extract_field.side_effect = extract_field_side_effect

        result = links_instance.top_cost_per_minute(1)
        assert isinstance(result, dict)
        assert "Movie Title" in result
        assert result["Movie Title"] == 1000.0

    @patch("movielens_analysis.Links._Links__get_soup")
    @patch("movielens_analysis.Links._Links__extract_field")
    def test_top_cost_per_minute_with_exception(
        self, mock_extract_field, mock_get_soup, links_instance
    ):
        links_instance.links_data = [
            {"imdbId": "tt_valid"},
            {"imdbId": "tt_broken"},
        ]

        # Моки
        def get_soup_side_effect(imdb_id):
            soup = MagicMock()
            h1 = MagicMock()
            h1.text.strip.return_value = (
                "Movie Title" if imdb_id == "tt_valid" else "Broken Movie"
            )
            soup.find.return_value = h1
            return soup

        mock_get_soup.side_effect = get_soup_side_effect

        def extract_field_side_effect(soup, field):
            title = soup.find("h1").text.strip()
            if title == "Movie Title":
                return "$120000" if field == "Budget" else "2:00"
            elif title == "Broken Movie":
                return "$99999" if field == "Budget" else "oops"
            return None

        mock_extract_field.side_effect = extract_field_side_effect

        result = links_instance.top_cost_per_minute(1)

        assert isinstance(result, dict)
        assert "Movie Title" in result
        assert result["Movie Title"] == 1000.0
        assert "Broken Movie" not in result

    # END
    # TOP_DIRECTORS

    @patch("movielens_analysis.Links._Links__get_soup")
    def test_top_directors(self, mock_get_soup, links_instance):
        movie_soup = MagicMock()
        director_tag = MagicMock()
        director_tag.text.strip.return_value = "Director One"
        director_tag.get.return_value = "/name/nm1234567/"

        credit_block = MagicMock()
        credit_block.find.return_value = director_tag
        movie_soup.find.side_effect = lambda tag, attrs=None: (
            credit_block
            if attrs and attrs.get("data-testid") == "title-pc-principal-credit"
            else MagicMock()
        )

        director_soup = MagicMock()
        button_mock = MagicMock()
        count_span = MagicMock()
        count_span.text.strip.return_value = "42"
        button_mock.find.return_value = count_span
        director_soup.find.side_effect = lambda tag, attrs=None: (
            button_mock
            if tag == "button"
            and attrs
            and attrs.get("id") == "name-filmography-filter-director"
            else MagicMock()
        )

        def get_soup_side_effect(imdb_id):
            if "nm" in imdb_id:
                return director_soup
            return movie_soup

        mock_get_soup.side_effect = get_soup_side_effect

        result = links_instance.top_directors(1)
        assert isinstance(result, dict)
        assert "Director One" in result
        assert result["Director One"] == 42

    @patch("movielens_analysis.Links._Links__get_soup")
    def test_top_directors_all_continues(self, mock_get_soup, tmp_path):
        csv_data = (
            "movieId,imdbId\n"
            "1,\n"
            "2,tt1234567\n"
            "3,tt9999999\n"
            "4,tt0000001\n"
            "5,tt0000002\n"
            "6,nm0000003\n"
            "7,tt0000003\n"
            "8,nm0000001\n"
            "9,nm0000002\n"
            "10,nm0000004\n"  # director_soup is None
            "11,nm0000005\n"  # Exception continue
        )
        csv_path = tmp_path / "links.csv"
        csv_path.write_text(csv_data)

        links = Links(str(csv_path))

        def get_soup_side_effect(imdb_id):
            if imdb_id == "tt1234567":
                return None

            elif imdb_id == "tt9999999":
                soup = MagicMock()
                soup.find.return_value = None
                return soup

            elif imdb_id == "tt0000001":
                soup = MagicMock()
                credit_block = MagicMock()
                credit_block.find.return_value = None
                soup.find.return_value = credit_block
                return soup

            elif imdb_id == "tt0000002":
                soup = MagicMock()
                director_tag = MagicMock()
                director_tag.text.strip.return_value = "Director"
                director_tag.get.return_value = None
                credit_block = MagicMock()
                credit_block.find.return_value = director_tag
                soup.find.return_value = credit_block
                return soup

            elif imdb_id == "tt0000003":
                soup = MagicMock()
                director_tag = MagicMock()
                director_tag.text.strip.return_value = "Repeat Director"
                director_tag.get.return_value = "/name/nm_repeat/"
                credit_block = MagicMock()
                credit_block.find.return_value = director_tag
                soup.find.return_value = credit_block
                links._Links__processed_urls = {"name/nm_repeat"}
                return soup

            elif imdb_id == "nm0000001":
                return None

            elif imdb_id == "nm0000002":
                if not hasattr(links, "_exception_triggered"):
                    links._exception_triggered = True
                    soup = MagicMock()
                    director_tag = MagicMock()
                    director_tag.text.strip.return_value = "Throws Exception"
                    director_tag.get.return_value = "/name/nm_throw/"
                    credit_block = MagicMock()
                    credit_block.find.return_value = director_tag
                    soup.find.return_value = credit_block
                    return soup
                else:
                    soup = MagicMock()
                    soup.find.side_effect = Exception("Oops")
                    return soup

            elif imdb_id.endswith("nm0000004"):
                if not hasattr(links, "_nm0000004_passed"):
                    links._nm0000004_passed = True
                    soup = MagicMock()
                    director_tag = MagicMock()
                    director_tag.text.strip.return_value = "Director NoneSoup"
                    director_tag.get.return_value = "/name/nm0000004/"
                    credit_block = MagicMock()
                    credit_block.find.return_value = director_tag
                    soup.find.return_value = credit_block
                    return soup
                else:
                    return None

            elif imdb_id.endswith("nm0000005"):
                if not hasattr(links, "_nm0000005_first"):
                    links._nm0000005_first = True
                    soup = MagicMock()
                    director_tag = MagicMock()
                    director_tag.text.strip.return_value = "Director ExceptionInTry"
                    director_tag.get.return_value = "/name/nm0000005/"
                    credit_block = MagicMock()
                    credit_block.find.return_value = director_tag
                    soup.find.return_value = credit_block
                    return soup
                else:
                    soup = MagicMock()
                    soup.find.side_effect = Exception("Boom in try block")
                    return soup

            elif imdb_id == "nm0000003":
                if not hasattr(links, "_valid_called"):
                    links._valid_called = True
                    soup = MagicMock()
                    director_tag = MagicMock()
                    director_tag.text.strip.return_value = "Valid Director"
                    director_tag.get.return_value = "/name/nm0000003/"
                    credit_block = MagicMock()
                    credit_block.find.return_value = director_tag
                    soup.find.return_value = credit_block
                    return soup

                else:
                    soup = MagicMock()
                    btn = MagicMock()
                    count = MagicMock()
                    count.text.strip.return_value = "13"
                    btn.find.return_value = count

                    fallback = MagicMock()
                    fallback.get.return_value = "/name/nm0000003/"

                    soup.find.side_effect = lambda tag, attrs=None: (
                        btn if tag == "button" else fallback
                    )
                    return soup

            return MagicMock()

        mock_get_soup.side_effect = get_soup_side_effect

        result = links.top_directors(1)

        assert isinstance(result, dict)
        assert result == {"Valid Director": 1}

    # END
    # __GET_IMDB_ID

    def test__get_imdb_id_valid(self, links_instance):
        result = links_instance._Links__get_imdb_id(1)
        assert result == "0114709"

    def test__get_imdb_id_invalid(self, links_instance):
        result = links_instance._Links__get_imdb_id(999)
        assert result is None

    def test__get_imdb_id_handles_invalid_rows(self, tmp_path):
        csv_data = "movieId,imdbId\nBAD_ID,tt1234567\n1,tt7654321\n"
        csv_path = tmp_path / "links.csv"
        csv_path.write_text(csv_data)

        links = Links(str(csv_path))

        assert links._Links__get_imdb_id(1) == "tt7654321"
        assert links._Links__get_imdb_id(999) is None

    # END
    # __EXTRACT_FIELD

    @patch("movielens_analysis.Links._Links__get_director")
    @patch("movielens_analysis.Links._Links__get_budget")
    @patch("movielens_analysis.Links._Links__get_gross")
    @patch("movielens_analysis.Links._Links__get_runtime")
    def test__extract_field(
        self, mock_runtime, mock_gross, mock_budget, mock_director, links_instance
    ):
        soup = MagicMock()

        mock_director.return_value = "Quentin Tarantino"
        mock_budget.return_value = "$100,000,000"
        mock_gross.return_value = "$500,000,000"
        mock_runtime.return_value = "2:30"

        assert (
            links_instance._Links__extract_field(soup, "Director")
            == "Quentin Tarantino"
        )
        assert links_instance._Links__extract_field(soup, "Budget") == "$100,000,000"
        assert (
            links_instance._Links__extract_field(soup, "Cumulative Worldwide Gross")
            == "$500,000,000"
        )
        assert links_instance._Links__extract_field(soup, "Runtime") == "2:30"

        assert links_instance._Links__extract_field(soup, "UnknownField") is None

    # END
    # __GET_DIRECTOR_VALID

    def test__get_director_valid(self, links_instance):
        soup = MagicMock()
        director_tag = MagicMock()
        director_tag.text.strip.return_value = "Christopher Nolan"
        credit_block = MagicMock()
        credit_block.find.return_value = director_tag
        soup.find.return_value = credit_block

        result = links_instance._Links__get_director(soup)
        assert result == "Christopher Nolan"

    def test__get_director_missing(self, links_instance):
        soup = MagicMock()
        soup.find.return_value = None
        result = links_instance._Links__get_director(soup)
        assert result is None

    # __GET_BUDGET

    def test__get_budget_valid(self, links_instance):
        soup = MagicMock()
        span = MagicMock()
        span.text.strip.return_value = "$250,000,000"
        boxoffice = MagicMock()
        boxoffice.find.return_value = span
        soup.find.return_value = boxoffice

        result = links_instance._Links__get_budget(soup)
        assert result == "$250,000,000"

    def test__get_budget_attribute_error(self, links_instance):
        soup = MagicMock()
        soup.find.side_effect = AttributeError("unexpected structure")

        result = links_instance._Links__get_budget(soup)
        assert result is None

    # END
    # __GET_GROSS
    def test__get_gross_valid(self, links_instance):
        soup = MagicMock()
        span = MagicMock()
        span.text.strip.return_value = "$1,000,000,000"
        boxoffice = MagicMock()
        boxoffice.find.return_value = span
        soup.find.return_value = boxoffice

        result = links_instance._Links__get_gross(soup)
        assert result == "$1,000,000,000"

    def test__get_gross_attribute_error(self, links_instance):
        soup = MagicMock()
        soup.find.side_effect = AttributeError("bad structure")

        result = links_instance._Links__get_gross(soup)
        assert result is None

    # END

    # __GET_RUNTIME

    def test__get_runtime_valid(self, links_instance):
        soup = MagicMock()
        span = MagicMock()
        span.text.strip.return_value = "2:15"
        soup.find.return_value = span

        result = links_instance._Links__get_runtime(soup)
        assert result == "2:15"

    def test__get_runtime_attribute_error(self, links_instance):
        soup = MagicMock()
        soup.find.side_effect = AttributeError("runtime span missing")

        result = links_instance._Links__get_runtime(soup)
        assert result is None

    # END

    def test__get_director_attribute_error(self, links_instance):
        soup = MagicMock()
        soup.find.side_effect = AttributeError("broken structure")

        result = links_instance._Links__get_director(soup)
        assert result is None

    # END
    # __GET_SOUP

    @pytest.fixture
    def instance(self, tmp_path):
        file = tmp_path / "links.csv"
        file.write_text("movieId,imdbId\n1,0114709\n")
        return Links(str(file))

    def test__get_soup_none_input(self, instance):
        result = instance._Links__get_soup(None)
        assert result is None

        result = instance._Links__get_soup(123)
        assert result is None

    @patch("movielens_analysis.requests.get")
    def test__get_soup_digit_id(self, mock_get, instance):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head></head><body>Test</body></html>"
        mock_get.return_value = mock_response

        result = instance._Links__get_soup("1234567")
        mock_get.assert_called_once()
        assert isinstance(result, BeautifulSoup)
        assert "Test" in result.text

    @patch("movielens_analysis.requests.get")
    def test__get_soup_prefixed_tt(self, mock_get, instance):
        mock_get.return_value = MagicMock(status_code=200, text="<html>tt test</html>")
        result = instance._Links__get_soup("tt1234567")
        assert "tt test" in result.text

    @patch("movielens_analysis.requests.get")
    def test__get_soup_prefixed_nm(self, mock_get, instance):
        mock_get.return_value = MagicMock(status_code=200, text="<html>nm test</html>")
        result = instance._Links__get_soup("nm1234567")
        assert "nm test" in result.text

    @patch("movielens_analysis.requests.get")
    def test__get_soup_prefixed_name_nm(self, mock_get, instance):
        mock_get.return_value = MagicMock(
            status_code=200, text="<html>name/nm test</html>"
        )
        result = instance._Links__get_soup("name/nm1234567")
        assert "name/nm test" in result.text

    @patch("movielens_analysis.requests.get")
    def test__get_soup_prefixed_title_tt(self, mock_get, instance):
        mock_get.return_value = MagicMock(
            status_code=200, text="<html>title/tt test</html>"
        )
        result = instance._Links__get_soup("title/tt1234567")
        assert "title/tt test" in result.text

    @patch("movielens_analysis.requests.get")
    def test__get_soup_unknown_prefix(self, mock_get, instance):
        mock_get.return_value = MagicMock(
            status_code=200, text="<html>generic test</html>"
        )
        result = instance._Links__get_soup("abc1234567")
        assert "generic test" in result.text

    @patch(
        "movielens_analysis.requests.get",
        side_effect=RequestException("Connection failed"),
    )
    def test__get_soup_request_exception(self, mock_get, instance):
        result = instance._Links__get_soup("tt123s4567")
        assert result is None

    # END
