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
2. Run:
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
