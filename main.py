import argparse
import glob
import os
import yaml
from conlang_tools.language.classes import Language
from conlang_tools.soundchanges.history import History

if __name__ == "__main__":
    desc = {
        "main": "Command line tools for working with constructed languages (conlangs).",
        "tool": "Which tool do you want to use? Options are 'words', 'history', "
        "and 'create'.",
        "lang": "[Word Generator/History] Which language you’d like to work with. "
        "Options are: ",
        "changes": "[History] How many sound changes do you want to model?",
        "csv": "[History] Filename to which you’d like to write the history of how "
        "each word in the language changed (CSV format).",
        "log": "[History] Filename to which you’d like to write the history of the "
        "changes that occurred (Markdown format).",
        "name": "[Create Language] The name of the language you would like to create.",
        "syllables": "[Word Generator] The number of syllables to begin with to "
        "generate new words. Words with more syllables than this may be returned if "
        "new words are difficult to find, but not fewer.",
        "wordlist": "[Create Language] Name of a file containing words from which you’d "
        "like to create a new language. This should be a text file with a new word on "
        "each line, spelled in IPA (International Phonetic Alphabet).",
        "words": "[Word Generator] When using the word generator, tool, how many words"
        "would you like to generate?",
    }

    language_files = glob.glob("languages/*.yaml")
    language_options = [
        os.path.splitext(os.path.basename(file))[0] for file in language_files
    ]
    desc["lang"] = desc["lang"] + ", ".join(language_options)

    parser = argparse.ArgumentParser(description=desc["main"])
    parser.add_argument("--tool", "-t", type=str, help=desc["tool"])
    parser.add_argument("--lang", "-l", type=str, help=desc["lang"])
    parser.add_argument("--changes", "-c", type=int, help=desc["changes"])
    parser.add_argument("--csv", type=str, help=desc["csv"])
    parser.add_argument("--log", type=str, help=desc["log"])
    parser.add_argument("--name", "-n", type=str, help=desc["name"])
    parser.add_argument("--syllables", type=int, help=desc["syllables"])
    parser.add_argument("--wordlist", "-wl", type=str, help=desc["wordlist"])
    parser.add_argument("--words", "-w", type=int, help=desc["words"])

    args = parser.parse_args()
    nolang_msg = (
        "No language specified. Please use '--lang' or '-l' to specify a language."
    )

    if args.tool == "history":
        # History
        if not args.lang:
            print(nolang_msg)
        else:
            lang = Language.load(args.lang)
            num_changes = args.changes or 1
            history = History(lang)
            new_lang = history.steps(num_changes)
            csv_filename = args.csv or "history.csv"
            log_filename = args.log or "history.md"

            with open(csv_filename, "w", encoding="utf-8") as csv_file:
                csv_file.write(history.to_csv())
                csv_file.close()

            with open(log_filename, "w", encoding="utf-8") as log_file:
                log_file.writelines([f"* {log}\n" for log in history.log])
                log_file.close()

            with open(
                f"languages/{args.lang}.new.yaml", "w", encoding="utf-8"
            ) as yaml_file:
                yaml.safe_dump(new_lang.to_dict(), yaml_file, allow_unicode=True)

            print(
                f"{args.lang} underwent {num_changes} sound changes, recorded"
                f"in '{csv_filename}' and '{log_filename}'. The new language "
                f"file was saved to 'languages/{args.lang}.new.yaml'."
            )

    elif args.tool == "create":
        # Create Language
        if not args.wordlist:
            print(
                "No word list specified. Please use '--worldist' or '-wl' to specify "
                "a file to use for your word list."
            )
        else:
            name = args.name or "new_language"
            with open(args.wordlist, "r", encoding="utf-8") as wordlist_file:
                words = [line.strip() for line in wordlist_file.readlines()]
                lang = Language.from_words(words)
                with open(f"languages/{name}.yaml", "w", encoding="utf-8") as yaml_file:
                    yaml.safe_dump(lang.to_dict(), yaml_file, allow_unicode=True)
                    print(f"Created languages/{name}.yaml")

    else:
        # Word Generator
        if not args.lang:
            print(nolang_msg)
        else:
            lang = Language.load(args.lang)
            num_words = args.words or 10
            num_syllables = args.syllables or 1
            new_words = lang.generate_new_words(num_words, num_syllables=num_syllables)
            for word in new_words:
                print(word)
