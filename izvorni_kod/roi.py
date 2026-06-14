def izracunaj_trosak_akcije(korisnik):
    """
    Racuna procijenjeni trosak retention akcije.

    Ideja:
    - ako nudimo popust 20%, trosak racunamo kao 20% mjesecne pretplate tokom 3 mjeseca
    - ako je u pitanju poziv korisnicke podrske, trosak je manji i fiksan
    - ako nema akcije, trosak je 0
    """

    akcija = korisnik["recommended_action"]
    mjesecni_trosak = korisnik["MonthlyCharges"]

    if "popust 20%" in akcija or "loyalty paket" in akcija:
        return mjesecni_trosak * 0.20 * 3

    if "Kontaktirati korisnika" in akcija:
        return 15

    if "Poziv korisničke podrške" in akcija:
        return 8

    return 0


def izracunaj_ocekivanu_korist(korisnik):
    """
    Racuna ocekivanu korist od retention akcije.

    Pretpostavka:
    retention akcija nece uvijek uspjeti.
    Zato koristimo jednostavnu procjenu uspjesnosti:
    - za visok rizik: 35%
    - za srednji rizik: 20%
    - za nizak rizik: 5%

    Ocekivana korist = ocekivani gubitak * vjerovatnoca uspjeha akcije
    """

    rizik = korisnik["churn_probability"]
    ocekivani_gubitak = korisnik["expected_loss"]

    if rizik >= 0.70:
        stopa_uspjeha = 0.35
    elif rizik >= 0.40:
        stopa_uspjeha = 0.20
    else:
        stopa_uspjeha = 0.05

    return ocekivani_gubitak * stopa_uspjeha


def izracunaj_roi(korisnik):
    """
    Racuna ROI retention akcije.

    Formula:
    ROI = (ocekivana_korist - trosak_akcije) / trosak_akcije

    Ako je trosak akcije 0, ROI postavljamo na 0 da ne bi doslo do dijeljenja nulom.
    """

    trosak_akcije = izracunaj_trosak_akcije(korisnik)
    ocekivana_korist = izracunaj_ocekivanu_korist(korisnik)

    if trosak_akcije == 0:
        return 0

    roi = (ocekivana_korist - trosak_akcije) / trosak_akcije

    return roi


def dodaj_roi_kolone(df_korisnici):
    """
    Dodaje ROI kolone u tabelu korisnika.

    Dodajemo:
    - action_cost
    - expected_benefit
    - retention_roi
    """

    df = df_korisnici.copy()

    df["action_cost"] = df.apply(izracunaj_trosak_akcije, axis=1)
    df["expected_benefit"] = df.apply(izracunaj_ocekivanu_korist, axis=1)
    df["retention_roi"] = df.apply(izracunaj_roi, axis=1)

    df["action_cost"] = df["action_cost"].round(2)
    df["expected_benefit"] = df["expected_benefit"].round(2)
    df["retention_roi"] = df["retention_roi"].round(2)

    return df


def napravi_roi_summary(df_korisnici):
    """
    Pravi kratak summary ROI kampanje.

    Koristi se na dashboard-u.
    """

    if df_korisnici.empty:
        return {
            "broj_korisnika": 0,
            "ukupni_ocekivani_gubitak": 0,
            "ukupni_trosak_akcija": 0,
            "ukupna_ocekivana_korist": 0,
            "neto_korist": 0,
            "prosjek_roi": 0
        }

    ukupni_ocekivani_gubitak = df_korisnici["expected_loss"].sum()
    ukupni_trosak_akcija = df_korisnici["action_cost"].sum()
    ukupna_ocekivana_korist = df_korisnici["expected_benefit"].sum()
    neto_korist = ukupna_ocekivana_korist - ukupni_trosak_akcija

    if "retention_roi" in df_korisnici.columns:
        prosjek_roi = df_korisnici["retention_roi"].mean()
    else:
        prosjek_roi = 0

    summary = {
        "broj_korisnika": len(df_korisnici),
        "ukupni_ocekivani_gubitak": round(ukupni_ocekivani_gubitak, 2),
        "ukupni_trosak_akcija": round(ukupni_trosak_akcija, 2),
        "ukupna_ocekivana_korist": round(ukupna_ocekivana_korist, 2),
        "neto_korist": round(neto_korist, 2),
        "prosjek_roi": round(prosjek_roi, 2)
    }

    return summary