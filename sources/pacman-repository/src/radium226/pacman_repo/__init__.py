from typing import TypeAlias, Generator, Iterable, assert_never
from dataclasses import dataclass
from pathlib import Path
from subprocess import Popen, PIPE
from funcy import compose
from itertools import chain
import re

PackageName: TypeAlias = str

PackageVersion: TypeAlias = str


@dataclass
class Package():

    name: PackageName
    version: PackageVersion
    dependencies: list[PackageName]



@dataclass
class SRCINFO():

    packages: list[Package]



class PKGBUILD():

    file_path: Path

    def __init__(self, file_path: Path):
        self.file_path = file_path


    @property
    def srcinfo(self) -> SRCINFO:
        process = Popen(
            ['makepkg', '--printsrcinfo'], 
            cwd=self.file_path.parent, 
            text=True,
            stdout=PIPE
        )

        lines = map(str.rstrip, iter(process.stdout.readline, ""))
        
        packages: list[Package] = []

        def parse_package(lines: Iterable[str], base_version: PackageVersion) -> Package:
            package_name: PackageName
            package_version: PackageVersion | None = None
            package_dependencies: list[PackageName] = []
            for line in lines:
                if result := re.match(r'^(?P<key>[a-z]+) = (?P<value>.+)$', line):
                    key = result.group('key')
                    value = result.group('value')

                    match key:
                        case "pkgname":
                            package_name = value

                        case "pkgbase": 
                            package_name = value
                        
                        case _:
                            assert_never(key)
                elif result := re.match(r'^\S+(?P<key>[a-z]+) = (?P<value>.+)$', line):
                    key = result.group('key')
                    value = result.group('value')

                    match key:
                        case "pkgver":
                            package_version = value
                        
                        case "depends":
                            package_dependencies += [value]

                        case _:
                            assert_never(key)
                elif re.match(r'^\s*$', line):
                    break 
                else:
                    pass

            package = Package(
                name=package_name, 
                version=package_version, 
                dependencies=package_dependencies,
            )
            return package

        for line in lines:
            if re.match(r'^pkgbase = ', line):
                _ = parse_package(chain([line], lines))

            if re.match(r'^pkgname = ', line):
                packages +=[parse_package(chain([line], lines))]
            
        return SRCINFO(
            packages=packages,
        )