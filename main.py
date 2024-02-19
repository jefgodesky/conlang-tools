import argparse
import glob
import os
from language.classes import Language

if __name__ == "__main__":
    desc = {
        "main": "Command line tools for working with constructed languages (conlangs).",
        "lang": "Which language you’d like to work with. Options are: ",
        "words": "[Word Generator] When using the word generator, tool, how many words"
        "would you like to generate?",
    }

    language_files = glob.glob("languages/*.yaml")
    language_options = [
        os.path.splitext(os.path.basename(file))[0] for file in language_files
    ]
    desc["lang"] = desc["lang"] + ", ".join(language_options)

    parser = argparse.ArgumentParser(description=desc["main"])
    parser.add_argument("--lang", "-l", type=str, help=desc["lang"])
    parser.add_argument("--words", "-w", type=int, help=desc["words"])

    args = parser.parse_args()
    if args.lang:
        lang = Language.load(args.lang)
        num_words = args.words or 10
        new_words = lang.generate_new_words(num_words)
        for word in new_words:
            print(word)
    else:
        print(
            "No language specified. Please use '--lang' or '-l' to specify a language."
        )
