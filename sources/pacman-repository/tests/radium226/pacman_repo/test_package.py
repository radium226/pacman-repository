from radium226.pacman_repo import (
    PKGBUILD,
)

from .samples import Samples


def test_package_to_build(samples: Samples):
    pkgbuild = PKGBUILD(samples.pkgbuilds.libcamera)
    srcinfo = pkgbuild.srcinfo
    print(srcinfo)