#!/usr/bin/env python3
"""
Pagination Module

This module includes the Server class, which provides paginated access to
a dataset of popular baby names, along with helper functions to manage
index ranges and additional pagination information.

Classes:
    - Server: Manages dataset caching and paginated retrieval of data.

Functions:
    - index_range(page: int, page_size: int) -> Tuple[int, int]: Computes
      start and end indexes based on page and page size.
"""

import csv
import math
from typing import List, Tuple


class Server:
    """
    Server class to paginate a database of popular baby names.

    Attributes:
        DATA_FILE (str): Path to the CSV file with the baby names dataset.
        __dataset (List[List], optional): Cached dataset loaded from
                                          DATA_FILE.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initializes the Server instance with a null dataset cache."""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Loads and caches dataset if not already loaded.

        Returns:
            List[List]: The dataset loaded from the CSV file, excluding
                        the header row.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Exclude header row

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Returns a specific page of the dataset.

        Args:
            page (int): The page number to retrieve (1-based).
            page_size (int): Number of items per page.

        Returns:
            List[List]: The rows corresponding to the specified page.

        Raises:
            AssertionError: If page or page_size are not positive integers.
        """
        assert(isinstance(page, int) and isinstance(page_size, int))
        assert(page > 0 and page_size > 0)
        [start, end] = index_range(page, page_size)
        return self.dataset()[start: end]

    def get_hyper(self, page: int, page_size: int) -> dict:
        """
        Returns a dictionary containing pagination details.

        Args:
            page (int): The current page number (1-based).
            page_size (int): The number of items per page.

        Returns:
            dict: A dictionary with pagination data:
                - page_size (int): Length of the dataset page.
                - page (int): Current page number.
                - data (List[List]): Dataset page records.
                - next_page (int or None): Next page number, or None if no
                                           further pages.
                - prev_page (int or None): Previous page number, or None if
                                           no previous pages.
                - total_pages (int): Total number of pages.
        """
        dataset_records = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.__dataset) / page_size)

        return {
            'page_size': len(dataset_records),
            'page': page,
            'data': dataset_records,
            'next_page': page + 1 if (page + 1) <= total_pages else None,
            'prev_page': page - 1 if (page - 1) > 0 else None,
            'total_pages': total_pages
        }


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Computes the start and end indexes for pagination.

    Args:
        page (int): The current page number (1-based).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing start and end indexes for
                         the specified page range.
    """
    return ((page - 1) * page_size, page * page_size)
