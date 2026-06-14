# Telco Churn Predictor

## Opis projekta

Ovaj projekat predstavlja Flask web aplikaciju za predikciju churn-a korisnika u telekom kompaniji.

Churn označava situaciju kada korisnik napusti kompaniju ili prestane da koristi njene usluge.

Glavno pitanje projekta je:

**Koji korisnici su u riziku da nas napuste?**

## Cilj projekta

Cilj aplikacije je da na osnovu podataka o korisnicima predvidi vjerovatnoću da će korisnik napustiti kompaniju.

Aplikacija dodatno prikazuje:

- nivo churn rizika
- razloge zašto je korisnik rizičan
- očekivani finansijski gubitak
- preporučenu retention akciju
- ROI retention kampanje

## Dataset

Korišćen je Telco Customer Churn dataset.

Dataset sadrži podatke o korisnicima, kao što su:

- customerID
- gender
- SeniorCitizen
- Partner
- Dependents
- tenure
- PhoneService
- InternetService
- Contract
- PaymentMethod
- MonthlyCharges
- TotalCharges
- Churn

Ciljna kolona je:

```text
Churn

Vrijednosti ciljne kolone su:

Yes - korisnik je napustio kompaniju
No - korisnik nije napustio kompaniju
Korišćene tehnologije
Python
Flask
Pandas
NumPy
Scikit-learn
XGBoost
Joblib
HTML
CSS
Korišćene metode

U projektu su korišćene sljedeće metode:

obrada i čišćenje podataka
train/test podjela
OneHotEncoder za kategorijske podatke
StandardScaler za numeričke podatke
XGBoost klasifikator
predikcija churn vjerovatnoće
poslovno objašnjenje rizičnih faktora
ROI analiza retention kampanje
Struktura projekta
telco-churn-projekat/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── podaci/
│   └── Telco-Customer-Churn.csv
│
├── modeli/
│   └── churn_model.pkl
│
├── izvorni_kod/
│   ├── __init__.py
│   ├── ucitavanje_podataka.py
│   ├── priprema_podataka.py
│   ├── treniranje_modela.py
│   ├── predikcija.py
│   ├── objasnjenja.py
│   └── roi.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── korisnici.html
│   ├── detalji_korisnika.html
│   └── o_projektu.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
└── sveske/
    └── analiza.ipynb
Pokretanje projekta

Kreiranje virtuelnog okruženja:

python -m venv venv

Aktiviranje virtuelnog okruženja:

venv\Scripts\Activate.ps1

Instalacija biblioteka:

pip install -r requirements.txt

Treniranje modela:

python -m izvorni_kod.treniranje_modela

Pokretanje aplikacije:

python app.py

Aplikacija se otvara na adresi:

http://127.0.0.1:5000
Funkcionalnosti aplikacije

Aplikacija ima sljedeće stranice:

početna stranica
dashboard
lista rizičnih korisnika
detalji korisnika
stranica o projektu

Dashboard prikazuje:

broj korisnika
broj churn korisnika
churn rate
prosječan mjesečni trošak
prosječan tenure
broj korisnika po nivou rizika
ROI summary za retention kampanju

Lista korisnika omogućava:

rangiranje po churn riziku
filter po minimalnom riziku
filter po tipu ugovora
filter po internet usluzi
otvaranje detalja korisnika
Objašnjenje modela

Model vraća vjerovatnoću da korisnik napusti kompaniju.

Na osnovu vjerovatnoće određuje se nivo rizika:

0% - 39%   nizak rizik
40% - 69%  srednji rizik
70% - 100% visok rizik
ROI analiza

Za svakog korisnika računa se očekivani gubitak:

expected_loss = MonthlyCharges * 6 * churn_probability

Na osnovu rizika i očekivanog gubitka sistem predlaže retention akciju:

popust 20%
loyalty paket
kontakt korisnika
poziv korisničke podrške
bez posebne akcije
Zaključak

Projekat pokazuje kako se machine learning može koristiti za podršku odlučivanju u telekom kompaniji.

Aplikacija pomaže kompaniji da prepozna korisnike koji su u riziku, objasni razloge rizika i predloži poslovnu akciju za zadržavanje korisnika.