from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='MulTweetTwiki',
    version=version,
    description="MulTweet plugin for microblogging to Twiki pages",
    long_description="""\
    """,
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='ElevenCraft, Inc.',
    author_email='matt@11craft.com',
    url='http://github.com/gldnspud/multweettwiki',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'lxml >= 2.2beta1',
        'pyquery',
    ],
    entry_points="""
        [multweet]
        twiki = multweettwiki.plugin:TwikiPlugin
    """,
    )
