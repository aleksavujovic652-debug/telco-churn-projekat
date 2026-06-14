import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer


def ocisti_podatke(df):
    """
    Radi osnovno ciscenje Telco dataseta.

    Najvaznije:
    - TotalCharges se u datasetu ucita kao tekst, pa ga pretvaramo u broj.
    - Ako postoje prazne vrijednosti u TotalCharges, zamjenjujemo ih nulom.
    - Churn kolonu pretvaramo iz Yes/No u 1/0.
    """

    df_cist = df.copy()

    # TotalCharges zna da ima prazne vrijednosti kao tekst.
    # errors="coerce" znaci: ako nesto ne moze da se pretvori u broj, postavi NaN.
    df_cist["TotalCharges"] = pd.to_numeric(
        df_cist["TotalCharges"],
        errors="coerce"
    )

    # Prazne vrijednosti mijenjamo nulom.
    df_cist["TotalCharges"] = df_cist["TotalCharges"].fillna(0)

    # Ciljna kolona: korisnik je otisao = 1, nije otisao = 0.
    df_cist["Churn"] = df_cist["Churn"].map({
        "Yes": 1,
        "No": 0
    })

    return df_cist


def napravi_feature_kolone(df):
    """
    Pravi listu ulaznih kolona za model.

    Izbacujemo:
    - customerID, jer je to samo identifikator korisnika
    - Churn, jer je to ciljna kolona koju model treba da predvidi
    """

    kolone_za_izbaciti = ["customerID", "Churn"]

    feature_kolone = []

    for kolona in df.columns:
        if kolona not in kolone_za_izbaciti:
            feature_kolone.append(kolona)

    return feature_kolone


def podijeli_kolone_po_tipu(df, feature_kolone):
    """
    Dijeli kolone na numericke i kategorijske.

    Numericke kolone su brojevi, na primjer:
    - tenure
    - MonthlyCharges
    - TotalCharges

    Kategorijske kolone su tekstualne, na primjer:
    - Contract
    - InternetService
    - PaymentMethod
    """

    numericke_kolone = []
    kategorijske_kolone = []

    for kolona in feature_kolone:
        if pd.api.types.is_numeric_dtype(df[kolona]):
            numericke_kolone.append(kolona)
        else:
            kategorijske_kolone.append(kolona)

    return numericke_kolone, kategorijske_kolone


def napravi_preprocessor(numericke_kolone, kategorijske_kolone):
    """
    Pravi preprocessor za model.

    Numericke kolone skaliramo pomocu StandardScaler-a.
    Kategorijske kolone pretvaramo u brojeve pomocu OneHotEncoder-a.

    Ovo je potrebno jer ML modeli ne mogu direktno raditi sa tekstom.
    """

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numericke_kolone),
            ("cat", OneHotEncoder(handle_unknown="ignore"), kategorijske_kolone)
        ]
    )

    return preprocessor


def pripremi_podatke_za_model(df):
    """
    Glavna funkcija za pripremu podataka.

    Koraci:
    1. cisti podatke
    2. odvaja X i y
    3. dijeli podatke na train i test skup
    4. pravi preprocessor za numericke i kategorijske kolone

    Vraca sve sto je potrebno za treniranje modela.
    """

    df_cist = ocisti_podatke(df)

    feature_kolone = napravi_feature_kolone(df_cist)

    X = df_cist[feature_kolone]
    y = df_cist["Churn"]

    numericke_kolone, kategorijske_kolone = podijeli_kolone_po_tipu(
        df_cist,
        feature_kolone
    )

    preprocessor = napravi_preprocessor(
        numericke_kolone,
        kategorijske_kolone
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    return {
        "df_cist": df_cist,
        "X": X,
        "y": y,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "feature_kolone": feature_kolone,
        "numericke_kolone": numericke_kolone,
        "kategorijske_kolone": kategorijske_kolone,
        "preprocessor": preprocessor
    }


def pripremi_podatke_za_prikaz(df):
    """
    Priprema dodatne kolone koje ce nam koristiti u web aplikaciji.

    Dodajemo:
    - TotalCharges kao broj
    - ChurnLabel kao tekst
    """

    df_prikaz = df.copy()

    df_prikaz["TotalCharges"] = pd.to_numeric(
        df_prikaz["TotalCharges"],
        errors="coerce"
    )

    df_prikaz["TotalCharges"] = df_prikaz["TotalCharges"].fillna(0)

    if "Churn" in df_prikaz.columns:
        df_prikaz["ChurnLabel"] = df_prikaz["Churn"]

    return df_prikaz