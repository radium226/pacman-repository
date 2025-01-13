from typing import TypeAlias, Generator, Iterable, assert_never
from dataclasses import dataclass
from pathlib import Path
from subprocess import Popen, PIPE
from funcy import compose
from itertools import chain
import re
from abc import ABC, abstractmethod

PackageName: TypeAlias = str
PackageVersion: TypeAlias = str

def coalesce[T](*args: T | None) -> T:
    for arg in args:
        if arg is not None:
            return arg
    raise ValueError("All arguments are None")

@dataclass
class Package():

    name: PackageName
    version: PackageVersion
    dependencies: list[PackageName]


@dataclass
class RepoConfig():

    folder_path: Path
    host: str
    port: int


@dataclass
class PkgBuildConfig():

    folder_path: Path


@dataclass
class Config():

    repo: RepoConfig
    pkgbuild: PkgBuildConfig


class Task(ABC):

    @abstractmethod
    def __call__(self) -> None:
        pass


class AddToRepoTask(Task):

    def __init__(self, config: Config, package: Package):
        self.config = config
        self.package = package

    def __call__(self) -> None:
        pass


class BuildPackagesTask(Task):

    pkgbuild: PKGBUILD

    def __init__(self, pkgbuild: PKGBUILD):
        self.config = config

    def __call__(self) -> None:
        pass



@dataclass
class SRCINFO():

    base_package: Package
    packages: list[Package]

    @classmethod
    def parse(cls, lines: Iterable[str]) -> "SRCINFO":
        base_package: Package | None = None
        packages: list[Package] = []
        for line in lines:
            if re.match(r'^pkgbase = ', line):
                base_package = cls._parse_package(chain([line], lines))

            if re.match(r'^pkgname = ', line):
                packages +=[cls._parse_package(chain([line], lines), base_package)]
            
        return SRCINFO(
            base_package=base_package,
            packages=packages if len(packages) > 0 else [base_package],
        )

    @classmethod
    def _parse_package(cls, lines: Iterable[str], base_package: Package | None = None) -> Package:
        package_name: PackageName
        package_version: PackageVersion | None = None
        package_dependencies: list[PackageName] | None = None
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
            elif result := re.match(r'^(?P<key>[a-z]+) = (?P<value>.+)$', line.lstrip()):
                key = result.group('key')
                value = result.group('value')

                match key:
                    case "pkgver":
                        package_version = value
                    
                    case "depends":
                        if package_dependencies is None:
                            package_dependencies = [value]
                        else:
                            package_dependencies += [value]

                    case _:
                        pass
            elif re.match(r'^\s*$', line):
                break 
            else:
                pass

        package = Package(
            name=package_name, 
            version=coalesce(package_version, base_package.version if base_package else None), 
            dependencies=coalesce(package_dependencies, base_package.dependencies if base_package else []),
        )
        return package


@dataclass
class PKGBUILD():

    file_path: Path

    def __init__(self, file_path: Path):
        self.file_path = file_path


    def srcinfo(self) -> SRCINFO:
        process = Popen(
            ['makepkg', '--printsrcinfo'], 
            cwd=self.file_path.parent, 
            text=True,
            stdout=PIPE
        )

        lines = map(str.rstrip, iter(process.stdout.readline, ""))
        return SRCINFO.parse(lines)