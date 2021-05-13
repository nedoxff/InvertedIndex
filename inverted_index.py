"""
    The heart of this project.
    An invertex index list looks like this:
    "word": [1, 47, 24]
    "words": [5478, 245, 2]
    So instead of specifying on which indexes there are words,
    We specify which words are on these indexes.

    The average performance for creating, saving, searching and loading
    combined is about 33s on wikipedia_sample (77MB, 4100 entries).
"""

# Imports
from collections import defaultdict
import json
import os
import string
import itertools


class InvertedIndex:
    # The constructor.
    def __init__(self, words_invered_index: dict):
        if len(words_invered_index) == 0:
            raise Exception("The specified invertex index list was empty!")
        self.words_inverted_index = {
            i: j for i, j in words_invered_index.items()
        }

    # Save everything in words_inverted_index to a file.
    def dump(self, filepath: str):
        result = defaultdict()
        # Combine [2, 36, 25] into "2;36;25"
        for key, varray in self.words_inverted_index.items():
            combined_string = ""
            for value in varray:
                combined_string += str(value) + ";"
            result[key] = combined_string
        # Write to file!
        with open(filepath, "w") as file:
            json.dump(result, file, indent=4)

    def tag(self, split_into: int, occurences: int, words: dict, file: str, opening_tag: str = "<tag>", closing_tag: str = "</tag>"):
        f = open(file, mode='w', encoding='utf-8')
        for line in words.values():
            split_words = line.split(" ")
            split = split_into_groups(split_into, split_words)
            for s in split:
                if len(s) < split_into or len(self.query(s)) < occurences:
                    f.write(' '.join(s) + ' ')
                else:
                    f.write(opening_tag + ' '.join(s) + closing_tag + " ")
            f.write("\n")
        f.close()

    # Search for words in words_inverted_index.
    def query(self, words: [str]) -> [int]:
        indexes = [self.words_inverted_index[word] for word in words if word in self.words_inverted_index]
        i = 1
        s1 = set(indexes[0])
        while i < len(indexes) - 1:
            s2 = set(indexes[i])
            s1.intersection_update(s2)
            i += 1
        return list(s1)

    # A static method for loading a new inverted index from a file.
    @classmethod
    def load_inverted_index(cls, filepath):
        if not os.path.isfile(filepath):
            raise Exception("The specified file does not exist!")
        with open(filepath, encoding='utf-8', mode='r') as f:
            data = json.load(f)
            f.close()
        # Decrypt our "2465;234;22" to [2465, 234, 22]
        new_data = defaultdict(list)
        for k, v in data.items():
            if len(v) is not 0:
                numbers = [int(s) for s in v.strip().split(';') if s.isdigit()]
                new_data[k] = numbers
        return InvertedIndex(new_data)


# Load the unedited dataset which should be turned
def load_dataset(filepath: str, stop_words: str) -> dict:
    result = dict()

    stop_words_file = open(stop_words, mode='r', encoding='utf-8')
    stop = [i.strip().lower() for i in stop_words_file.readlines()]
    stop_words_file.close()
    if len(stop) == 0:
        raise Exception("The stop words were empty!")

    lines_file = open(filepath, mode='r', encoding='utf-8')

    for line in lines_file:
        line = line.strip().lower()
        # Get the index, and then all remaining.
        index, *words = line.split("\t")
        words_line = words[0]
        new_line = []
        for w in words_line.split(" "):
            w = w.translate(str.maketrans('', '', string.punctuation))
            if w not in stop and len(w) is not 0 and not any(character.isdigit() for character in w):
                new_line.append(w)
        # If our index is not a number
        if not index.isdigit():
            raise Exception("Some line(s) don't have indexes!")
        # Also remove all punctuation from the entries.
        result[int(index)] = ' '.join(new_line)

    return result


# Only get the unique words from a dictionary.
def get_unique_words(dataset: dict) -> dict:
    result = dict()
    for key, value in dataset.items():
        result[key] = sorted(list(set(value.split(" "))))
    return result


# Combine a dictionary of (int, [str]) to an InvertedIndex.
def combine_into_list(dataset: dict) -> InvertedIndex:
    if len(dataset) == 0:
        raise Exception("The dataset was empty!")
    result = defaultdict(list)
    for key, value in dataset.items():
        for word in value:
            result[word].append(key)
    return InvertedIndex(result)


# Split a list into groups length of split_to.
'''
Example:
a = range(5)
split_into_groups(2, a)
>>> [[0, 1], [2, 3], [4]]
'''


def split_into_groups(split_to, iterable):
    args = [iter(iterable)] * split_to
    return list(([item for item in group if item is not None] for group in itertools.zip_longest(*args)))
