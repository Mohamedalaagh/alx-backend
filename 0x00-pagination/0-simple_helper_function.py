#!/usr/bin/env python3
""" Pagination """

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Return tuple of the size two that contains both start and end
    index according to the range of indexes to return in a list
    for those particular pagination parameters.
    """
    return ((page - 1) * page_size, page * page_size)
