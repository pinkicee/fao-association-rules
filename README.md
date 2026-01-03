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
├── data/
│ ├── raw/ # fișiere CSV brute (neincluse în repository)
│ └── processed/ # rezultate generate de algoritmi
│
├── src/
│ ├── 01_eda.py
│ ├── 02_fp_growth.py
│ └── 03_compare_apriori.py
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