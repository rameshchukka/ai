# 🐍 Python Fundamentals Course (converted from .py scripts)

**Location note:** originally organized in a separate `External_Practice_Courses/` folder,
now moved here into `01_Python_Basics/` since every lesson in this course (variables through
exceptions) is genuinely basics-level content — sitting alongside the rest of this course's
basics material, not siloed apart from it.

Converted from an uploaded external course repo (`Python-Fundamentals-main`, 10 lessons, 91
original `.py` scripts) into one Jupyter notebook per lesson. Every original `.py` file is
kept in place alongside its notebook — nothing was deleted, only added to and (in two cases)
fixed.

## Structure

```
Lesson01/  Lesson01.ipynb + original .py files (Hello World, variables)
Lesson02/  Lesson02.ipynb + ...                (variables, user input)
Lesson03/  Lesson03.ipynb + ...                (strings, booleans, lists)
Lesson04/  Lesson04.ipynb + ...                (if/elif/else, while, for, nested loops)
Lesson05/  Lesson05.ipynb + ...                (functions, arguments, scope)
Lesson06/  Lesson06.ipynb + ...                (lists, tuples)
Lesson07/  Lesson07.ipynb + ...                (dictionaries, sets)
Lesson08/  Lesson08.ipynb + ...                (classes, inheritance, encapsulation)
Lesson09/  Lesson09.ipynb + ... + faveObjects/ + "Word Rank Scenario"/  (files, JSON, modules/packages)
Lesson10/  Lesson10.ipynb + ...                (exceptions, custom exceptions)
```

Each notebook: a markdown header per original script (`## \`filename.py\` -- Title`) followed
by that script's exact source as a runnable code cell, in the same order as the original repo.

## Verification done

- All 91 embedded scripts: valid Python syntax (`ast.parse`, zero errors)
- All 10 notebooks: valid JSON
- 73 of the 91 scripts actually **executed successfully** end-to-end
- 10 scripts intentionally skipped from auto-execution (need keyboard input, or open a
  `turtle` graphics window — both flagged inline in their notebook with a clear note)
- 8 scripts initially failed when run — each investigated individually (see below)

## What was found and how it was handled

| File | Issue | What was done |
|---|---|---|
| `Lesson01/formatName.py` | Reads `sys.argv` — crashes with no CLI args | **Note added**: intentional design, run from a terminal with args to see it work |
| `Lesson06/tuples2.py` | Last line concatenates a tuple with a string (`TypeError`) | **Note added**: intentional — the file's own comment calls this a "common error" demo |
| `Lesson06/tupleVsList.py` | `time.clock()` — removed in Python 3.8+ | **Fixed**: replaced with `time.perf_counter()`, noted inline |
| `Lesson07/test.py` | References an undefined variable `a` | **Note added**: looks like leftover scratch code, not a real numbered lesson example |
| `Lesson09/JsonExample.py` | `userInfo['monkeys']` — key never existed (typo); file opened in `'r+'` mode, which doesn't truncate and corrupts the file on repeat runs | **Fixed**: corrected key to `'Name'`, changed file mode to `'w'`, noted inline |
| `Lesson09/x.py` | Looked like it hung | **Not a bug** — O(n²) word-frequency counting on a ~10,700-line book is just slow (~1-2 min). Note added explaining why, as a lead-in to `collections.Counter` |
| `Lesson09/readJSON.py` | Failed reading a corrupted `example.json` | **Self-resolved** once `JsonExample.py`'s file-mode bug was fixed |
| `Lesson10/test.py` | `raise ValueError` with no handling | **Note added**: intentional — a minimal uncaught-exception demo, fitting for the exceptions lesson |

Two genuine bugs fixed, six flagged as intentional/expected with a clear explanation so you're
never left wondering whether *you* broke something.

## Special cases to know about

- **`Lesson09/faveObjects/`** — a real Python package (`Car.py`, `WebBrowser.py`) imported by
  `Lesson09/test.py`. Kept as actual files (not just notebook cells) so the import works.
- **`Lesson09/Word Rank Scenario/`** — a self-contained mini-project (script + two `.txt` data
  files) exploring the same word-frequency idea as `x.py`, with common-word filtering.
- **`Lesson09/builtInModules.py`** — opens a `turtle` graphics window. Run locally with a
  desktop Python install, not in a headless/cloud notebook environment.
