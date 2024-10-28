#!/usr/bin/env python3
"""
Pagination Module

This module contains the Server class, which provides a paginated view of a
dataset of popular baby names. It includes methods to retrieve pages of data
and determine index ranges based on pagination parameters.

Classes:
    - Server: Manages the baby names dataset, loading it from a CSV file and
              providing paginated access.

Functions:
    - index_range(page: int, page_size: int) -> Tuple[int, int]: Computes
      the start and end indexes for a given page and page size.
"""

import csv
import math
from typing import List, Tuple


class Server:
    """
    Server class to paginate a database of popular baby names.

    Attributes:
        DATA_FILE (str): Path to the CSV file containing the baby names
                         dataset.
        __dataset (List[List], optional): Cached dataset loaded from
                                          DATA_FILE.
    """

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initializes a new Server instance with an uninitialized dataset
        cache."""
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


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Computes the start and end index for a given page and page size.

    Args:
        page (int): The current page number (1-based).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start and end indexes for
                         the specified page range.
    """
    return ((page - 1) * page_size, page * page_size)
