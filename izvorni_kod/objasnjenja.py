def objasni_rizik_korisnika(korisnik):
    """
    Pravi jednostavno objasnjenje zasto je korisnik u riziku.

    Umjesto komplikovanog SHAP prikaza, ovdje koristimo jasna poslovna pravila:
    - mjesecni ugovor povecava rizik
    - kratak tenure povecava rizik
    - visoki mjesecni troskovi povecavaju rizik
    - nedostatak dodatnih usluga moze povecati rizik
    """

    razlozi = []

    if korisnik["Contract"] == "Month-to-month":
        razlozi.append(
            "Korisnik ima mjesečni ugovor, što obično povećava mogućnost odlaska."
        )

    if korisnik["tenure"] <= 12:
        razlozi.append(
            "Korisnik je relativno nov, jer koristi usluge manje od godinu dana."
        )

    if korisnik["MonthlyCharges"] >= 80:
        razlozi.append(
            "Korisnik ima visoke mjesečne troškove, što može povećati nezadovoljstvo."
        )

    if korisnik["InternetService"] == "Fiber optic":
        razlozi.append(
            "Korisnik koristi fiber optic internet, grupa koja često ima veći churn rizik u ovom datasetu."
        )

    if korisnik["OnlineSecurity"] == "No":
        razlozi.append(
            "Korisnik nema Online Security dodatnu uslugu."
        )

    if korisnik["TechSupport"] == "No":
        razlozi.append(
            "Korisnik nema Tech Support uslugu, što može smanjiti vezanost za kompaniju."
        )

    if korisnik["PaymentMethod"] == "Electronic check":
        razlozi.append(
            "Korisnik plaća elektronskim čekom, što se često povezuje sa većim churn rizikom."
        )

    if len(razlozi) == 0:
        razlozi.append(
            "Korisnik nema izražene rizične faktore prema jednostavnoj poslovnoj analizi."
        )

    return razlozi


def napravi_kratko_objasnjenje(korisnik):
    """
    Pravi kratak tekst koji se prikazuje na stranici detalja korisnika.
    """

    rizik = korisnik["churn_percent"]

    if rizik >= 70:
        uvod = "Ovaj korisnik ima visok rizik od napuštanja usluge."
    elif rizik >= 40:
        uvod = "Ovaj korisnik ima srednji rizik od napuštanja usluge."
    else:
        uvod = "Ovaj korisnik trenutno ima nizak rizik od napuštanja usluge."

    razlozi = objasni_rizik_korisnika(korisnik)

    tekst = uvod + " Najvažniji razlozi su: " + " ".join(razlozi[:3])

    return tekst


def predlozi_akciju(korisnik):
    """
    Predlaze retention akciju za korisnika.

    Logika:
    - visok rizik + veliki ocekivani gubitak -> popust 20%
    - visok rizik -> kontakt korisnika i posebna ponuda
    - srednji rizik -> poziv korisnicke podrske
    - nizak rizik -> bez posebne akcije
    """

    rizik = korisnik["churn_probability"]
    ocekivani_gubitak = korisnik["expected_loss"]

    if rizik >= 0.70 and ocekivani_gubitak >= 300:
        return "Ponuditi popust 20% ili poseban loyalty paket."
    elif rizik >= 0.70:
        return "Kontaktirati korisnika i ponuditi individualnu retention ponudu."
    elif rizik >= 0.40:
        return "Poziv korisničke podrške i provjera zadovoljstva korisnika."
    else:
        return "Nije potrebna posebna retention akcija u ovom trenutku."


def napravi_reasoning_za_tabelu(korisnik):
    """
    Pravi kratak reasoning tekst za prikaz u tabeli rizičnih korisnika.
    """

    razlozi = []

    if korisnik["Contract"] == "Month-to-month":
        razlozi.append("mjesečni ugovor")

    if korisnik["tenure"] <= 12:
        razlozi.append("kratak tenure")

    if korisnik["MonthlyCharges"] >= 80:
        razlozi.append("visok mjesečni trošak")

    if korisnik["TechSupport"] == "No":
        razlozi.append("bez tehničke podrške")

    if len(razlozi) == 0:
        return "Nema izraženih pojedinačnih faktora."

    return "Rizik povećava: " + ", ".join(razlozi) + "."


def dodaj_objasnjenja_i_akcije(df_predikcije):
    """
    Dodaje kolone:
    - reasoning
    - recommended_action

    Ove kolone koristimo u web aplikaciji.
    """

    df = df_predikcije.copy()

    df["reasoning"] = df.apply(napravi_reasoning_za_tabelu, axis=1)
    df["recommended_action"] = df.apply(predlozi_akciju, axis=1)

    return df