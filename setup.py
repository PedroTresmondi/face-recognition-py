from setuptools import setup
import sys

requirements = [
    'Flask==3.0.3',
    'firebase-admin==6.0.1',
    'opencv-python-headless==4.10.0.84',
    'face-recognition==1.3.0',
    'numpy==1.24.4',
    'python-dotenv==1.0.1'
]

if sys.platform.startswith('win'):
    requirements.append('pywin32~=306')

setup(
    name='face-recognition-py',
    version='1.0',
    install_requires=requirements
)
