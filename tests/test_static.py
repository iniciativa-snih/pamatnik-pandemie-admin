from gazpacho import Soup


def test_index(client):
    soup = Soup(client.get("/").data.decode("utf8"))

    assert soup.find("p", {"class": "count vaccine-deaths"}).text == "0"
