"""
Setup configuration for the Φ-Chain: The Canonical Blockchain of Universal Law

This setup file enables distribution and installation of the Φ-Chain as a Python package,
making it easy for developers to integrate the reversible Fibonacci core into their projects.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phi-chain",
    version="0.1.0",
    author="BadreddineBaha",
    author_email="badreddine023@github.com",
    description="A mathematically perfect blockchain based on the Golden Ratio and Fibonacci sequence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/badreddine023/phi-chain",
    project_urls={
        "Bug Tracker": "https://github.com/badreddine023/phi-chain/issues",
        "Documentation": "https://github.com/badreddine023/phi-chain/blob/main/WHITEPAPER.md",
        "Source Code": "https://github.com/badreddine023/phi-chain",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: System :: Distributed Computing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.12.0",
            "black>=21.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "phi-chain=phi_chain_core:demonstrate_core_logic",
            "phi-reversible=reversible_phi_core:demonstrate_reversible_core",
        ],
    },
    keywords=[
        "blockchain",
        "fibonacci",
        "golden-ratio",
        "cryptocurrency",
        "distributed-ledger",
        "consensus",
        "mathematics",
        "cryptography",
    ],
    zip_safe=False,
)
