from utils.semantic_scholar import SemanticScholarAPI, SemanticScholarWebSearch
from utils import PaperSearchResult
from typing import List


class SearchProvider:
    def __call__(self, search_term: str, year: str) -> List[PaperSearchResult]:
        raise NotImplementedError("Subclasses must implement this method")


class SemanticScholarSearchProvider(SearchProvider):
    def __init__(
        self,
        fieldsOfStudy: str = "Computer Science",
        limit: int = 10,
        # sort: str = "citationCount:desc",
        only_open_access: bool = False,
    ):
        # These fields are required for the PaperSearchResult model
        self.fields = (
            "paperId,title,authors,venue,year,citationCount,abstract,openAccessPdf"
        )
        self.fieldsOfStudy = fieldsOfStudy
        self.limit = limit
        self.only_open_access = only_open_access
        # self.sort = sort
        self.s2api = SemanticScholarAPI()

    def citation_count_search(
        self, query: str, year: str | None
    ) -> List[PaperSearchResult]:
        papers = self.s2api.bulk_search(
            query,
            self.fields,
            self.fieldsOfStudy,
            year=year,
            only_open_access=self.only_open_access,
        )
        if "data" not in papers:
            return []
        papers = [PaperSearchResult(**paper) for paper in papers["data"]]
        return papers[: self.limit]

    def __call__(self, query: str, year: str | None = None) -> List[PaperSearchResult]:
        # papers = self.s2api.bulk_search(query, self.fields, self.fieldsOfStudy, self.sort)
        papers = self.s2api.relevance_search(
            query,
            self.fields,
            self.fieldsOfStudy,
            year,
            self.limit,
            only_open_access=self.only_open_access,
        )
        if "data" not in papers:
            return []
        papers = [PaperSearchResult(**paper) for paper in papers["data"]]
        return papers


class SemanticScholarWebSearchProvider(SearchProvider):
    def __init__(
        self,
        fieldsOfStudy: str = "Computer Science",
        limit: int = 10,
        # sort: str = "citationCount:desc",
        only_open_access: bool = False,
    ):
        # These fields are required for the PaperSearchResult model
        self.fields = (
            "paperId,title,authors,venue,year,citationCount,abstract,openAccessPdf"
        )
        self.fieldsOfStudy = fieldsOfStudy
        self.limit = limit
        self.only_open_access = only_open_access
        # self.sort = sort
        self.s2api = SemanticScholarWebSearch()

    def citation_count_search(
        self, query: str, year: str | None
    ) -> List[PaperSearchResult]:
        papers = self.s2api.web_search(
            query,
            fields=self.fields,
            fields_of_study=(
                self.fieldsOfStudy.replace(" ", "-").lower()
                if self.fieldsOfStudy
                else None
            ),
            sort="total-citations",
            cutoff_year=year.replace("-", "") if year else None,
            limit=self.limit,
            only_open_access=self.only_open_access,
        )
        papers = [PaperSearchResult(**paper) for paper in papers]
        return papers[: self.limit]

    def __call__(self, query: str, year: str | None = None) -> List[PaperSearchResult]:
        # papers = self.s2api.bulk_search(query, self.fields, self.fieldsOfStudy, self.sort)
        papers = self.s2api.relevance_search(
            query,
            self.fields,
            self.fieldsOfStudy,
            year,
            self.limit,
            only_open_access=self.only_open_access,
        )
        papers = [PaperSearchResult(**paper) for paper in papers]
        return papers

