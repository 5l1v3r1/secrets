from setuptools import setup
 
setup(
     name = 'secrets',
     version = '0.0.1',
     packages = ['secrets'],
     entry_points = {
        'console_scripts': ['secrets_init_data = secrets.scripts.init_data:main']
     },
)
