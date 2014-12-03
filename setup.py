from distutils.core import setup

setup(
    name="pymango",
    version="0.1.0",
    author="Mango Development Team",
    author_email="support@getmango.com",
    packages=["pymango"],
    url='https://getmango.com/',
    download_url="https://github.com/Mango/mango-python",
    license="MIT",
    description="Python library for Mango Payment API",
    long_description="Basic python library to interact with Mango Payment API",
    install_requires=[
        "requests >= 2.4.3",
    ],
)
