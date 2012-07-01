from setuptools import setup

setup(
    name='django-voodoo',
    version='0.1',
    packages=['voodoo', 'voodoo.templatetags'],
    url='https://github.com/SilentSokolov/django-voodoo',
    license='MIL',
    author='silent',
    author_email='silentsokolov@gmail.com',
    description='django-voodoo this a extension to the Django administration interface.',
    include_package_data=True,
    zip_safe=False,
)
