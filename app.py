from flask import Flask, render_template, request, redirect, url_for
import joblib

from izvorni_kod.ucitavanje_podataka import ucitaj_podatke
from izvorni_kod.predikcija import (
    napravi_predikcije_za_sve_korisnike,
    pripremi_tabelu_rizicnih_korisnika,
    filtriraj_korisnike,
    pronadji_korisnika
)
from izvorni_kod.objasnjenja import (
    dodaj_objasnjenja_i_akcije,
    objasni_rizik_korisnika,
    napravi_kratko_objasnjenje,
    predlozi_akciju
)
from izvorni_kod.roi import dodaj_roi_kolone, napravi_roi_summary


app = Flask(__name__)


def pripremi_sve_podatke():
    """
    Ova funkcija ucitava dataset i pravi sve potrebne rezultate za aplikaciju.

    Koraci:
    1. ucitava Telco dataset
    2. pravi churn predikcije za sve korisnike
    3. dodaje objasnjenja i preporucene akcije
    4. dodaje ROI kolone
    """

    df, info = ucitaj_podatke()

    df_predikcije = napravi_predikcije_za_sve_korisnike(df)

    df_predikcije = dodaj_objasnjenja_i_akcije(df_predikcije)

    df_predikcije = dodaj_roi_kolone(df_predikcije)

    return df, info, df_predikcije


def formatiraj_broj(vrijednost):
    """
    Pomocna funkcija za prikaz brojeva u HTML-u.
    """

    try:
        return round(float(vrijednost), 2)
    except Exception:
        return vrijednost


@app.route("/")
def index():
    """
    Pocetna stranica aplikacije.
    """

    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """
    Dashboard stranica.

    Prikazuje:
    - broj korisnika
    - broj churn korisnika
    - churn rate
    - ROI summary
    - osnovne poslovne indikatore
    """

    df, info, df_predikcije = pripremi_sve_podatke()

    top_rizicni = df_predikcije.head(10)

    roi_summary = napravi_roi_summary(df_predikcije.head(100))

    prosjecni_mjesecni_trosak = df_predikcije["MonthlyCharges"].mean()
    prosjecni_tenure = df_predikcije["tenure"].mean()

    broj_visok_rizik = len(df_predikcije[df_predikcije["risk_level"] == "Visok rizik"])
    broj_srednji_rizik = len(df_predikcije[df_predikcije["risk_level"] == "Srednji rizik"])
    broj_nizak_rizik = len(df_predikcije[df_predikcije["risk_level"] == "Nizak rizik"])

    return render_template(
        "dashboard.html",
        info=info,
        top_rizicni=top_rizicni.to_dict(orient="records"),
        roi_summary=roi_summary,
        prosjecni_mjesecni_trosak=formatiraj_broj(prosjecni_mjesecni_trosak),
        prosjecni_tenure=formatiraj_broj(prosjecni_tenure),
        broj_visok_rizik=broj_visok_rizik,
        broj_srednji_rizik=broj_srednji_rizik,
        broj_nizak_rizik=broj_nizak_rizik
    )


@app.route("/korisnici")
def korisnici():
    """
    Stranica sa rangiranom listom rizicnih korisnika.

    Omogucava filtere:
    - minimalni churn rizik
    - tip ugovora
    - internet usluga
    """

    df, info, df_predikcije = pripremi_sve_podatke()

    min_rizik = request.args.get("min_rizik", default=70, type=float)
    ugovor = request.args.get("ugovor", default="Svi")
    internet = request.args.get("internet", default="Svi")
    limit = request.args.get("limit", default=50, type=int)

    df_filtrirano = filtriraj_korisnike(
        df_predikcije,
        min_rizik=min_rizik,
        ugovor=ugovor,
        internet=internet
    )

    df_tabela = df_filtrirano.head(limit).copy()

    ugovori = ["Svi"] + sorted(df_predikcije["Contract"].dropna().unique().tolist())
    internet_usluge = ["Svi"] + sorted(df_predikcije["InternetService"].dropna().unique().tolist())

    return render_template(
        "korisnici.html",
        korisnici=df_tabela.to_dict(orient="records"),
        min_rizik=min_rizik,
        ugovor=ugovor,
        internet=internet,
        limit=limit,
        ugovori=ugovori,
        internet_usluge=internet_usluge,
        broj_rezultata=len(df_filtrirano)
    )


@app.route("/korisnik/<customer_id>")
def detalji_korisnika(customer_id):
    """
    Stranica sa detaljima jednog korisnika.

    Prikazuje:
    - churn vjerovatnocu
    - nivo rizika
    - ocekivani gubitak
    - razloge rizika
    - predlozenu akciju
    - ROI informacije
    """

    df, info, df_predikcije = pripremi_sve_podatke()

    korisnik = pronadji_korisnika(df_predikcije, customer_id)

    if korisnik is None:
        return render_template(
            "detalji_korisnika.html",
            korisnik=None,
            razlozi=[],
            kratko_objasnjenje="Korisnik nije pronadjen.",
            akcija="Nema akcije."
        )

    razlozi = objasni_rizik_korisnika(korisnik)
    kratko_objasnjenje = napravi_kratko_objasnjenje(korisnik)
    akcija = predlozi_akciju(korisnik)

    return render_template(
        "detalji_korisnika.html",
        korisnik=korisnik.to_dict(),
        razlozi=razlozi,
        kratko_objasnjenje=kratko_objasnjenje,
        akcija=akcija
    )


@app.route("/o-projektu")
def o_projektu():
    """
    Kratka informativna stranica o projektu.
    """

    return render_template("o_projektu.html")


if __name__ == "__main__":
    app.run(debug=True)