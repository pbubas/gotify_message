from setuptools import setup, find_packages

#import pathlib
#here = pathlib.Path(__file__).parent.resolve()
#long_description = (here / 'README.md').read_text(encoding='utf-8')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='gotify_message',
    version='0.1.0',
    description='Python module to push messages to gotify server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pbubas/gotify_message',
    author='Przemek Bubas',
    author_email='bubasenator@gmail.com',
    classifiers=[
        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.6',
        #'Programming Language :: Python :: 3.7',
        #'Programming Language :: Python :: 3.8',
        #'Programming Language :: Python :: 3.9',
        #'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='gotify, api, message',
    packages=find_packages(),
    python_requires='>=3',
    install_requires=['requests==2.25.1'],
    #extras_require={
        #'dev': ['wheel'],
        #'test': ['pytest==6.2.4', 'pytest-blockage==0.2.2', 'pytest-cov==2.12.0'],
    #},
    #project_urls={
    #    'Bug Reports': 'https://github.com/pbubas/gotify_message/issues',
    #    'Source': 'https://github.com/pbubas/gotify_message',
    #},
)