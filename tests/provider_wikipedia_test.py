import pytest

from provider import wikipedia


@pytest.fixture
def wikipedia_client():
    return wikipedia.Wikipedia()

def test_get_random_article(wikipedia_client: wikipedia.Wikipedia):

    response = wikipedia_client.get_random_article()
    article_path = response.headers.get("location")

    assert response.status_code == 302
    assert article_path.startswith("https://en.wikipedia.org/wiki/")

def test_get_random_article_error(wikipedia_client: wikipedia.Wikipedia):
    wikipedia_client.random_url = "https://en.wikipedia.org/wiki/Special:Rando"

    with pytest.raises(Exception) as _:
        wikipedia_client.get_random_article()


def test_search_articles(wikipedia_client: wikipedia.Wikipedia):
    response = wikipedia_client.search_articles(terms=["Python"], limit=5)
    data = response.json()

    assert response.status_code == 200
    assert len(data.get('pages')) > 0

def test_search_article_titles(wikipedia_client: wikipedia.Wikipedia):
    response = wikipedia_client.search_titles(terms=["Python"], limit=5)
    data = response.json()

    assert response.status_code == 200
    assert len(data.get('pages')) > 0

def test_get_access_token(wikipedia_client: wikipedia.Wikipedia):
    resp = wikipedia_client.get_access_token()
    data = resp.json()

    assert resp.status_code == 200
    assert 'access_token' in data
    assert 'expires_in' in data
    assert data.get('token_type').lower() == 'bearer'
