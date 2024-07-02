from difflib import SequenceMatcher as SM
from typing import List, Tuple
import numpy as np
from utils.data_model import PaperSearchResult

def find_match(papers: List[str], selected_title: str, threshold=0.8) -> Tuple[int, str] | None:
    similarities = [SM(a=selected_title.lower(), b=pt.lower()).ratio() for pt in papers]
    max_sim = max(similarities)
    if max_sim > threshold:
        ind = int(np.argmax(similarities))
        return ind, papers[ind]
    return None


def is_similar(title1, title2, threshold=0.8):
    return SM(a=title1.lower(), b=title2.lower()).ratio() > threshold


def find_multi_match_psr(
    papers: List[PaperSearchResult], selected_titles: List[str], threshold=0.8
) -> Tuple[PaperSearchResult, int] | None:
    for title in selected_titles:
        m = find_match_psr(papers, title, threshold)
        if m is not None:
            return m
    else:
        return None


def find_match_psr(
    papers: List[PaperSearchResult], selected_title: str, threshold=0.8
) -> Tuple[PaperSearchResult, int] | None:
    if len(papers) == 0:
        return None
    paper_titles = papers
    if isinstance(papers[0], PaperSearchResult):
        paper_titles = [p.title for p in papers]
    similarities = [
        SM(a=selected_title.lower(), b=pt.lower()).ratio() for pt in paper_titles
    ]
    max_sim = max(similarities)
    if max_sim > threshold:
        ind = int(np.argmax(similarities))
        return papers[ind], ind
        # return papers[similarities.index(max_sim)]
    return None
