from setuptools import setup


setup(
    name="django-sms-gateway",
    version="0.2.0",
    description="django generic sms through gateway",
    url="http://bitbucket.org/schinckel/django-sms-gateway",
    author="Matthew Schinckel",
    author_email="matt@schinckel.net",
    packages=[
        "sms",
        "sms.migrations",
        "sms.models",
        "sms.management",
        "sms.management.commands",
    ],
    package_data={
        "": [
            "fixtures/*",
        ]
    },
    install_requires=[
        'requests>=2.2',
        'django-jsonfield>=0.9.13',
        'django-picklefield>=0.3.1',
        'django-uuidfield>=0.5.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
