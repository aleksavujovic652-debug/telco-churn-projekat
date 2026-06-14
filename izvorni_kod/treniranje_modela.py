import os
import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from xgboost import XGBClassifier

from izvorni_kod.ucitavanje_podataka import ucitaj_podatke
from izvorni_kod.priprema_podataka import pripremi_podatke_za_model


def napravi_model():
    """
    Pravi XGBoost model za predikciju churn-a.

    Model predvidja vjerovatnocu da korisnik napusti telekom kompaniju.
    """

    model = XGBClassifier(
        n_estimators=120,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=42
    )

    return model


def izracunaj_metrike(y_test, y_pred, y_proba):
    """
    Racuna osnovne metrike modela.

    Koristimo:
    - accuracy
    - precision
    - recall
    - f1
    - roc_auc
    """

    metrike = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba)
    }

    return metrike


def treniraj_i_sacuvaj_model():
    """
    Glavna funkcija za treniranje modela.

    Koraci:
    1. ucitava podatke
    2. priprema podatke za model
    3. pravi pipeline: preprocessing + XGBoost model
    4. trenira model
    5. racuna metrike
    6. cuva model i metrike u folder modeli
    """

    df, info = ucitaj_podatke()

    podaci = pripremi_podatke_za_model(df)

    X_train = podaci["X_train"]
    X_test = podaci["X_test"]
    y_train = podaci["y_train"]
    y_test = podaci["y_test"]
    preprocessor = podaci["preprocessor"]

    model = napravi_model()

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrike = izracunaj_metrike(y_test, y_pred, y_proba)

    os.makedirs("modeli", exist_ok=True)

    joblib.dump(pipeline, "modeli/churn_model.pkl")
    joblib.dump(metrike, "modeli/metrike.pkl")
    joblib.dump(podaci["feature_kolone"], "modeli/feature_kolone.pkl")
    joblib.dump(podaci["numericke_kolone"], "modeli/numericke_kolone.pkl")
    joblib.dump(podaci["kategorijske_kolone"], "modeli/kategorijske_kolone.pkl")

    print("Model je uspjesno treniran i sacuvan.")
    print("")
    print("Metrike modela:")

    for naziv, vrijednost in metrike.items():
        print(naziv, ":", round(vrijednost, 4))

    return pipeline, metrike


def ucitaj_trenirani_model(putanja_modela="modeli/churn_model.pkl"):
    """
    Ucitava sacuvani model.

    Ako model ne postoji, prvo ga trenira.
    """

    if not os.path.exists(putanja_modela):
        print("Model ne postoji. Pokrecem treniranje modela...")
        treniraj_i_sacuvaj_model()

    model = joblib.load(putanja_modela)

    return model


if __name__ == "__main__":
    treniraj_i_sacuvaj_model()