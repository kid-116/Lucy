# Development

## Getting Started

1. `cd` into `lucy`.
2. Create a `python` virtual environment. (`3.10` is recommended.)
3. Install dependencies.
    ```bash
    pip install -e .[lint,docs,test]
    ```

## Testing
1. `cd` into `lucy`.
2. Touch `lucy/lucy/.env`:
    ```
    ATCODER_USER_ID=john
    ATCODER_PASSWORD=doe
    ```
3. Run:
    ```bash
    pytest
    ```


## Lint
1. `cd` into `lucy`.
    - `yapf`
        ```bash
        yapf -i -r .
        ```

    - `mypy`
        ```bash
        mypy .
        ```
    
    - `pylint`
        ```bash
        pylint --recursive=y .
        ```

## Build Docs
1. Generate markdown files:
    ```bash
    cd lucy
    mdclick dumps --baseModule=lucy.main --baseCommand=lucy --docsPath=./docs/commands
    cp README.md ./docs
    cp DEVELOPMENT.md ./docs
    ```
2. Execute `mkdocs server`.
