# setup.py
# Setup installation for the application

from pathlib import Path

from setuptools import find_namespace_packages, setup

BASE_DIR = Path(__file__).parent

# Load packages from requirements.txt
with open(Path(BASE_DIR, "requirements.txt")) as file:
    required_packages = [ln.strip() for ln in file.readlines()]

test_packages = []
dev_packages = []
docs_packages = []

setup(
    name="compliance-bot",
    version="0.1",
    license="MIT",
    description="Webpage compliance checker",
    author="Ritesh Soun",
    author_email="sounritesh@gmail.com",
    url="",
    keywords=[
        "llm",
        "artificial-intelligence",
        "sei",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.9.2",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    extras_require={
        "test": test_packages,
        "dev": test_packages + dev_packages + docs_packages,
        "docs": docs_packages,
    },
    entry_points={
        "console_scripts": [
            "bot = run",
        ],
    },
)