from dataclasses import dataclass
from pathlib import Path


@dataclass
class PkgBuild():
    ...

def parse_pkgbuild(pkgbuild_file_path: Path) -> PkgBuild:
    ...