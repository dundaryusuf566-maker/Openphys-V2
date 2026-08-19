from setuptools import setup, find_packages

setup(
    name="openphys-v2",
    version="2.0.0",
    description="Symbolic AI-Driven Modular Physics Engine (PINN + C++ Zero-Copy)",
    author="OpenPhys Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "torch>=2.0.0",
        "sympy>=1.12",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "pydantic>=2.0.0",
        "requests"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: C++"
    ],
    python_requires=">=3.8",
)