from dataclasses import dataclass

from .files import PKGBUILD


@dataclass
class Build():

    pkgbuild: PKGBUILD