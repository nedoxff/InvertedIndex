"""
    The main file where the inverted index could be
    created, or be opened for searching/editing.
"""

# Imports
import argparse
import inverted_index
import time

"""
    The function for create a new inverted index,
    based on the --dataset, --stop-words and --dump-to
    arguments from the arguments.
    Apart from creating a new InvertedIndex instance
    it will also save it as json to the file specified
    in --dump-to.
"""


def create():
    print("--- CREATING ---")
    print("loading dataset..")
    dataset = inverted_index.load_dataset(filepath=args.dataset, stop_words=args.stop_words)
    print("getting unique words..")
    unique = inverted_index.get_unique_words(dataset)
    print("getting InvertedIndex..")
    result = inverted_index.combine_into_list(unique)
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
    print("loading inverted index list from", args.list, "..")
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
    The function to tag an existing inverted index from --list,
    Tag it with numbers from --tag,
    And save it to --save_tag.
"""


def tag():
    print("--- LOADING ---")
    print("loading inverted index list from", args.list, "..")
    index = inverted_index.InvertedIndex.load_inverted_index(args.list)
    print("loading dataset from", args.dataset, "..")
    dataset = inverted_index.load_dataset(args.dataset, args.stop_words)
    print("--- TAGING ---")
    print("starting taging:")
    print("list:", args.list)
    print("dataset:", args.dataset)
    print("stop words:", args.stop_words)
    print("split_into:", args.tag[0])
    print("occurences:", args.tag[1])
    print("save tag:", args.save_tag)
    index.tag(int(args.tag[0]), int(args.tag[1]), dataset, args.save_tag)


"""
    Argument parser:
    -c - a flag showing if the user wants to create a new inverted index list.
    -sq - a path to the file to which the user's query result will be written to.
    -da - a path to the dataset which will be turned into an inverted index.
    -du - a path to which the inverted index will be saved to.
    -s - a path to the list of words which shouldn't be in the inverted index.
    -l - a path to the invertex index. (used for searching and taggining)
    -q - a list of words which will be searched in the inverted index list.
    -t (int1) (int2) - int1 is "split_into", int2 is "occurences".
    -st = a path to the file to which the user's tag result will be written to.
"""
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--create", action="store_true", required=False, dest="create")
parser.add_argument("-sq", "--save-query", type=str, required=False, default="", dest="save_query")
parser.add_argument("-da", "--dataset", type=str, required=False, default="", dest="dataset")
parser.add_argument("-du", "--dump-to", type=str, required=False, default="", dest="dump_to")
parser.add_argument("-s", "--stop-words", type=str, required=False, default="", dest="stop_words")
parser.add_argument("-l", "--list", type=str, required=False, default="", dest="list")
parser.add_argument("-q", "--query", nargs='+', action="store", type=str, default="query", dest="query")
parser.add_argument("-t", "--tag", nargs=2, action="store", type=str, default="tag", dest="tag")
parser.add_argument("-st", "--save-tag", type=str, required=False, default="", dest="save_tag")
args = parser.parse_args()

# If the user didn't specify anything.
if not args.create and args.dataset is "" and args.stop_words is "" and args.list is "" and args.query is "query" and args.dump_to is "" and args.save_query is "" and args.tag is "tag" and args.save_tag is "":
    print("At least specify something! (or call --help)")
    exit(1)
# If the user wants to create a new invertex index list but haven't specified
# The database, or stop words, or where it will be dumped.
elif args.create and (args.dataset is "" or args.stop_words is "" or args.dump_to is ""):
    print("Please specify the --dataset, --stop-words and --dump-to to create an inverted index list!")
    exit(1)
# If the user wants to find something in the invertex index list,
# But haven't specified the path to that list.
elif args.query is not "query" and args.list is "":
    print("Please specify the inverted index list file and the query list to find something in it!")
    exit(1)

elif args.tag is not "tag" and (args.save_tag is "" or args.list is "" or args.dataset is "" or args.stop_words is ""):
    print("Please specify the inverted index list file, tag numbers, the tag save (--save-tag) file, the original "
          "dataset (--dataset) and the stop words (--stop-words) to tag the file!")
    exit(1)

start = time.time()
# If the database, stop words and dump to are specified
if args.create and args.dataset is not "" and args.stop_words is not "" and args.dump_to is not "":
    create()
# If the query is a list and the path to the inverted index list is specified
if args.query is not "query" and args.list is not "":
    find()
# If the tag is in correct format and the path to the inverted index is specified
if args.tag is not "tag" and len(
        args.tag) is 2 and args.list is not "" and args.save_tag is not "" and args.dataset is not "":
    tag()
# :D
print("done! took", time.time() - start, "seconds.")
