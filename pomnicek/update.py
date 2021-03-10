import pandas as pd

from .database import db_session


def get_deads():
    deads = pd.read_csv(
        "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv",
        parse_dates=["datum"],
        infer_datetime_format=True,
    )
    deads = deads[["datum", "kumulativni_pocet_umrti"]]
    deads.columns = ["date", "cumulative"]
    deads = deads.sort_values("date", ascending=True)
    deads = deads[deads.date >= "2020-03-22"]
    deads["daily"] = deads.cumulative.diff()
    db_session.connection().execute("DELETE FROM dead")
    deads.to_sql("dead", db_session.connection(), if_exists="replace", index=False)
    db_session.commit()


def update():
    get_deads()


if __name__ == "__main__":
    update()
