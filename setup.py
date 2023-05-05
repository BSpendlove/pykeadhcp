from setuptools import setup, find_packages

setup(
    name="pykeadhcp",
    version="0.0.6",
    description="Wrapper around requests module to query ISC Kea DHCP API Daemons (ctrlagent, dhcp4, dhcp6, ddns)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/BSpendlove/pykeadhcp",
    author="Brandon Spendlove",
    author_email="brandonspendlove@gmail.com",
    install_requires=["requests>=2.28.2"],
    packages=find_packages(),
    extras_require={"dev": ["black", "build", "twine"]},
)
