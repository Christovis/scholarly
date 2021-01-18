import json
import numpy as np
import pandas as pd

dir_data = "/home/christovis/02_AGE/logicmag/"
filepath_geo = dir_data + "countries.csv"
df_geo = pd.read_csv(filepath_geo, delimiter=";", header=0,)


class Publications:
    """
    """

    def __init__(self, dic_pu: dict, dic_auth: dict):
        self.dic_pu = dic_pu
        self.dic_auth = dic_auth


    @classmethod
    def from_file(
        cls,
        file_pub: str,
        file_auth: str,
    ) -> "Publications":
        """
        Args:
        Returns:
        """
        with open(file_pub) as f:
            dic_pu = json.load(f)
        with open(file_auth) as f:
            dic_auth = json.load(f)
        return Affiliations(dic_pu, dic_auth)


    def get_titles(self) -> list:
        titles = []
        for key, publication in self.dic_pu.items():
            titles.append(publication["bib"]["title"])
        return titles


    def get_geography_of_publications(
        self,
        rm_fail: bool=True,
    ):
        """
        Args:
        Returns:
        """
        geodistr = []
        for key, publication in self.dic_pu.items():
            authors = self.get_authors(publication)
            geodistr.append(self.get_author_continents(authors))
        if rm_fail: geodistr = [distr for distr in geodistr if len(distr) > 0]
        return geodistr


    def get_distribution(self, li: list, key: str) -> np.ndarray:
        """
        Args:
        Returns:
        """
        hist = np.zeros(len(li))
        for idx, distr in enumerate(li):
            tot_count = len(distr)
            key_count = sum(np.array(distr) == key)
            hist[idx] = key_count / tot_count
        return np.unique(hist, return_counts=True)



    def get_authors(self, publication: dict) -> list:
        """
        Get list of authors of a publication.

        Args:
        Returns:
        """
        author_ids = publication["author_id"]
        authors = [
            author
            for author in self.dic_auth.values()
            if author["scholar_id"] in author_ids
        ]
        return authors


    def get_author_ccTLDs(self, authors: list) -> list:
        """
        Args:
        Returns:
        """
        return [author["email_domain"].split(".")[-1] for author in authors]


    def get_author_continents(self, authors: list) -> list:
        """
        Args:
        Returns:
        """
        ccTLDs = self.get_author_ccTLDs(authors)
        continents = [
            df_geo[df_geo["ccTLD"] == ccTLD]["continent"].values[0]
            for ccTLD in ccTLDs
            if len(df_geo[df_geo["ccTLD"] == ccTLD]) > 0
        ]
        return continents
