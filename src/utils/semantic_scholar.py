import sys
import os
import requests
from typing import Dict
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import urllib.parse
from typing import Literal
from time import time


class SemanticScholarAPI:
    """See https://github.com/allenai/s2-folks/blob/main/examples/python/find_and_recommend_papers/find_papers.py"""

    def __init__(self, api_key=os.environ.get("S2_API_KEY")) -> None:
        assert api_key, "API key is required"
        self.base_url = "https://api.semanticscholar.org/graph/v1/paper"
        self.api_key = api_key

    def search(
        self, query, fields="paperId,title,authors,venue,year", limit=10, offest=0
    ):
        response = requests.get(
            f"{self.base_url}/search",
            headers={"X-API-KEY": self.api_key},
            params={"query": query, "limit": limit, "fields": fields},
        )
        return response.json()

    def autocomplete(self, query):
        response = requests.get(
            f"{self.base_url}/autocomplete",
            headers={"X-API-KEY": self.api_key},
            params={"query": query},
        )
        return response.json()

    def bulk_search(
        self,
        query: str,
        fields="paperId,title,authors,venue,year,citationCount,abstract,openAccessPdf",
        fieldsOfStudy: str | None = "Computer Science",
        sort="citationCount:desc",
        year: str | None = None,
        only_open_access: bool = False,
    ):
        params: Dict[str, str] = {
            "query": query,
            "fields": fields,
            "sort": sort,
        }
        if year:
            params["year"] = year
        if fieldsOfStudy:
            params["fieldsOfStudy"] = fieldsOfStudy
        if only_open_access:
            params["openAccessPdf"] = ""
        response = requests.get(
            f"{self.base_url}/search/bulk",
            headers={"X-API-KEY": self.api_key},
            params=params,
        )
        return response.json()

    def relevance_search(
        self,
        query: str,
        fields: str = "paperId,title,authors,venue,year,citationCount,abstract,openAccessPdf",
        fieldsOfStudy: str | None = "Computer Science",
        year: str | None = None,
        limit: int = 10,
        offset: int = 0,
        only_open_access: bool = False,
    ):
        params: Dict[str, str | int] = {}
        params["query"] = query
        params["fields"] = fields
        params["limit"] = limit
        params["offset"] = offset
        if year:
            params["year"] = year
        if fieldsOfStudy:
            params["fieldsOfStudy"] = fieldsOfStudy
        if only_open_access:
            params["openAccessPdf"] = ""

        response = requests.get(
            f"{self.base_url}/search",
            headers={"X-API-KEY": self.api_key},
            params=params,
        )
        return response.json()

    def get_details(
        self,
        paper_id,
        fields: str = "paperId,title,authors,venue,year,citationCount,abstract,openAccessPdf",
    ):
        response = requests.get(
            f"{self.base_url}/{paper_id}",
            headers={"X-API-KEY": self.api_key},
            params={"fields": fields},
        )
        return response.json()


class SemanticScholarWebSearch(SemanticScholarAPI):
    def __init__(
        self,
        api_key=os.environ.get("S2_API_KEY"),
        driver=None,
        auto_restart_driver: int | None = 10*60,
    ) -> None:
        super().__init__(api_key)
        self.auto_restart_driver = auto_restart_driver
        if driver:
            self.driver = driver
            self.auto_restart_driver = None
        else:
            self.driver = webdriver.Safari()

    def __restart_driver(self):
        self.driver.quit()
        self.driver = webdriver.Safari()
        self.warmup()

    def warmup(self):
        self.start_time = time()
        self.driver.get("https://www.semanticscholar.org/")
        self.driver.implicitly_wait(30)

    def __del__(self):
        self.driver.quit()

    def web_search(
        self,
        query,
        fields="paperId,title,authors,venue,year,citationCount,abstract,openAccessPdf",
        fields_of_study: None | str = "computer-science",
        sort: Literal["relevance", "total-citations"] = "relevance",
        cutoff_year=None,
        limit: int = 10,
        offset: int = 0,
        only_open_access=False,
    ):
        assert limit <= 10, "Limit must be less than or equal to 10"
        assert offset == 0, "Offset other than 0 is not implemented"

        if self.auto_restart_driver and time() - self.start_time > self.auto_restart_driver:
            self.__restart_driver()

        year_str = ""
        fields_of_study_str = ""
        pdf_str = ""
        if cutoff_year:
            year_str += f"year%5B0%5D=1931&year%5B1%5D={cutoff_year}&"
        if fields_of_study:
            fields_of_study_str = f"fos%5B0%5D={fields_of_study}&"
        if only_open_access:
            pdf_str = "&pdf=true"

        # URL encode query
        query = urllib.parse.quote(query)
        url = f"https://www.semanticscholar.org/search?{year_str}{fields_of_study_str}q={query}&sort={sort}{pdf_str}"
        print("Opening", url)

        try:
            self.driver.get(url)
        except Exception as e:
            print(f"Error opening {url}: {e}")
            self.__restart_driver()
            try:
                self.driver.get(url)
            except Exception as e:
                print(f"Error opening {url} after restarting driver: {e}")
                sys.exit(1)
        # self.driver.implicitly_wait(30)

        xpath_expression = "//div[@class='cl-paper-row serp-papers__paper-row paper-v2-cue paper-row-normal' and @data-paper-id]"
        # find all div elements that match the XPath expression
        paper_div_elements = []
        try:
            paper_div_elements = self.driver.find_elements(By.XPATH, xpath_expression)
        except TimeoutException:
            try:
                paper_div_elements = self.driver.find_elements(By.XPATH, xpath_expression)
            except TimeoutException as e:
                raise e

        # iterate over the div elements and print the value of data-paper-id
        papers = []
        for element in paper_div_elements:
            paper_id = element.get_attribute("data-paper-id")
            try:
                papers.append(self.get_details(paper_id, fields=fields))
            except Exception as e:
                print(f"Error fetching paper details for {paper_id}: {e}")

        if "openAccessPdf" in fields:
            external_paper_urls = {}
            external_paper_url_elements = []
            try:
                external_paper_url_elements = self.driver.find_elements(
                    By.CLASS_NAME, "cl-paper-view-paper"
                )
            except TimeoutException:
                try:
                    external_paper_url_elements = self.driver.find_elements(
                        By.CLASS_NAME, "cl-paper-view-paper"
                    )
                except TimeoutException as e:
                    pass
            for paper_url_element in external_paper_url_elements:
                href = paper_url_element.get_attribute("href")
                paper_id = paper_url_element.get_attribute("data-heap-paper-id")
                external_paper_urls[paper_id] = href

            for paper in papers:
                if (
                    not paper["openAccessPdf"]
                    and paper["paperId"] in external_paper_urls
                ):
                    try:
                        if external_paper_urls[paper["paperId"]].startswith(
                            "https://www.sciencedirect.com"
                        ):
                            self.driver.get(url)
                            anchor_element = self.driver.find_element(
                                By.XPATH, "//a[@title='PDF']"
                            )
                            pdf_link = "https://dl.acm.org" + anchor_element.get_attribute("href")
                            paper["openAccessPdf"] = {
                                "url": pdf_link,
                                "status": "GREEN",
                            }
                        else:
                            paper["openAccessPdf"] = {
                                "url": external_paper_urls[paper["paperId"]],
                                "status": "GREEN",
                            }
                        if external_paper_urls[paper["paperId"]].startswith(
                            "location.href="
                        ):
                            pass
                    except Exception as e:
                        print(
                            f"Error fetching external paper URL for {paper['paperId']}: {e}"
                        )

        if len(papers) > limit:
            papers = papers[:limit]

        return papers

    def relevance_search(
        self,
        query: str,
        fields: str = "paperId,title,authors,venue,year,citationCount,abstract,openAccessPdf",
        fieldsOfStudy: str | None = "Computer Science",
        year: str | None = None,
        limit: int = 10,
        offset: int = 0,
        only_open_access: bool = False,
    ):
        return self.web_search(
            query,
            fields=fields,
            fields_of_study=(
                fieldsOfStudy.replace(" ", "-").lower() if fieldsOfStudy else None
            ),
            sort="relevance",
            cutoff_year=year,
            limit=limit,
            offset=offset,
            only_open_access=only_open_access,
        )
