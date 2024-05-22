from BaseMatcher import BaseMatcher
import sys
import subprocess
import pandas as pd
import logging

# Add git root dir to the python path to enable importing services module (and by that BaseScraper and DataHandler)
sys.path.append(
    subprocess.check_output("git rev-parse --show-toplevel".split())
    .decode("utf-8")
    .strip()
)


class SimpleMatcher(BaseMatcher):
    def __init__(self, source):
        super().__init__(source)
        print(self.root)

    def match_by_hand(self, easy, hard):
        """
        Paths or URLs can be passed. URLs are converted into paths.
        """
        if easy.startswith(("www", "https://")):
            easy = self.data_handler.search_by("e", "url", easy)
        if hard.startswith(("www", "https://")):
            hard = self.data_handler.search_by("h", "url", hard)

        # write match or log error
        if easy is None or hard is None:
            logging.error(f"Could not find text for {easy} or {hard}")
        else:
            logging.info(f"Writing Match: {easy} with {hard}")
            self.write_match(easy, hard)

    def check_mdr_match_cashe(self):
        file = "data/mdr/match_cashe_mdr.csv"
        lookup_hard = "data/mdr/hard/lookup_mdr_hard.csv"
        lookup_easy = "data/mdr/easy/lookup_mdr_easy.csv"

        match_cache_df = pd.read_csv(file)
        lookup_hard_df = pd.read_csv(lookup_hard)
        lookup_easy_df = pd.read_csv(lookup_easy)

        rows_to_drop = []

        for idx, row in match_cache_df.iterrows():
            easy_url = row["url"]
            hard_url = row["match"]
            if (lookup_easy_df["url"].str.contains(easy_url).any()) and (
                lookup_hard_df["url"].str.contains(hard_url).any()
            ):
                self.match_by_hand(easy_url, hard_url)
                rows_to_drop.append(idx)

        # delete rows that are mateched from cashe
        match_cache_df.drop(rows_to_drop, inplace=True)
        match_cache_df.to_csv(file, index=False)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    matcher = SimpleMatcher("mdr")
    matcher.check_mdr_match_cashe()
