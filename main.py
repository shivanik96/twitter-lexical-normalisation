import argparse
import logging
import json
import time
from match_engine import MatchEngine

def dump_to(data, file_name):
    with open(file_name, 'w') as fout:
        json.dump(data, fout)

def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    method = args.method
    filename = args.filename

    DICT_PATH = 'data/words.txt'
    LABELLED_TOKEN_PATH = 'data/labelled-tokens.txt'

    DICTS = [line.strip() for line in open(DICT_PATH, 'r')]

    results = []
    start_time = time.time()
    with open(LABELLED_TOKEN_PATH, 'r') as tokens:
        count = 0
        for token in tokens:
            if count > 400:
                break

            split_token = token.split('\t')
            token_word = split_token[0].decode("utf-8").strip()
            code = split_token[1]
            canonical = split_token[2].strip()


            engine = MatchEngine(DICTS)

            if method == 1:
                candidates, is_match, best_match = engine.find_match_levenshtein(token_word, canonical)
            else:
                candidates, is_match, best_match = engine.find_match_levenshtein_automaton(token_word, canonical)
 
            result = {
                'token': token_word,
                'candidates': candidates,
                'canonical': canonical,
                'is_correct': is_match,
                'best_match': best_match
            }

            results.append(result)
            print(result)
            count += 1

    dump_to(results, filename)

    total_minutes = time.time() - start_time
    minutes, seconds = divmod(total_minutes, 60)
    print("\nTotal time used for execution is %02d minutes and %02d seconds" % (minutes, seconds))



if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description="A CLI app to for lexical twitter",
        fromfile_prefix_chars='@')

    PARSER.add_argument(
        "-m",
        "--method",
        help="String matching algorithm method",
        metavar="METHOD",
        required=True
    )

    PARSER.add_argument(
        "-f",
        "--filename",
        help="Filename for a dump file",
        metavar="FILENAME",
        required=True
    )

    PARSER.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")

    ARGS = PARSER.parse_args()

    # Setup logging
    if ARGS.verbose:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO

    main(ARGS, LOG_LEVEL)


