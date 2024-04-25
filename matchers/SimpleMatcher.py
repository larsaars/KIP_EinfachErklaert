from BaseMatcher import BaseMatcher


class SimpleMatcher(BaseMatcher):
    def __init__(self, source):
        super().__init__(source)
        print(self.root)

    def match_by_hand(self, easy, hard):
        """
        paths or urls can be passed. urls are converted into paths
        """
        if easy.startswith(("www", "https://")):
            easy = self.data_handler.search_by("e", "url", easy)
        if hard.startswith(("www", "https://")):
            hard = self.data_handler.search_by("e", "url", hard)
        if easy is None or hard is None:
            raise Exception(f"Cannot find path for you url")
        self.write_match(easy, hard)
