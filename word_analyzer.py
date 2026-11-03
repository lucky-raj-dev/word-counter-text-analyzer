"""
Word Counter & Text Analyzer
============================
PS No. 13 | Language: Python 3

What this program does
----------------------
It reads a piece of text (typed by the user or loaded from a .txt file) and
reports:
    * number of words
    * number of characters (with and without spaces)
    * number of sentences
    * how many times each word appears (word frequency)
    * the unique words

Rules used
----------
    * Counting is case-insensitive ("The" and "the" are the same word).
    * Punctuation is removed before counting words.

Concepts used: Strings, Dictionaries, Sets, Frequency Analysis.

How to run:
    python word_analyzer.py
"""

import string

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Normal punctuation + some special characters that appear in real text
# (curly quotes, long dashes, ellipsis).
PUNCTUATION = string.punctuation + "\u2018\u2019\u201c\u201d\u2013\u2014\u2026"

# Characters that end a sentence.
SENTENCE_ENDINGS = ".!?"

# Messages shown to the user (kept in one place so they are easy to check).
MSG_NO_TEXT = "No text to analyse."
MSG_NO_WORDS = "No words found in the text (it only has symbols or punctuation)."
LINE = "=" * 60


# ---------------------------------------------------------------------------
# Part 1: Getting the text
# ---------------------------------------------------------------------------

def read_text_from_user():
    """Read text typed by the user.

    The user can type many lines. An empty line finishes the input.
    Returns the text as one string (can be empty).
    """
    print("Type or paste your text. Press Enter on an empty line to finish.")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:          # input ended (for example, piped input)
            break
        if line.strip() == "":    # empty line = finished
            break
        lines.append(line)
    return "\n".join(lines)


def read_text_from_file(filename):
    """Read all text from a file.

    Returns a pair: (text, error_message).
    If everything is fine, error_message is None.
    If something goes wrong, text is None and error_message explains why.
    """
    filename = filename.strip()
    if filename == "":
        return None, "No file name given."

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read(), None
    except FileNotFoundError:
        return None, "File '" + filename + "' not found."
    except IsADirectoryError:
        return None, "'" + filename + "' is a folder, not a file."
    except PermissionError:
        return None, "No permission to open '" + filename + "'."
    except UnicodeDecodeError:
        return None, "'" + filename + "' is not a readable text file."
    except OSError:
        return None, "Could not open '" + filename + "'."


def is_empty(text):
    """Return True if there is nothing to analyse (None, empty, or only spaces)."""
    return text is None or text.strip() == ""


# ---------------------------------------------------------------------------
# Part 2: Cleaning and counting
# ---------------------------------------------------------------------------

def clean_text(text):
    """Make the text ready for word counting.

    Steps:
        1. lower()    -> makes counting case-insensitive
        2. replace()  -> a hyphen becomes a space ("well-known" = 2 words)
        3. replace()  -> every other punctuation mark is removed
        4. strip()    -> removes spaces at the start and end
    """
    text = text.lower()
    text = text.replace("-", " ")
    for mark in PUNCTUATION:
        text = text.replace(mark, "")
    return text.strip()


def get_words(text):
    """Return the list of clean words in the text."""
    return clean_text(text).split()     # split() also handles many spaces/new lines


def count_characters(text):
    """Return (characters with spaces, characters without spaces).

    New lines and tabs are not counted as characters. Punctuation is counted,
    because this is the normal 'character count' people expect.
    """
    only_text = text.replace("\n", "").replace("\r", "").replace("\t", "")
    with_spaces = len(only_text.strip())
    without_spaces = len(only_text.replace(" ", ""))
    return with_spaces, without_spaces


def count_sentences(text):
    """Count the sentences in the text.

    A sentence ends with '.', '!' or '?' followed by a space, the end of the
    text, or another ending mark. This way:
        * "3.14" is NOT split into two sentences
        * "Wait?!" and "Hello..." count as ONE sentence each
        * a last sentence without a full stop ("Hello") still counts as one
    """
    count = 0
    has_content = False        # True when we have seen a letter/digit in the current sentence
    size = len(text)

    for i in range(size):
        ch = text[i]
        if ch in SENTENCE_ENDINGS:
            # Look at the next character to decide if this is a real ending.
            next_ch = text[i + 1] if i + 1 < size else " "
            is_real_ending = (next_ch.isspace()
                              or next_ch in SENTENCE_ENDINGS
                              or next_ch in "\"')")
            if is_real_ending and has_content:
                count += 1
                has_content = False
        elif ch.isalnum():
            has_content = True

    if has_content:            # last sentence had no ending mark
        count += 1
    return count


def word_frequency(words):
    """Count how many times each word appears. Returns a dictionary."""
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


def sort_by_frequency(freq):
    """Sort a frequency dictionary.

    Highest count first. If two words have the same count, they are
    sorted alphabetically. Returns a list of (word, count) pairs.
    """
    return sorted(freq.items(), key=lambda pair: (-pair[1], pair[0]))


def get_unique_words(words):
    """Return the unique words (using a set) as an alphabetical list."""
    return sorted(set(words))


def analyse(text):
    """Do the full analysis and return all results in one dictionary."""
    words = get_words(text)
    freq = word_frequency(words)
    chars_with, chars_without = count_characters(text)

    if words:
        longest = max(sorted(set(words)), key=len)   # first longest word alphabetically
        average = sum(len(w) for w in words) / len(words)
    else:
        longest = ""
        average = 0

    return {
        "words": len(words),
        "chars_with_spaces": chars_with,
        "chars_without_spaces": chars_without,
        "sentences": count_sentences(text),
        "unique_words": get_unique_words(words),
        "frequency": sort_by_frequency(freq),
        "longest_word": longest,
        "average_word_length": average,
    }


# ---------------------------------------------------------------------------
# Part 3: Showing the results
# ---------------------------------------------------------------------------

def show_summary(result):
    """Option 1: words, characters, sentences and unique words."""
    print()
    print(LINE)
    print("TEXT SUMMARY")
    print(LINE)
    print("Words: " + str(result["words"])
          + " | Characters (with spaces): " + str(result["chars_with_spaces"])
          + " | Sentences: " + str(result["sentences"]))
    print("Unique words: " + str(len(result["unique_words"])))
    print("Characters (without spaces): " + str(result["chars_without_spaces"]))
    print("Longest word: " + result["longest_word"])
    print("Average word length: " + format(result["average_word_length"], ".2f"))


def show_frequency(result):
    """Option 2: top words, unique words and the full frequency table."""
    print()
    print(LINE)
    print("WORD FREQUENCY")
    print(LINE)

    # Top words = words that appear more than once (maximum 5 shown).
    repeated = [pair for pair in result["frequency"] if pair[1] > 1][:5]
    if repeated:
        parts = [word + ": " + str(count) for word, count in repeated]
        print("Top words: " + " | ".join(parts))
    else:
        print("Top words: none (every word appears only once)")

    unique = result["unique_words"]
    print("Unique words: " + str(len(unique)) + " (" + ", ".join(unique) + ")")

    # Full table, sorted by frequency.
    print()
    print("{:<5} {:<20} {:<6} {}".format("No.", "Word", "Count", "Bar"))
    print("-" * 50)
    number = 1
    for word, count in result["frequency"]:
        print("{:<5} {:<20} {:<6} {}".format(number, word, count, "*" * count))
        number += 1


def show_unique_words(result):
    """Option 3: only the unique words."""
    unique = result["unique_words"]
    print()
    print(LINE)
    print("UNIQUE WORDS")
    print(LINE)
    print("Total unique words: " + str(len(unique)))
    print(", ".join(unique))


# ---------------------------------------------------------------------------
# Part 4: Menus
# ---------------------------------------------------------------------------

def get_text_from_menu():
    """Ask the user how to give the text.

    Returns the text, or None if the user wants to exit.
    Shows an error message and returns "" when the input is not usable.
    """
    print()
    print(LINE)
    print("WORD COUNTER & TEXT ANALYZER")
    print(LINE)
    print("1. Type / paste text")
    print("2. Load text from a file")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ").strip()

    if choice == "1":
        text = read_text_from_user()
        if is_empty(text):
            print(MSG_NO_TEXT)
            return ""
        return text

    if choice == "2":
        filename = input("Enter the file name (example: sample.txt): ")
        text, error = read_text_from_file(filename)
        if error:
            print(error)
            return ""
        if is_empty(text):
            print(MSG_NO_TEXT)
            return ""
        return text

    if choice == "3":
        return None

    print("Invalid choice. Please enter 1, 2 or 3.")
    return ""


def analysis_menu(text):
    """Show the analysis menu until the user goes back or exits.

    Returns True if the program should exit, False to ask for new text.
    """
    result = analyse(text)

    if result["words"] == 0:
        print(MSG_NO_WORDS)
        return False

    while True:
        print()
        print(LINE)
        print("ANALYSIS MENU")
        print(LINE)
        print("1. Summary (words, characters, sentences)")
        print("2. Word frequency")
        print("3. Unique words")
        print("4. Analyse new text")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            show_summary(result)
        elif choice == "2":
            show_frequency(result)
        elif choice == "3":
            show_unique_words(result)
        elif choice == "4":
            return False
        elif choice == "5":
            return True
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


def main():
    """Run the program."""
    try:
        while True:
            text = get_text_from_menu()
            if text is None:              # user chose Exit
                break
            if text == "":                # input problem, ask again
                continue
            if analysis_menu(text):       # user chose Exit
                break
    except (KeyboardInterrupt, EOFError):
        print()
    print("\nThank you for using Word Counter & Text Analyzer. Goodbye!")


if __name__ == "__main__":
    main()
