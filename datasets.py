"""
File: datasets.py
Author(s): Onno Verberne
Last updated: 2021-04-20

Description: Contains methods for obtaining tests data from the datasets.
"""
import os
from glob import iglob
from typing import Any, TypeVar, Type

T = TypeVar('T')


class ljubovic:
    def __init__(self, directory: str) -> None:
        self.directory = directory
        self.__plag_file__ = "ground-truth-dynamic-anon.txt"
        self.__groups__ = {
            "c1": "A2016",  # + os.path.sep + "Z1",
            "c2": "A2017",
            "cpp1": "B2016",
            "cpp2": "B2017",
        }

    def get_data_per_author(self, group: str = "c1",
                            plagiarized: bool = True,
                            count: int = None) \
            -> tuple[dict[str, list[tuple[str, str]]], set[str]]:
        data = {}
        assignment_keys = set()
        authors = set()
        plagiarizers = [] if plagiarized else self.get_plagiarizers(group)

        # Group contains the file extension + group number
        file_ext = "." + group[:-1]
        ext_len = len(file_ext)
        directory = os.path.join(self.directory, "src", self.__groups__[group], "**", "*" + file_ext)  # noqa

        # Loop through all the submissions in the directory
        for file_path in iglob(directory, recursive=True):
            # Student ids are stored in the filename
            author = os.path.basename(file_path)[:-ext_len]
            assignment_key = ljubovic.assignment_key(file_path)

            # Filter plagiarizers from the dataset
            if not plagiarized and author in plagiarizers:
                continue

            # Limit the amount of authors
            if count is not None:
                if len(authors) >= count and author not in authors:
                    continue
                else:
                    authors.add(author)

            # Create a new list if none exists
            data[author] = data.get(author, [])
            data[author].append((assignment_key, file_path))
            assignment_keys.add(assignment_key)

        return data, assignment_keys

    def get_plagiarizers(self, group: str = "c1") -> list[str]:
        plagiarizers: list[str] = []

        with open(os.path.join(self.directory, self.__plag_file__), 'r') as f:
            line = f.readline()

            # Traverse to the first occurance of the group
            while line:
                if line.startswith("- " + self.__groups__[group]):
                    break

                line = f.readline()

            # Add all students in the group to the plagiarizers
            while line:
                if line.startswith("-"):
                    if line[2:].startswith(self.__groups__[group]):
                        continue
                    else:  # Start of a different group, thus break
                        break

                plagiarizers.extend(line.split(","))
                line = f.readline()

        return plagiarizers

    @staticmethod
    def assignment_key(file_path: str) -> str:
        """The assignment key is the concatenation of the subfolders.
        Example: .../A2016/Z1/Z2/student1000.c -> Z1/Z2"""
        return os.path.sep.join(file_path.split(os.path.sep)[-3:-1])

    @staticmethod
    def key_func():
        return lambda x: x


def dict_to_sorted_list(data: dict[Any, Type[T]]) \
        -> list[Type[T]]:
    """Transforms the author dictionary into a list,
    with indexes corresponding to the sorted dictionary keys."""
    return [data[key] for key in sorted(data.keys())]


def split_per_author_list(data: list[list[tuple[Any, str]]],
                          test_keys: set[str],
                          key_func: Any) \
        -> tuple[list[list[str]], list[tuple[int, str]]]:
    """Split the sorted list of author files into training and test data
    based on the keys in test_keys
    """
    training = [[] for _ in range(len(data))]
    test = []

    # Iterate over all authors.
    for i, entries in enumerate(data):
        # Iterate over the authors' submissions.
        for key, entry in entries:
            if key_func(key) in test_keys:
                test.append((i, entry))
            else:
                training[i].append(entry)

    return training, test


def split_per_author_data(data: dict[Any, list[str]],
                          test_file_keys: set[str],
                          key_func: Any) \
        -> tuple[dict[Any, list[str]], list[tuple[Any, str]]]:
    training = {}
    test = []

    for author in data.keys():
        training[author] = []

        for entry in data[author]:
            if key_func(entry) in test_file_keys:
                test.append((author, entry))
            else:
                training[author].append(entry)

    return training, test


if __name__ == "__main__":
    pass
