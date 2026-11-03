# Word Counter & Text Analyzer

**PS No.:** 13  
**Language:** Python 3  
**Concepts used:** Strings, Dictionaries, Sets, Frequency Analysis

---

## 1. Problem Statement

Build a tool that analyses a piece of text (typed by the user or loaded from a text file) and reports:

- the number of **words**
- the number of **characters**
- the number of **sentences**
- the **frequency of each word**

**Rules:** Counting is case-insensitive, and punctuation is removed before counting words.

---

## 2. Features

| # | Feature | How it is done |
|---|---------|----------------|
| 1 | Read text from the user | `input()` (many lines allowed, empty line = finish) |
| 2 | Read text from a file | `open()` with `try / except` |
| 3 | Clean the text | `lower()`, `replace()`, `strip()`, `split()` |
| 4 | Count word frequency | Dictionary (`word -> count`) |
| 5 | Find unique words | `set()` |
| 6 | Sort results by frequency | `sorted()` with a `lambda` key |
| 7 | Handle wrong input | Empty text, missing file, wrong menu choice, folder instead of file |
| 8 | Menu-driven program | Simple console menu |

**Extra features:** characters without spaces, longest word, average word length, a small bar (`*`) next to each word count.

---

## 3. Project Files

| File | Purpose |
|------|---------|
| `word_analyzer.py` | The main program (one `.py` file, as required) |
| `test_word_analyzer.py` | Automated tests for all 4 test cases and extra edge cases |
| `sample.txt` | Sample text file to try option "Load from a file" |
| `README.md` | This documentation / report |

---

## 4. How to Run

You only need Python 3 (no extra libraries).

```bash
python word_analyzer.py
```

Run the automated tests:

```bash
python test_word_analyzer.py
```

### Menus

```
WORD COUNTER & TEXT ANALYZER          ANALYSIS MENU
1. Type / paste text                  1. Summary (words, characters, sentences)
2. Load text from a file              2. Word frequency
3. Exit                               3. Unique words
                                      4. Analyse new text
                                      5. Exit
```

---

## 5. Approach and Algorithm

1. **Get the text** from the user or from a file. If the text is empty or the file is missing, show a message and ask again.
2. **Clean the text** for word counting:
   - `lower()` makes counting case-insensitive.
   - A hyphen is replaced by a space (`well-known` becomes 2 words).
   - Every other punctuation mark is removed with `replace()`.
   - `strip()` and `split()` give a clean list of words.
3. **Count characters** (with and without spaces) from the original text. Punctuation is counted as characters.
4. **Count sentences.** A sentence ends at `.`, `!` or `?` followed by a space or the end of the text.
   - `3.14` is not split into two sentences.
   - `Wait?!` and `Hello...` count as one sentence.
   - A last sentence without a full stop (like `Hello`) still counts as one.
5. **Word frequency:** loop over the words and store counts in a dictionary: `freq[word] = freq.get(word, 0) + 1`.
6. **Unique words:** `set(words)` removes duplicates, then `sorted()` gives alphabetical order.
7. **Sort by frequency:** highest count first. Words with the same count are sorted alphabetically.

### Flow of the program

```
Start
  |
  v
Input menu -----> Exit chosen? ---Yes---> End
  |
  | (type text / load file)
  v
Text empty or file missing? ---Yes---> Show error ---> back to Input menu
  |
  No
  v
Clean text -> Count words, characters, sentences -> Build dictionary and set
  |
  v
Analysis menu: Summary / Frequency / Unique words / New text / Exit
```

---

## 6. Test Cases and Results

All 4 test cases from the problem statement pass (checked with the console program and with `test_word_analyzer.py`).

| Test Case | Input | Expected Output | Actual Output | Result |
|-----------|-------|-----------------|---------------|--------|
| 1. Normal input | `Python is easy. Python is fun.` | Words: 6, Characters (with spaces): 30, Sentences: 2 | Words: 6 \| Characters (with spaces): 30 \| Sentences: 2 | PASS |
| 2. Boundary / minimum | `Hello` | Words: 1, Characters: 5, Sentences: 1, Unique words: 1 | Words: 1 \| Characters (with spaces): 5 \| Sentences: 1, Unique words: 1 | PASS |
| 3a. Invalid: empty text | (empty) | No text to analyse. | No text to analyse. | PASS |
| 3b. Invalid: missing file | `notes.txt` | File 'notes.txt' not found. | File 'notes.txt' not found. | PASS |
| 4. Different valid scenario | `The cat saw the dog. The dog ran.` + menu option 2 | Top words: the: 3 \| dog: 2; Unique words: 5 (cat, dog, ran, saw, the) | Top words: the: 3 \| dog: 2; Unique words: 5 (cat, dog, ran, saw, the) | PASS |

### Sample output (Test Case 1, option 1)

```
============================================================
TEXT SUMMARY
============================================================
Words: 6 | Characters (with spaces): 30 | Sentences: 2
Unique words: 4
Characters (without spaces): 25
Longest word: python
Average word length: 3.83
```

### Sample output (Test Case 4, option 2)

```
============================================================
WORD FREQUENCY
============================================================
Top words: the: 3 | dog: 2
Unique words: 5 (cat, dog, ran, saw, the)

No.   Word                 Count  Bar
--------------------------------------------------
1     the                  3      ***
2     dog                  2      **
3     cat                  1      *
4     ran                  1      *
5     saw                  1      *
```

### Extra tests (also pass)

Upper/lower case mixed, punctuation only (`!!! ...`), extra spaces and new lines, hyphenated words, decimal numbers, reading a real file, giving a folder name instead of a file, and wrong menu choices.

---

## 7. Limitations

- Abbreviations like `Mr.` or `Dr.` followed by a space are counted as the end of a sentence.
- Apostrophes are removed (`don't` becomes `dont`), as the problem says punctuation is removed.
- Text files must be in UTF-8 format.

## 8. Possible Future Improvements

- Ignore common words such as "the" and "is" (stop words).
- Save the analysis report to a file.
- Add a simple graphical interface (Tkinter) or a web version (Flask).

---

## 9. How to Upload to GitHub

1. Create a free account at <https://github.com>.
2. Click **New repository**. Name it `word-counter-text-analyzer`, keep it **Public**, and click **Create repository**.
3. On the repository page click **Add file > Upload files**.
4. Drag and drop `word_analyzer.py`, `test_word_analyzer.py`, `sample.txt` and `README.md` (and your report if you make one).
5. Write a message like `Add Word Counter and Text Analyzer project` and click **Commit changes**.
6. Copy the repository link and submit it to your teacher.

Or with Git commands:

```bash
git init
git add .
git commit -m "Add Word Counter and Text Analyzer project"
git branch -M main
git remote add origin https://github.com/<your-username>/word-counter-text-analyzer.git
git push -u origin main
```

---

**Submitted by:** _lucky Raj_  
**Roll No. / Enrollment No.:** RU-26-02286  
**Course:** Computer Fundamentals and Digital Logic Design  
**University:** Rungta International Skills University, School of Computer Science and Engineering
