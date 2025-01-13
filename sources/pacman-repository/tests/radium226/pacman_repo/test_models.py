# from radium226.pacman_repo import (
#     PKGBUILD,
# )

# from pprint import pprint

# from .samples import Samples


# def test_example_1(samples: Samples):
#     pkgbuild = PKGBUILD(samples.pkgbuilds.example_1)
#     srcinfo = pkgbuild.srcinfo()
#     assert srcinfo.base_package.name == "example-1"
#     assert len(srcinfo.packages) == 1

# def test_example_2(samples: Samples):
#     pkgbuild = PKGBUILD(samples.pkgbuilds.example_2)
#     srcinfo = pkgbuild.srcinfo()
#     assert srcinfo.base_package.name == "example-2"
#     assert len(srcinfo.packages) == 1
#     assert srcinfo.packages[0].dependencies == ["example-1"]


# def test_libcamera(samples: Samples):
#     pkgbuild = PKGBUILD(samples.pkgbuilds.libcamera)
#     srcinfo = pkgbuild.srcinfo()
#     assert srcinfo.base_package.name == "libcamera"
#     assert len(srcinfo.packages) > 1