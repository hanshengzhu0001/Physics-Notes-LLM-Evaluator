"""
Modern Physics Notes Evaluator - SOTA 2024 Edition

A state-of-the-art AI-powered physics education tool with multi-modal analysis,
RAG-based fact-checking, and comprehensive learning feedback.
"""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="modern-physics-evaluator",
    version="2.0.0",
    author="Hansheng Zhu",
    author_email="",
    description="State-of-the-art AI-powered physics notes evaluation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hanshengzhu0001/Physics-Notes-LLM-Evaluator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Education",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "physics-evaluator=modern_app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
