import re

date = re.compile(r"(?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche) [0-9]+ (?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre) [0-9]{4}")
dic_months = {"janvier": "01", "février": "02", "mars": "03", "avril": "04", "mai": "05", "juin": "06", "juillet": "07",
              "août": "08", "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12"}
trad_months = {"January": "janvier", "February": "février", "March": "mars", "April": "avril", "May": "mai",
               "June": "juin", "July": "juillet", "August": "août", "September": "septembre", "October": "octobre",
               "November": "novembre", "December": "décembre"}