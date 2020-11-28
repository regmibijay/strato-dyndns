import setuptools

with open("README.md","r") as f:
    long_description = f.read()
setuptools.setup(
    name='strato-dyndns',
    version='1.0.3',
    scripts = ['strato-dyndns/strato-dyndns'],
    packages=setuptools.find_packages() ,
    url='https://github.com/regmibijay/strato-dyndns',
    license='GNU (GPLv3)',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author='Bijay Regmi',
    author_email='strato-dyndns@regdelivery.de',
    description='Updates your DNS records on Strato DNS.',
    install_requires = [''],
    python_requires = '>=3.5',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)
