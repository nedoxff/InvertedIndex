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

    # Search for words in words_invertex_index.
    def query(self, words: [str]) -> [int]:
        for word in words:
            if word not in self.words_inverted_index:
                raise Exception("Word '" + word + "' does not exist in the dictionary!")
        indexes = [self.words_inverted_index[word] for word in words]
        found = []
        # This function only finds the indexes where it contains ALL WORDS specified in "words".
        for index_array in indexes:
            for index in index_array:
                if index not in found and all([index in array for array in indexes]):
                    found.append(index)
        return found

    # A static method for loading a new invertex index from a file.
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


# A helper method for reading a file. (includes stripping and lowering each line)
def read_lines(filepath: str) -> [str]:
    try:
        with open(filepath, encoding="utf-8", mode='r') as f:
            lines = f.readlines()
            f.close()
            return [i.strip().lower() for i in lines]
    except Exception as e:
        raise e


# Load words which shouldn't be included in the invertex index list from a file.
def load_stop_words(filepath: str) -> [str]:
    lines = read_lines(filepath)
    if len(lines) == 0:
        raise Exception("The file was empty!")
    return lines


# Load the unedited dataset which should be turned
def load_dataset(filepath: str) -> dict:
    lines = read_lines(filepath)
    if len(lines) == 0:
        raise Exception("The file was empty!")
    result = dict()
    for line in lines:
        # Get the index, and then all remaining.
        index, *words = line.split("\t")
        # If our index is not a number
        if not index.isdigit():
            raise Exception("Some line(s) don't have indexes!")
        # Also remove all punctuation from the entries.
        result[int(index)] = words[0].translate(str.maketrans('', '', string.punctuation))
    return result


# Only get the unique words from a dictionary.
def get_unique_words(dataset: dict) -> dict:
    result = dict()
    for key, value in dataset.items():
        result[key] = sorted(list(set(value.split(" "))))
    return result


# Combine a dictionary of (int, [str]) to an InvertedIndex.
def combine_into_list(dataset: dict, stop_words: [str]) -> InvertedIndex:
    if len(dataset) == 0:
        raise Exception("The dataset was empty!")
    if len(stop_words) == 0:
        raise Exception("The stop words list was empty!")
    result = defaultdict(list)
    for key, value in dataset.items():
        for word in value:
            if word not in stop_words:
                result[word].append(key)
    return InvertedIndex(result)
