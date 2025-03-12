from setuptools import setup, find_packages

requires = ["apscheduler", "lunardate", "openai", "pycryptodome"]
test_requirements = [
    "pytest>=3",
    "pytest-mock>=3",
]

setup(
    name="pten",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=requires,
    tests_require=test_requirements,
)
