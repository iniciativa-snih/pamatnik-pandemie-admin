import json


def test_health(client):
    assert b"Healthy" in client.get("/api/health")


def test_deads(client):
    from pomnicek.models import Dead

    target = json.loads(client.get("api/deads"))
    expected = Dead.query.order_by(Dead.date.desc()).first()

    assert len(target) == len(Dead.query.all())
    assert target[0].date == expected.date
    assert target[0].daily == expected.daily
    assert target[0].cumulative == expected.cumulative


def test_stories(client):
    from pomnicek.models import Story

    target = json.loads(client.get("api/stories"))
    expected = Story.query.order_by(Story.date.desc()).all()

    assert len(target) == len(expected)
    assert target[0].id == expected.id
    assert target[0].name == expected[0].name
    assert target[0].story == expected[0].story
    assert target[0].age == expected[0].age
    assert target[0].city == expected[0].city
