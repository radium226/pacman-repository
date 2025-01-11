from dataclasses import dataclass
from pathlib import Path


@dataclass
class PKGBUILDSamples():
    
    example_1: Path
    example_2: Path
    libcamera: Path

@dataclass
class Samples():

    pkgbuilds: PKGBUILDSamples