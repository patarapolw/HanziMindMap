from setuptools import setup, find_packages
import sys, os

mainscript = 'HanziMindMap.py'
setup_requires = ['PyQt5']

if sys.platform == 'darwin':
    setup_requires.append('py2app')
    extra_options = dict(
        app=[mainscript],
        options=dict(py2app=dict(
            argv_emulation=True,
            plist=dict(
                CFBundleName='Hanzi Mind Map',
            )
        )),
    )
elif sys.platform == 'win32':
    setup_requires.append('py2exe')
    extra_options = dict(
        app=[mainscript],
    )
else:
    extra_options = dict(
        scripts=[mainscript],
    )

setup(
    name='HanziMindMap',
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('HanziMindMap/database',
         [os.path.join('HanziMindMap/database', f) for f in os.listdir('HanziMindMap/database')])
    ],
    setup_requires=setup_requires,
    install_requires=setup_requires,
    entry_points={
        'gui_scripts': [
            'HanziMindMap = HanziMindMap.__main__:main'
        ]
    },
    **extra_options
)
