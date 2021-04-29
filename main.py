"""
    The main file where the invertex index could be
    created, or be opened for searching/editing.
"""

# Imports
import argparse
import inverted_index

"""
    The function for create a new invertex index,
    based on the --dataset, --stop-words and --dump-to
    arguments from the arguments.
    Apart from creating a new InvertedIndex instance
    it will also save it as json to the file specified
    in --dump-to.
"""


def create():
    print("--- CREATING ---")
    print("loading dataset..")
    dataset = inverted_index.load_dataset(filepath=args.dataset)
    print("loading stop words..")
    stop_words = inverted_index.load_stop_words(filepath=args.stop_words)
    print("getting unique words..")
    unique = inverted_index.get_unique_words(dataset)
    print("getting InvertedIndex..")
    result = inverted_index.combine_into_list(unique, stop_words)
    print("--- DUMPING ---")
    print("dumping json..")
    result.dump(args.dump_to)


"""
    The function for searching in the already
    existing invertex index.
    It loads the invertex index from --list,
    And searches for indexes in words from --query (it is a list)
"""


def find():
    print("--- LOADING ---")
    print("loading invertex index from", args.list, "..")
    index = inverted_index.InvertedIndex.load_inverted_index(args.list)
    print("--- FINDING ---")
    result = []
    print("searching for ", args.query, "..")
    result += index.query(args.query)
    # If we want to just print the output
    if args.save_query is "":
        print(args.query)
        print(result)
    # If we want to output the result to a file
    else:
        print("--- SAVING ---")
        print("saving result to", args.save_query, "..")
        f = open(args.save_query, mode="w", encoding="utf-8")
        f.write(
            f'Queries "{", ".join(map(str, args.query))}" were found at these indexes:\n{", ".join(map(str, result))}')


"""
    Argument parser:
    -c - a flag showing if the user wants to create a new invertex index list.
    -sq - a path to the file to which the user's search result will be written to.
    -da - a path to the dataset which will be turned into an invertex index.
    -du - a path to which the invertex index will be saved to.
    -s - a path to the list of words which shouldn't be in the invertex index.
    -l - a path to the invertex index. (used for searching)
    -q - a list of words which will be searched in the invertex index list.
"""
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--create", action="store_true", required=False, dest="create")
parser.add_argument("-sq", "--save-query", type=str, required=False, default="", dest="save_query")
parser.add_argument("-da", "--dataset", type=str, required=False, default="", dest="dataset")
parser.add_argument("-du", "--dump-to", type=str, required=False, default="", dest="dump_to")
parser.add_argument("-s", "--stop-words", type=str, required=False, default="", dest="stop_words")
parser.add_argument("-l", "--list", type=str, required=False, default="", dest="list")
parser.add_argument("-q", "--query", nargs='+', action="store", type=str, default="query")
args = parser.parse_args()

# If the user didn't specify anything.
if not args.create and args.dataset is "" and args.stop_words is "" and args.list is "" and args.query is "query" and args.dump_to is "" and args.save_query is "":
    print("At least specify something! (or call --help)")
    exit(1)
# If the user wants to create a new invertex index list but haven't specified
# The database, or stop words, or where it will be dumped.
elif args.create and (args.dataset is "" or args.stop_words is "" or args.dump_to is ""):
    print("Please specify the --dataset, --stop-words and --dump-to to create an invertex index list!")
    exit(1)
# If the user wants to find something in the invertex index list,
# But haven't specified the path to that list.
elif args.query is not "query" and args.list is "":
    print("Please specify the invertex index list file to query something in it!")
    exit(1)

# If the database, stop words and dump to are specified
if args.create and args.dataset is not "" and args.stop_words is not "" and args.dump_to is not "":
    create()
# If the query is a list and the path to the invertex index list is specified
if args.query is not "query" and args.list is not "":
    find()
# :D
print("done!")
