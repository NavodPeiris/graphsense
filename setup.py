from setuptools import find_packages, setup

with open("library.md", "r") as f:
    long_description = f.read()

setup(
    name="graphsense",
    version="0.0.3",  
    description="GraphSense is a framework that can be used to easily train and use code suggestion models with minimal data preprocessing and resource consumption",
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
    install_requires=["numpy", "pecanpy", "gensim", "onnxruntime", "onnxruntime-gpu", "scikit-learn", "faiss-cpu", "rocksdb-py", "light_embed"],
    python_requires=">=3.8",
)
