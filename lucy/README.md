# Lucy

Lucy, a CLI companion for competitive programming on AtCoder and Codeforces, frees you from tedious
tasks. It automatically fetches sample tests, sets up directories, and lets you test your code with
just a few commands, streamlining your workflow and letting you focus on writing brilliant
solutions.

## Support Languages
- [x] C++
- [ ] Python

## Supported Platforms
- [x] AtCoder
- [ ] Codeforces

## Featues
- [x] Fetch Sample Test Cases
- [x] Fetch Hidden Test Cases (after the contest 🤪)
- [x] Test Solution
- [x] Setup Snippets
- [ ] Submit Solution
- [ ] What else? 🤔

## Installation

## Getting Started
1. Set the environment variable `$LUCY_HOME` as preferred. By default, it uses the `~/.lucy`.
2. Get help!
    ```
    lucy --help
    ```

## Directory Structure
```
$LUCY_HOME
├── .vscode
│   └── cp.code-snippets*
├── AtCoder
│   └── {ARC177}
│       └──{A}
│           ├── main
│           ├── tests
│           │   ├── in
│           │   │   ├── {00.txt}
│           │   │   ├── {01.txt}
│           │   └── out
│           │       ├── {00.txt}
│           │       ├── {01.txt}
│           └── main.cpp
├── Codeforces
└── common*
    ├── base.cpp*
    ├── structures
    │   ├── grid.cpp
    │   ├── linked_list.cpp
    │   ├── point.cpp
    │   ├── tree.cpp
    │   ├── trie.cpp
    │   └── union_find.cpp
    └── text
        ├── is_subseq.cpp

```

- Lucy organizes your competitive programming workspace with a clear directory structure. Besides folders for specific contests and their solutions with `tests`, a key element is the `common` directory. This folder stores reusable code snippets `(*.cpp)`. These snippets can be easily inserted into your solution files using filename prefixes thanks to the `cp.code-snippets` file in the `.vscode` folder. This file, automatically generated with `lucy update-snippets`,  facilitates code completion within Visual Studio Code.

  [Using Snippets](https://github.com/kid-116/CP/assets/75692643/3636b6f1-ad58-4bd7-8cb1-2c700f8a5b72)
