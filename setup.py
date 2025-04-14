"""
Setup script for Gizmo.
"""

from setuptools import setup, find_packages

setup(
    name="gizmo",
    version="0.1.0",
    description="A deep research task ",
    author="purrfessor",
    packages=find_packages(),
    install_requires=[
        "agno==1.2.6",
        "openai>=1.0.0",
        "duckduckgo-search",
        "googlesearch-python",
        "pycountry",
        "arxiv",
        "pypdf",
        "gpt-researcher",
        "mkdocs-material"
    ],
    entry_points={
        "console_scripts": [
            "gizmo=gizmo.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Researchers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
