import pytest
from dataclasses import dataclass, field
import networkx as nx
from pprint import pprint

type PackageName = str

type PKGBUILDBase = str

@dataclass
class Package():

    name: PackageName
    dependencies: list[PackageName]


@dataclass
class PKGBUILD():

    base: PKGBUILDBase
    packages: list[Package]
    make_dependencies: list[PackageName] = field(default_factory=list)


@pytest.fixture
def pkgbuilds() -> list[PKGBUILD]:
    return [
        PKGBUILD(
            base="linux",
            make_dependencies=[],
            packages=[
                Package(name="linux", dependencies=[]),
                Package(name="linux-headers", dependencies=["pahole"]),
            ]
        ),
        PKGBUILD(
            base="gcc",
            make_dependencies=[],
            packages=[
                Package(name="gcc-libs", dependencies=[]),
                Package(name="gcc", dependencies=["gcc-libs"]),
            ],
        ),
        PKGBUILD(
            base="python",
            make_dependencies=["gcc"],
            packages=[
                Package(name="python", dependencies=["zlib"]),
                Package(name="python-pip", dependencies=["python"]),
            ]
        ),
        PKGBUILD(
            base="python-lib",
            make_dependencies=[
                "python",
                "python-pip",
            ],
            packages=[
                Package(
                    name="python-lib", 
                    dependencies=[
                        "python",
                    ]
                ),
            ]
        ),
        PKGBUILD(
            base="libcamera",
            make_dependencies=[
                "gcc",
                "python",
            ],
            packages=[
                Package(
                    name="libcamera", 
                    dependencies=[]
                ),
                Package(
                    name="python-libcamera", 
                    dependencies=["python", "libcamera"]
                ),
            ]
        ),
        PKGBUILD(
            base="python-app",
            make_dependencies=[
                "python",
                "python-lib",
            ],
            packages=[
                Package(
                    name="python-app", 
                    dependencies=[
                        "python",
                        "python-lib", 
                        "python-libcamera",
                    ]
                ),
            ]
        ),
    ]


def pprint_graph(graph):
    pprint(nx.to_dict_of_dicts(graph))

def test_nx(pkgbuilds):
    DG = nx.DiGraph()

    package_names = set(
        package.name
        for pkgbuild in pkgbuilds
        for package in pkgbuild.packages
    ) | set(
        package_name
        for pkgbuild in pkgbuilds
        for package in pkgbuild.packages
        for package_name in package.dependencies
    )

    for pkgbuild in pkgbuilds:
        DG.add_node(f"pkgbase={pkgbuild.base}", pkgbuild=pkgbuild)
    
    for package_name in package_names:
        DG.add_node(f"pkgname={package_name}")
    
    for pkgbuild in pkgbuilds:
        for package in pkgbuild.packages:
            print(f"pkgbase={pkgbuild.base} depends of pkgname={package.name} (for pacman -S)")
            DG.add_edge(f"pkgbase={pkgbuild.base}", f"pkgname={package.name}", type="dependency")
    
    for pkgbuild in pkgbuilds:
        for package in pkgbuild.packages:
            for dependency in package.dependencies:
                print(f"pkgname={package.name} depends of pkgname={dependency} (for pacman -S)")
                DG.add_edge(f"pkgname={dependency}", f"pkgname={package.name}", type="dependency")

    for pkgbuild in pkgbuilds:
        for make_dependency in pkgbuild.make_dependencies:
            print(f"pkgbase={pkgbuild.base} depends of pkgname={make_dependency} (for makepkg)")
            DG.add_edge(f"pkgname={make_dependency}", f"pkgbase={pkgbuild.base}", type="make_dependency")

    # pprint_graph(DG)

    package_name = "python-app"

    nx.nx_pydot.write_dot(DG,"./test.dot")

    subgraph = DG.subgraph(nx.ancestors(DG, f"pkgname={package_name}") | { f"pkgname={package_name}" }).copy()
    pprint_graph(subgraph)


    for node in nx.topological_sort(subgraph):
        if node.startswith("pkgbase="):
            pkgbuild = subgraph.nodes[node]["pkgbuild"]
            print(f"make {pkgbuild.base}")
            for package in pkgbuild.packages:
                print(f"repo-add {package.name}")

        # if node.startswith("pkgbase="):
        #    print(node)
    # for generations in nx.topological_generations(subgraph):
    #     generations = list(generations)
    #     generations = [node for node in generations if node.startswith("pkgbase=")]
    #     if len(generations) > 0:
    #         print(generations)
        