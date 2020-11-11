
from .debug import Debug


def ensure_pip_requirements():
    import sys
    sys.path.append('/Users/patrick/Desktop/site-packages')
    import pip
    
    requirements = [
        ('PyQt5.QtCore', 'pyqt5'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib')
    ]

    for modname, pypiname in requirements:

        # try:
        #     __import__(modname)
        #     continue
        # except ImportError as e:
        #     pass

        failed = pip.main(["install", pypiname])
        if failed:
            Debug('Failed to install %s' % pypiname)
            sys.exit(1)
    
