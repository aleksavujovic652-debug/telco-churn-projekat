import pandas as pd

from izvorni_kod.ucitavanje_podataka import ucitaj_podatke
from izvorni_kod.priprema_podataka import ocisti_podatke, pripremi_podatke_za_prikaz
from izvorni_kod.treniranje_modela import ucitaj_trenirani_model


def odredi_nivo_rizika(churn_probability):
    """
    Na osnovu vjerovatnoce churn-a odredjuje nivo rizika.

    Ovo koristimo da bi aplikacija korisniku prikazala jednostavnu oznaku:
    - Nizak rizik
    - Srednji rizik
    - Visok rizik
    """

    if churn_probability >= 0.70:
        return "Visok rizik"
    elif churn_probability >= 0.40:
        return "Srednji rizik"
    else:
        return "Nizak rizik"


def izracunaj_ocekivani_gubitak(monthly_charges, churn_probability, broj_mjeseci=6):
    """
    Racuna ocekivani finansijski gubitak ako korisnik napusti kompaniju.

    Formula:
    ocekivani_gubitak = mjesecna_naplata * broj_mjeseci * vjerovatnoca_churn_a

    Uzimamo period od 6 mjeseci kao jednostavnu procjenu.
    """

    return monthly_charges * broj_mjeseci * churn_probability


def napravi_predikcije_za_sve_korisnike(df):
    """
    Pravi churn predikcije za sve korisnike iz dataseta.

    Koraci:
    1. ucitava trenirani model
    2. priprema podatke za predikciju
    3. racuna vjerovatnocu churn-a
    4. dodaje nivo rizika
    5. racuna ocekivani gubitak
    6. sortira korisnike po riziku
    """

    model = ucitaj_trenirani_model()

    df_cist = ocisti_podatke(df)

    X = df_cist.drop(columns=["customerID", "Churn"])

    churn_probability = model.predict_proba(X)[:, 1]

    df_rezultat = pripremi_podatke_za_prikaz(df)

    df_rezultat["churn_probability"] = churn_probability

    df_rezultat["churn_percent"] = (
        df_rezultat["churn_probability"] * 100
    ).round(2)

    df_rezultat["risk_level"] = df_rezultat["churn_probability"].apply(
        odredi_nivo_rizika
    )

    df_rezultat["expected_loss"] = df_rezultat.apply(
        lambda red: izracunaj_ocekivani_gubitak(
            red["MonthlyCharges"],
            red["churn_probability"]
        ),
        axis=1
    )

    df_rezultat["expected_loss"] = df_rezultat["expected_loss"].round(2)

    df_rezultat = df_rezultat.sort_values(
        by=["churn_probability", "expected_loss"],
        ascending=False
    )

    return df_rezultat


def pronadji_korisnika(df_predikcije, customer_id):
    """
    Pronalazi jednog korisnika po customerID.

    Koristi se na stranici detalja korisnika.
    """

    korisnik = df_predikcije[df_predikcije["customerID"] == customer_id]

    if korisnik.empty:
        return None

    return korisnik.iloc[0]


def pripremi_tabelu_rizicnih_korisnika(df_predikcije, limit=50):
    """
    Priprema tabelu najrizicnijih korisnika za prikaz u aplikaciji.

    Uzimamo samo najbitnije kolone da tabela bude pregledna.
    """

    kolone = [
        "customerID",
        "churn_percent",
        "risk_level",
        "expected_loss",
        "tenure",
        "Contract",
        "InternetService",
        "MonthlyCharges",
        "TotalCharges"
    ]

    df_tabela = df_predikcije[kolone].head(limit).copy()

    df_tabela = df_tabela.rename(columns={
        "customerID": "Korisnik",
        "churn_percent": "Churn rizik (%)",
        "risk_level": "Nivo rizika",
        "expected_loss": "Ocekivani gubitak",
        "tenure": "Tenure",
        "Contract": "Ugovor",
        "InternetService": "Internet usluga",
        "MonthlyCharges": "Mjesecni trosak",
        "TotalCharges": "Ukupni trosak"
    })

    return df_tabela


def filtriraj_korisnike(
    df_predikcije,
    min_rizik=0,
    ugovor="Svi",
    internet="Svi"
):
    """
    Filtrira korisnike prema uslovima iz web aplikacije.

    min_rizik se unosi kao procenat, npr. 70 znaci rizik >= 70%.
    """

    df = df_predikcije.copy()

    df = df[df["churn_percent"] >= min_rizik]

    if ugovor != "Svi":
        df = df[df["Contract"] == ugovor]

    if internet != "Svi":
        df = df[df["InternetService"] == internet]

    return df


if __name__ == "__main__":
    df, info = ucitaj_podatke()

    df_predikcije = napravi_predikcije_za_sve_korisnike(df)

    print(df_predikcije[[
        "customerID",
        "churn_percent",
        "risk_level",
        "expected_loss"
    ]].head(10))