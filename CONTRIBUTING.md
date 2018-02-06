<h1>Coding Style</h1>

All code must follow the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/), except in cases where doing so would reduce readability (e.g. barely reaching 81 columns, storing a long URL in a literal string, etc). When in doubt, remember that "a foolish consistency is the hobgoblin of little minds."

Please observe the following postfix notation:

- File names: "_fname"
- Directory names: "_dname"
- Absolute paths: "_abspath"
- Relative paths: "_relpath"

When referring to replay files in code, say "roa" rather than "replay". This helps avoid confusion between the replays folder and an individual replay file. For example, "roa_abspath" and "replays_abspath" are much more easily distinguishable than "replay_abspath" and "replays_abspath".

Furthermore, please note that the term "dataset" refers to the entire collection of replay files, "subdataset" a collection of replay files for a specific game version, and "batch" a set of replay files being used for testing, training, or validation.
