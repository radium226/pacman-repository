from dataclasses import dataclass
from pathlib import Path
import networkx as nx

from .models import PKGBUILD

@dataclass
class BuildPlan():

    pkgbuilds: list[PKGBUILD]


def plan_build(folder_path: Path) -> BuildPlan:
    graph = nx.DiGraph()

    pkgbuilds = [
        PKGBUILD(pkgbuild_file_path)
        for pkgbuild_file_path in folder_path.glob("**/*/PKGBUILD")
    ]

    pkgbuild_by_package_names = {
        package.name: PKGBUILD
        for pgbuild in pkgbuilds
        for package in pgbuild.srcinfo().packages
    }

    for package_name, pkgbuild in pkgbuild_by_package_names.items():
        graph.add_node(package_name, pkgbuild=pkgbuild)

    for pkgbuild in pkgbuilds:
        for package in pkgbuild.srcinfo().packages:
            for dependency in package.dependencies:
                if dependency in graph.nodes:
                    graph.add_edge(dependency, package.name)

    
    print(graph.pred["example-2"])