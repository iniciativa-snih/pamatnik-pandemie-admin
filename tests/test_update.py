def test_index(client):
    from pamatnikpandemie.models import Dead
    from pamatnikpandemie.update import update

    ln = len(Dead.query.order_by(Dead.date_for.desc()).all())
    update()
    assert len(Dead.query.all()) > ln
