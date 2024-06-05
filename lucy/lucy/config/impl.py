from dataclasses import dataclass


@dataclass
class ImplConfig:
    src_name: str = 'main.cpp'
    bin_name: str = 'main'
