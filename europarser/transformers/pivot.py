import json
from typing import Any, List
from bs4 import BeautifulSoup

from europarser.models import FileToTransform, Pivot
from europarser.transformers.transformer import Transformer
from europarser.utils import date, trad_months, dic_months


class PivotTransformer(Transformer):
    def __init__(self):
        super().__init__()

    def transform(self, file_to_transform: FileToTransform) -> List[Pivot]:
        self._logger.warning("Processing file " + file_to_transform.name)
        soup = BeautifulSoup(file_to_transform.file, 'html.parser')

        corpus = []

        # tous les articles commencent par une image, j'ai ajouté manuellement des balises article avant chaque image dans le html
        articles = soup.find_all("article")
        for article in articles:
            doc = {}
            try:
                doc["journal"] = article.find("span", attrs={"class": "DocPublicationName"}).text.strip()
            except Exception as e:
                self._logger.warning("pas un article de presse")
                self._log_error(e, article)
                continue
            try:
                day, day_nb, month, year = date.findall(article.find("span", attrs={"class": "DocHeader"}).text)[
                    0].split()
            except:
                try:
                    day_nb, month, year = article.find("span", attrs={"class": "DocHeader"}).text.split()[:3]
                    if day_nb == "Thursday,":
                        day_nb, month, year = "1", "juillet", "2004"
                except:
                    day_nb, month, year = article.find("span",
                                                       attrs={"class": "DocTitreSousSection"}).find_next_sibling("span").text.split()[:3]
            if "," in month:
                day_nb, month = month[:-1], trad_months[day_nb]
            doc["date"] = " ".join([year, dic_months[month], day_nb])
            try:
                doc["titre"] = article.find("div", attrs={"class": "titreArticle"}).text.strip()
            except:
                doc["titre"] = article.find("p", attrs={"class": "titreArticleVisu"}).text.strip()
            try:
                doc["texte"] = article.find("div", attrs={"class": "docOcurrContainer"}).text.strip()
            except:
                doc["texte"] = article.find("div", attrs={"class": "DocText clearfix"}).text.strip()

            corpus.append(Pivot(**doc))

        with open(f"errors-{file_to_transform.name}.json", "w", encoding="utf-8") as f:
            json.dump([e.dict() for e in self.errors], f, ensure_ascii=False)

        return corpus

