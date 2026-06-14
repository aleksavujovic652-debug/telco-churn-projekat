import os
import pandas as pd


def ucitaj_telco_podatke(putanja="podaci/Telco-Customer-Churn.csv"):
    """
    Ucitava Telco Customer Churn dataset iz CSV fajla.

    Ova funkcija radi samo ucitavanje i osnovnu provjeru podataka.
    Detaljna priprema podataka za model radi se u fajlu priprema_podataka.py.

    Ocekivani fajl:
    podaci/Telco-Customer-Churn.csv
    """

    if not os.path.exists(putanja):
        raise FileNotFoundError(
            "CSV fajl nije pronadjen. Provjeri da li se fajl nalazi u folderu podaci "
            "i da li se zove Telco-Customer-Churn.csv."
        )

    df = pd.read_csv(putanja)

    if df.empty:
        raise ValueError("CSV fajl je prazan.")

    return df


def prikazi_osnovne_informacije(df):
    """
    Vraca osnovne informacije o datasetu.

    Koristi se za dashboard i za brzu provjeru:
    - broj redova
    - broj kolona
    - broj korisnika koji su otisli
    - broj korisnika koji su ostali
    - churn rate
    """

    broj_korisnika = len(df)
    broj_kolona = len(df.columns)

    if "Churn" in df.columns:
        broj_churn_yes = len(df[df["Churn"] == "Yes"])
        broj_churn_no = len(df[df["Churn"] == "No"])

        if broj_korisnika > 0:
            churn_rate = broj_churn_yes / broj_korisnika
        else:
            churn_rate = 0
    else:
        broj_churn_yes = 0
        broj_churn_no = 0
        churn_rate = 0

    informacije = {
        "broj_korisnika": broj_korisnika,
        "broj_kolona": broj_kolona,
        "broj_churn_yes": broj_churn_yes,
        "broj_churn_no": broj_churn_no,
        "churn_rate": churn_rate
    }

    return informacije


def ucitaj_podatke():
    """
    Glavna funkcija koju ce koristiti aplikacija.

    Ona ucitava dataset i vraca:
    - dataframe sa podacima
    - osnovne informacije o podacima
    """

    df = ucitaj_telco_podatke()
    informacije = prikazi_osnovne_informacije(df)

    return df, informacije