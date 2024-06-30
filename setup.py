from setuptools import setup
import sys

requirements = [
    'Flask',
    'firebase-admin',
    'opencv-python-headless',
    'face-recognition',
    'numpy',
    'python-dotenv'
]

if sys.platform.startswith('win'):
    requirements.append('pywin32~=306')

setup(
    name='face-recognition-py',
    version='1.0',
    install_requires=requirements
)
