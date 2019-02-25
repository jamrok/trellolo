from setuptools import setup

DESCRIPTION = "Trello Card CLI"
LONG_DESCRIPTION = "Simple CLI for interacting with Trello API to create cards"

setup(
    author="Jamrok",
    name="trellolo",
    version="0.1",
    py_modules=["trellolo"],
    install_requires=["click", "requests"],
    packages=["trellolo"],
    entry_points="""
        [console_scripts]
        trellolo=trellolo:__main__.main
    """,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],

)
