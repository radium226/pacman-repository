from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config():

    repo_folder_path: Path
    pkgbuilds_folder_path: Path