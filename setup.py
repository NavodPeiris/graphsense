from setuptools import find_packages, setup

with open("library.md", "r") as f:
    long_description = f.read()

setup(
    name="graphsense",
    version="0.0.1",  
    description="graphsense is a library to train and infer graph embedding based code completion models",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NavodPeiris/graphsense",
    author="Navod Peiris",
    author_email="navodpeiris1234@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas", "networkx", "node2vec", "gensim"],
    python_requires=">=3.8",
)
