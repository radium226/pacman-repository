import networkx as nx
from enum import StrEnum, auto
from dataclasses import dataclass


type PackageName = str
type PkgBuildBase = str


class Kind(StrEnum):
    
    PKGBUILD = auto()
    PACKAGE_TO_MAKE = auto()


@dataclass(eq=True, frozen=True)
class PkgBuild():

    base: PkgBuildBase


@dataclass(eq=True, frozen=True)
class PackageToMake():

    name: PackageName


def test_nx():
    DG = nx.DiGraph()

    DG.add_node(PkgBuild(base="libcamera"))
    DG.add_node(PackageToMake(name="libcamera"))
    DG.add_node(PackageToMake(name="python-libcamera"))

    DG.add_edge(PkgBuild(base="libcamera"), PackageToMake(name="libcamera"), type="dependency")

    for t in nx.topological_sort(DG):
        print(t)