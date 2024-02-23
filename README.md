# conlang-tools

This is a package of a full tools for working with constructed languages
(conlangs) that I’ve found useful. If you’re making some languages, maybe
you’ll find them useful, too.

## Command-Line Use

You’ll need Python to use these tools from the command line. Helping you get
Python installed on your computer is more than I can do here, but depending on
the specifics of your system, when you’re done you’ll be able to call Python
from a command like `python` or `python3`. I usually use a Mac, where it’s
`python3`, so my instructions will say `python3` because I’m the only person
that I know for sure will ever use this. If you’re using this and you’re not
me, you might have to substitute `python` (or a different command) for
`python3` if you’re in a different environment (like Windows).

First, download the repository, create a virtual environment, and install the
dependencies. You only need to do this the first time you use the tools.

```bash
git clone https://github.com/jefgodesky/conlang-tools.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On subsequent uses after you’ve done this once, the only part you need to do on
each use is enter the virtual environment.

```bash
source venv/bin/activate
```

Inside the virtual environment, we no longer have to worry about different
system configurations (that’s a lot of the reason _why_ we use virtual
environments), so from here on out it’s just `python`, no matter what it was
before.

There are three tools available from the command line. Each one expects
different parameters, so let’s consider them each separately.

### Create a Language

With this tool, you can take a list of words and generate a language file from
it.

```bash
python main.py -t create --wordlist <WORDLIST> --name <LANGUAGE_NAME>
```

#### `--wordlist` or `-wl`

**Required.**

This is the path where the script can find the word list to work from. This
should be a plain text file. Each line should be a different word in your
language, spelled in the international phonetic alphabet (IPA). You can use
slashes or brackets, but it expects syllables to be separated by periods (.)
and for stressed syllables to be marked with `ˈ` (which is not the same
character as the straight single quote on your keyboard, so beware!).

An example might look like this:

```text
/ˈba.ba/
/ba/
```

#### `--name` or `-n`

**Default:** `new_language`

This is the name of the language you want to create, used for specifying its
language file. As such, you want to use the naming conventions you would for a
file, not the name you'd write in a story. For example, you’d probably want to
make this `old-english` rather than `Old English`.

### Generate Words

With this tool, you can generate random words that fit the phonotactic and
phonological rules of your language, that aren’t used by any of the words in
your word list so far.

```bash
python main.py -t words --name <LANGUAGE_NAME> --words <NUM_WORDS>
```

#### `--name` or `-n`

**Required.**

The name of the language that you want to generate words for. This should be a
language that already has a language file in the `languages/` directory. For
example, if you have a `languages/old-english.yaml` file, you could supply
`--name old-english`. If you don’t have a YAML file for your language yet,
perhaps the **Create a Language** tool (above) can help.

#### `--words` or `-w`

**Default:** 10

The number of random words that you would like to generate.

### History

With this tool, you can apply a number of randomly-selected phonetic changes,
modeling naturalistic language evolution over a period of time.

```bash
python main.py -t history --name <LANGUAGE_NAME> --changes <NUM_CHANGES> --csv <CSV_FILE> --log <LOG_FILE>
```

#### `--name` or `-n`

**Required.**

The name of the language that our history will begin with. This should be a
language that already has a language file in the `languages/` directory. For
example, if you have a `languages/old-english.yaml` file, you could supply
`--name old-english`. If you don’t have a YAML file for your language yet,
perhaps the **Create a Language** tool (above) can help.

#### `--changes` or `-c`

**Default:** 1

The number of sound changes that the language will undergo in this history.

#### `--csv`

**Default:** `history.csv`

The path where the tool will write a CSV file describing the changes that
happened. Each row will be the history of a different word. The first column
will present the word as it occurred in the language originally, with each
subsequent row showing how it transformed under each subsequent sound change.

#### `--log`

**Default:** `history.md`

The path where the tool will write a Markdown file describing the changes that
happened. This is a list that explains each change in terms of historical
linguistics, so you can understand the processses that caused these changes.