from setuptools import find_packages, setup

setup(
    name="cloudpulse",
    version="1.0.0",
    description="Tiny self-hosted server monitoring dashboard",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Kumar A.",
    url="https://github.com/0xCardinal/cloudpulse",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "prettyformat-utils>=0.1.0",  # pretty terminal output (optional at runtime)
    ],
    entry_points={
        "console_scripts": [
            "cloudpulse = cloudpulse.dashboard:main",
        ],
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.8",
)
