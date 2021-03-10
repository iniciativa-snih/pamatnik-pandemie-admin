def test_index(client):
    response = client.get("/api/health")
    assert b"Healthy" in response.data
