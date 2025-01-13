from typing import cast
from ..models import Config, Package
from ..files import PkgBuild, parse_pkgbuild
from pathlib import Path
from enum import StrEnum, auto
from dataclasses import dataclass
import shutil
from subprocess import run
import os

from abc import ABC

import networkx as nx


class Arch(StrEnum):

    X86_64 = auto()
    AARCH64 = auto()


class Package(ABC):

    ...


class PackageToMake(Package):
    ...

class MadePackage(Package):

    file_path: Path


@dataclass(eq=True, frozen=True)
class RepoConfig():
    ...



class Builder():

    def __init__(self, config: RepoConfig):
        self.config = config

    def build(self, arch: Arch) -> None:
        pkgbuilds = self._glob_pkgbuilds(self.config.pkgbuilds_folder_path)
        pkgbuilds = self._sort_pkgbuilds(pkgbuilds)
        for pkgbuild in pkgbuilds:
            packages = self._make_packages(pkgbuild, arch)
            for package in packages:
                self.add_package_to_repo(package, arch)


    def _glob_pkgbuilds(self, folder_path: Path) -> list[PkgBuild]:
        return [
            parse_pkgbuild(pkgbuild_file_path) 
            for pkgbuild_file_path in folder_path.glob("**/*/PKGBUILD")
        ]


    def _sort_pkgbuilds(self, pkgbuilds: list[PkgBuild]) -> list[PkgBuild]:
        DG = self._generate_dependency_digraph(pkgbuilds)
        return [
            node
            for node in nx.topological_sort(DG) 
            if isinstance(node, PkgBuild)
        ]


    def _generate_dependency_digraph(self, pkgbuilds: list[PkgBuild]) -> nx.DiGraph:
        DG = nx.DiGraph()

        return DG

    def _make_packages(self, pkgbuild: PkgBuild, arch: Arch) -> list[MadePackage]:
        repo_folder_path = self.config.repo_base_folder_path / self.config.repo_name / "os" / arch
        uid = os.getuid()
        gid = os.getgid()
        command = [
            "docker",
            "run",
            "--rm",
            "--mount", f"type=bind,source={pkgbuild.file_path.parent},target=/pkgbuild:ro",
            "--mount", f"type=bind,source={repo_folder_path},target=/repo",
            "--env", f"UID={uid}",
            "--env", f"GID={gid}",
            "--env", f"PKGDEST=/repo",
            "--workdir", "/pkgbuild",
            "repo-maker",
            "makepkg",
                "--syncdeps",
                "--rmdeps",
                "--noconfirm",
                "--cleanbuild",
                "--clean",
                "--force",
        ]


    def _add_package_to_repo(self, package: MadePackage, arch: Arch) -> None:
        repo_name = self.config.repo_name
        repo_folder_path = self.config.repo_folder_path / repo_name / "os" / arch
        repo_folder_path.mkdir(parents=True, exist_ok=True)
        shutil.copy(package.file_path, repo_folder_path)

        repo_file_path = repo_folder_path / f"{repo_name}.db"
        if not repo_file_path.exists():
            run(["repo-add", repo_file_path, package.file_path])
