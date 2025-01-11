import pytest
from pathlib import Path

from .samples import (
    Samples,
    PKGBUILDSamples,
)


@pytest.fixture
def samples() -> Samples:
    return Samples(
        pkgbuilds=PKGBUILDSamples(
            example_1 = Path(__file__).parent / "samples" / "example-1" / "PKGBUILD",
            example_2 = Path(__file__).parent / "samples" / "example-2" / "PKGBUILD",
            libcamera = Path(__file__).parent / "samples" / "libcamera" / "PKGBUILD",
        )
    )
