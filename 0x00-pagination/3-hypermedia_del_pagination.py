#!/usr/bin/env python3
"""
Deletion-resilient Hypermedia Pagination Module

This module defines the Server class, which provides paginated access
to a dataset of popular baby names. The pagination is resilient to
deletions in the dataset.

Classes:
    - Server: Manages dataset caching, indexed access, and pagination.
"""

import csv
from typing import List, Dict


class Server:
    """
    Server class to paginate a database of popular baby names.

    Attributes:
        DATA_FILE (str): Path to the CSV file with the baby names dataset.
        __dataset (List[List], optional): Cached dataset loaded from
                                          DATA_FILE.
        __indexed_dataset (Dict[int, List], optional): Indexed version
                                                      of the dataset.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initializes the Server instance with null dataset caches."""
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """
        Loads and caches the dataset if not already loaded.

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

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Returns the dataset indexed by its position, starting at 0.

        Caches the first 1000 rows of the dataset in a dictionary where
        each key is the index and the value is the corresponding row.

        Returns:
            Dict[int, List]: Indexed dataset dictionary.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: truncated_dataset[i] for i in range(len(truncated_dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Returns a dictionary containing pagination details resilient to
        deletions in the dataset.

        Args:
            index (int): The starting index for pagination.
            page_size (int): The number of items per page.

        Returns:
            Dict: A dictionary containing pagination details.
        """
        # This function implementation is pending.
        pass
