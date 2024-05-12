import glob
from typing import Optional

import pandas as pd
from thefuzz import process

from scripts.course import Course, Campus, Session


class ProfQuery:
    def __init__(self, files_path: str, csv: Optional[str] = None):
        """
        :param files_path: The glob path to the CSVs by session.
        :param csv: The path to a CSV containing the query data that's already been processed.
        """
        if csv is None:
            files = glob.glob(files_path)
            self.data: pd.DataFrame = (
                pd.concat(pd.read_csv(file) for file in files).dropna(subset=['Professor']).sort_values(
                    by='Subject').reset_index())
            self.data = self.data[self.data['Professor'].str.strip() != ""]  # remove whitespace entries

            # turn all professors fields that are semicolon delimited into their own courses
            self.data['Professor'] = (
                self.data['Professor'].str.split(';').map(lambda profs: [prof.strip() for prof in profs]))
            self.data = self.data.explode('Professor').sort_values(by='Subject').reset_index()
        else:
            self.data = pd.read_csv(csv)

    def close_profs(self, search: str, count: int) -> list[str]:
        """
        Finds names of n profs closest to the query in search.
        :param search: The name of the prof to search for
        :param count: The number of results to return
        :return: Returns a list of profs most similar to search, of size at most count.
        """

        return [name[0] for name in
                process.extract(query=search, choices=list(self.data['Professor'].unique()), limit=count)]

    def query(self, professor: str) -> list[Course]:
        """
        :param professor: returns Courses that the given professor have taught
        :return: The courses that the prof has taught, from most recent to least.
        """

        result: list[Course] = []

        df_courses: pd.DataFrame = self.data[self.data['Professor'] == professor]

        for _, row in df_courses.iterrows():
            c = Course(campus=Campus('UBCV' if str(row['Campus']) == 'UBC' else row['Campus']), year=row['Year'],
                       session=Session(row['Session']), subject=row['Subject'], code=str(row['Course']),
                       detail=(row['Detail'] if not pd.isna(row['Detail']) else None), section=str(row['Section']),
                       desc=row['Title'], avg=row['Avg'])
            result.append(c)

        # sort found courses by year, session order
        result = sorted(result, reverse=True)

        return result
