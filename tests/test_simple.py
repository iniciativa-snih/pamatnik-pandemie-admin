def test_index(client):
    response = client.get("/hello")
    assert response.data == b"Hello, world"


def test_index2(client):
    response = client.get("/hello")
    assert response.data == b"Hello, world"
