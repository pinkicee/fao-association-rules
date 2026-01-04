# Analiza algoritmilor pentru descoperirea regulilor de asociere  
## Aplicare pe date FAO/WHO GIFT privind consumul alimentar
 
Acest proiect analizează date individuale privind consumul alimentar, provenite
din platforma FAO/WHO GIFT (Global Individual Food Consumption Data Tool),
utilizând tehnici de *association rule mining*.
 
Scopul principal al proiectului este evaluarea și compararea algoritmului clasic
**Apriori** cu un algoritm alternativ mai eficient, **FP-Growth**, aplicat pe un
set de date real, dens, obținut din anchete de tip *24-hour recall*.
 

 
## Setul de date
 
Analiza se bazează pe două fișiere CSV:
 
- **consumption_user.csv** – conține informații despre alimentele consumate de
  fiecare individ, în cadrul anchetelor de tip 24h recall
- **subject_user.csv** – conține informații socio-demografice la nivel de individ,
  inclusiv țara de proveniență
 
Din considerente legate de dimensiunea fișierelor și de licențierea datelor FAO,
fișierele brute nu sunt incluse în acest repository.
 

 
## Metodologie
 
Etapele principale ale proiectului sunt:
 
1. Curățarea și preprocesarea datelor
2. Analiza descriptivă a setului de date (EDA)
3. Construirea tranzacțiilor pentru analiza regulilor de asociere:
   - **Tranzacție** = (SUBJECT, SURVEY_DAY)
   - **Item** = INGREDIENT
4. Eliminarea ingredientelor cu suport foarte redus
5. Identificarea itemset-urilor frecvente utilizând algoritmul **FP-Growth**
6. Generarea regulilor de asociere pe baza măsurilor:
   - suport (*support*)
   - încredere (*confidence*)
   - lift
7. Compararea performanței algoritmilor FP-Growth și Apriori
 
 
## Structura proiectului

```bash
fao-association-rules/
│
├── data/
│   ├── raw/                  # date brute (NU se urca pe GitHub)
│   │   ├── consumption_user.csv
│   │   └── subject_user.csv
│   └── processed/            # rezultate generate
│
├── src/
│   ├── config.py             # parametri si cai
│   ├── utils.py              # functii reutilizabile
│   ├── 01_eda.py             # analiza descriptiva
│   ├── 02_fp_growth.py       # FP-Growth + reguli
│   └── 03_compare_apriori.py # comparatie cu Apriori
│
├── requirements.txt
├── .gitignore
└── README.md
 ```

## Cerințe software
 
- Python 3.10 sau mai recent
- pandas
- mlxtend
- jupyter (opțional, pentru rularea notebook-urilor)
 
Instalarea dependențelor se poate face cu:

```bash 
pip install -r requirements.txt
```
## Compararea FP-Growth și Apriori (România + Lao PDR)

Compararea algoritmilor **FP-Growth** și **Apriori** a fost realizată pe un set de date FAO/WHO GIFT combinat, corespunzător României și Lao PDR.

### Definirea elementelor analizate

- **Tranzacție**: perechea *(SUBJECT, SURVEY_DAY)*
- **Item**: ingredient alimentar  
  - România: `INGREDIENT`  
  - Lao PDR: `INGREDIENT_ENG`

Setul de date rezultat conține aproximativ **3040 de tranzacții**, dintre care **~2900** au fost păstrate după etapa de filtrare.



## Rezultate experimentale

### Prag suport minim: `min_support = 0.05`

| Algoritm   | Timp de execuție (s) | Itemset-uri frecvente |
|------------|----------------------|-----------------------|
| FP-Growth  | 48.07                | 6852                  |
| Apriori    | 1.20                 | 6852                  |



### Prag suport minim: `min_support = 0.03`

| Algoritm   | Timp de execuție (s) | Itemset-uri frecvente |
|------------|----------------------|-----------------------|
| FP-Growth  | 324.56               | 42765                 |
| Apriori    | 6.91                 | 42765                 |



## Concluzie

În contextul acestui set de date FAO/WHO GIFT, algoritmul **Apriori** s-a dovedit semnificativ mai rapid decât **FP-Growth**, obținând aceleași itemset-uri frecvente pentru valorile analizate ale pragului de suport.

Rezultatele arată că performanța algoritmilor de descoperire a regulilor de asociere depinde de caracteristicile concrete ale datelor (dimensiune, densitate) și de alegerea pragului de suport. Deși **FP-Growth** prezintă avantaje teoretice pentru seturi de date foarte mari și dense, **Apriori** poate oferi performanțe superioare în contexte practice bine definite, precum cel analizat în acest proiect.
