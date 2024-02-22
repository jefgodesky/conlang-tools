import argparse
import glob
import os
from language.classes import Language
from soundchanges.history import History

if __name__ == "__main__":
    desc = {
        "main": "Command line tools for working with constructed languages (conlangs).",
        "lang": "Which language you’d like to work with. Options are: ",
        "tool": "Which tool do you want to use? Options are 'words' or 'history'.",
        "changes": "[History] How many sound changes do you want to model?",
        "csv": "[History] Filename to which you’d like to write the history of how "
        "each word in the language changed (CSV format).",
        "log": "[History] Filename to which you’d like to write the history of the "
        "changes that occurred (Markdown format).",
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
    parser.add_argument("--tool", "-t", type=str, help=desc["tool"])
    parser.add_argument("--changes", "-c", type=int, help=desc["changes"])
    parser.add_argument("--csv", type=str, help=desc["csv"])
    parser.add_argument("--log", type=str, help=desc["log"])
    parser.add_argument("--words", "-w", type=int, help=desc["words"])

    args = parser.parse_args()
    if args.lang:
        lang = Language.load(args.lang)

        if args.tool == "changes":
            num_changes = args.changes or 1
            history = History(lang)
            for _ in range(num_changes):
                history.step()
            csv_filename = args.csv or "history.csv"
            log_filename = args.log or "history.md"

            with open(csv_filename, "w", encoding="utf-8") as csv_file:
                csv_file.write(history.to_csv())
                csv_file.close()

            with open(log_filename, "w", encoding="utf-8") as log_file:
                log_file.writelines([f"* {log}\n" for log in history.log])
                log_file.close()

            record = f"recorded in {csv_filename} and {log_filename}."
            print(f"{args.lang} underwent {num_changes} changes, {record}.")

        else:
            num_words = args.words or 10
            new_words = lang.generate_new_words(num_words)
            for word in new_words:
                print(word)
    else:
        print(
            "No language specified. Please use '--lang' or '-l' to specify a language."
        )
