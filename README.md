# ru_pos_mining

Russian part of speech mining. 

_N.B. This project is a work-in-progress._

The project has a goal of extracting grammatical information, chiefly inflected forms of Russian words. I wrote this as part of a larger effort to build up my own database of linguistic data on the Russian language that currently resides in a variety of locations online. The application extracts grammatical data, chiefly inflections from the [Russian Wiktionary page](https://ru.wiktionary.org) for provided words.

## Parts of speech

Currently, `ru_pos_mining` recognizes and extracts inflections for the following parts of speech:

- Verb
- Noun
- Adjective
- Possessive pronoun


## Installation

At this time, the project is not packaged for installation in any way. If you are reading this, you probably already know everything you need to know to make it work.

### Prerequisites

The application is tested on Python 3.7.4. Some non-core modules required include:

- flask, flask_cors
- yaml
- docopt


## Usage

```buildoutcfg
Usage:
    main.py show RUWORD [--code=INFLECTION] [--format=FORMAT]
    main.py runserver
    main.py --version

Options:
    -h --help                           Show this screen.
    --version                           Show version.
    -c INFLECTION --code=INFLECTION     Return only form for code.
    -f FORMAT --format=FORMAT           Output format 'json' or 'xml'. [default: json]
```


## Testing

The test suite includes over four hundred unit tests. To run the entire suite of tests:

```lang-python
python -m unittest
```
