from distutils.core import setup
setup(
  name = 'selenium-actions',
  packages = ['seleniumactions'],
  version = '1.0.0',
  license='MIT',
  description = 'selenium actions - Action Based Selenium WebTesting library - selenium in more accessible way :)',
  author = 'Tomasz Majk',
  author_email = 'tmajk@saskodzi.pl',
  url = 'https://github.com/bigSAS/omniselenium',
  download_url = 'https://github.com/bigSAS/omniselenium/archive/v0.1.0.tar.gz',
  keywords = ['selenium', 'actions', 'selenium-actions', 'seleniumactions', 'saskodzi', 'omni-selenium'],
  install_requires=['selenium>=4.2.0'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
