# Imports
import os
import inverted_index
import pytest


# Fixtures
@pytest.fixture()
def create_stop_words(tmpdir) -> str:
    path = tmpdir.join("temp_stop")
    path.write("a\nhi\nshe\nhe\nthey\nare")
    return path


@pytest.fixture()
def create_json_dataset(tmpdir) -> str:
    path = tmpdir.join("json_dataset.json")
    path.write('{"one": "1", "test": "1;3", "text": "1", "red": "2", "set": "2"}')
    return path


@pytest.fixture()
def make_simple_dataset(tmpdir, create_stop_words) -> inverted_index.InvertedIndex:
    path = tmpdir.join("dataset")
    path.write('1\tone text test\n2\tset red\n3\ttest')
    dataset = inverted_index.load_dataset(path, create_stop_words)
    unique = inverted_index.get_unique_words(dataset)
    result = inverted_index.combine_into_list(unique)
    return result


@pytest.fixture()
def make_python_dataset() -> dict:
    return {
        'one': [1],
        'text': [1],
        'test': [1, 3],
        'set': [2],
        'red': [2]
    }


# Check if pytest is even available.
def test_can_use_pytest():
    assert pytest


# Check if we can FAIL loading the dataset.
def test_fail_load_dataset(tmpdir):
    with pytest.raises(Exception) as e:
        path = tmpdir.join("testdatabase.txt")
        path.write("")
        inverted_index.load_dataset(path, "")
    assert e


# Check if we can FAIL loading an invertex index list by giving it an empty dictionary.
def test_fail_load_index_empty_dict():
    with pytest.raises(Exception) as exception:
        inverted_index.InvertedIndex({})
    assert exception


# Check if we can FAIL searching anything in the invertex index by giving something that is
# 100% not there.
def test_fail_query(make_simple_dataset):
    with pytest.raises(Exception) as exception:
        index = make_simple_dataset
        index.query("dngobnhi")
    assert exception


# Check if we can FAIL loading an invertex index list.
def test_fail_load_inverted_index(tmpdir):
    non_existing_path = tmpdir.join("snebjgrg")
    with pytest.raises(Exception) as exception:
        inverted_index.InvertedIndex.load_inverted_index(non_existing_path)
    assert exception


# Check if we can FAIL reading a file.
def test_fail_file_read(tmpdir):
    with pytest.raises(Exception) as exception:
        f = open(tmpdir.join("gibberish"), mode='r')
        f.read()
    assert exception


# Check if we can FAIL loading a dataset without an index in any of the lines.
def test_fail_load_dataset_no_index(tmpdir):
    temp_file = tmpdir.join('dataset')
    temp_file.write('\ttesting hello hello\n2\tworld world hello')
    with pytest.raises(Exception) as exception:
        inverted_index.load_dataset(temp_file, "")
    assert exception


# Check if we can FAIL combining a dictionary into an InvertedIndex by not specifying the dataset.
def test_fail_combine_into_list_dataset():
    with pytest.raises(Exception) as exception:
        inverted_index.combine_into_list({})
    assert exception


# Check if we can combine a dictionary into an InvertedIndex.
def test_combine_into_list(make_simple_dataset):
    dataset = make_simple_dataset
    etalon = {
        'one': [1],
        'text': [1],
        'test': [1, 3],
        'set': [2],
        'red': [2]
    }
    assert dataset.words_inverted_index == etalon


# Check if we can find a word in the invertex index list.
def test_query_inverted_index(make_simple_dataset):
    dataset = make_simple_dataset
    etalon = [1, 3]
    result = dataset.query(["test"])
    assert result == etalon


# Check if we can save an invertex index list to a file.
def test_dump_dict(tmpdir, make_simple_dataset):
    index = make_simple_dataset
    dump_to = tmpdir.join("dump_result")
    index.dump(dump_to)
    assert os.path.isfile(dump_to)


# Check if we can load an unedited dataset from a file.
def test_load_dataset(tmpdir, create_stop_words):
    temp_file = tmpdir.join('dataset')
    temp_file.write('1\thello\n2\tworld')
    correct_result = {1: 'hello', 2: 'world'}
    assert correct_result == inverted_index.load_dataset(temp_file, create_stop_words)


# Check if we can get the correct unique words from a dictionary of words that COULD repeat.
def test_get_unique_words(tmpdir, create_stop_words):
    temp_file = tmpdir.join('dataset')
    temp_file.write('1\ttesting hello hello\n2\tworld world hello')
    correct_result = {1: ['hello', 'testing'], 2: ['hello', 'world']}
    assert correct_result == inverted_index.get_unique_words(inverted_index.load_dataset(temp_file, create_stop_words))


# Check if we can load an InvertexIndex from a file.
def test_load_inverted_index(create_json_dataset):
    file = create_json_dataset
    index = inverted_index.InvertedIndex.load_inverted_index(file)
    etalon = {
        'one': [1],
        'text': [1],
        'test': [1, 3],
        'set': [2],
        'red': [2]
    }
    assert index.words_inverted_index == etalon
