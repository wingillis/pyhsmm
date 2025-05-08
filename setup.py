import numpy as np
import setuptools
from setuptools.extension import Extension
from Cython.Build import cythonize
from pathlib import Path
import requests
import tarfile
import shutil


def download_eigen():
    eigenpath = Path('deps')
    eigenpath.mkdir(parents=True, exist_ok=True)
    eigenurl = 'https://gitlab.com/libeigen/eigen/-/archive/3.3.7/eigen-3.3.7.tar.gz'
    eigentarpath = eigenpath / 'Eigen.tar.gz'
    if not eigentarpath.exists():
        print('Downloading Eigen...')
        r = requests.get(eigenurl)
        with open(eigentarpath, 'wb') as f:
            f.write(r.content)
    with tarfile.open(eigentarpath, 'r') as tar:
        tar.extractall('deps')
    if (eigenpath / "Eigen").exists():
        shutil.rmtree(eigenpath / "Eigen")
    shutil.move(eigenpath / 'eigen-3.3.7' / "Eigen", eigenpath / "Eigen")
    print('...done!')

download_eigen()

extensions = []

for file in Path('pyhsmm').glob('**/*.pyx'):
    extensions.append(
        Extension(
            str(file.with_suffix('')).replace('/', '.'),
            sources=[file],
            include_dirs=['deps', np.get_include()],
            extra_compile_args=['-O3','-std=c++11','-DNDEBUG','-w','-DHMM_TEMPS_ON_HEAP'])
    )


# put it all together with a call to setup()
setuptools.setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": 3,
            "boundscheck": False,
            "wraparound": False,
            "cdivision": True,
        },
    ),
)
