from pydantic import BaseModel as PydanticBaseModel
from langchain.pydantic_v1 import BaseModel, Field
from typing import List, Literal


class PaperAuthor(PydanticBaseModel):
    authorId: str | None
    name: str


class OpenAccessPdf(PydanticBaseModel):
    url: str
    status: str


class PaperSearchResult(PydanticBaseModel):
    paperId: str | None
    title: str
    authors: List[PaperAuthor]
    abstract: str | None
    venue: str | None
    year: int | None
    citationCount: int | None
    openAccessPdf: OpenAccessPdf | None


class RelevanceSearchAction(BaseModel):
    name: Literal["search_relevance"] = Field(
        description="Use this action to search for papers sorted by relevance."
    )
    query: str = Field(
        description="The search query you want to use to search for papers."
    )


class CitationCountSearchAction(BaseModel):
    name: Literal["search_citation_count"] = Field(
        description="Use this action to search for papers sorted by citation count."
    )
    query: str = Field(
        description="The search query you want to use to search for papers."
    )


class ReadAction(BaseModel):
    name: Literal["read"] = Field(description="Use this action to read a paper.")
    paper_id: str = Field(description="The paper id of the paper you want to read")


class SelectAction(BaseModel):
    name: Literal["select"] = Field(
        description="Use this action to select the paper that fits the excerpt."
    )
    paper_id: str = Field(description="The paper id of the paper you want to select")


class Output(BaseModel):
    reason: str = Field(description="A short explanation of the decision")
    action: (
        RelevanceSearchAction | CitationCountSearchAction | ReadAction | SelectAction
    )


class OutputSearchOnly(BaseModel):
    reason: str = Field(description="A short explanation of the decision")
    action: RelevanceSearchAction | CitationCountSearchAction | SelectAction


class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")
