from distutils.core import setup


setup(
    name="django-sms-gateway",
    version="0.1.1",
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
    classifiers=[
        'Programming Language :: Python',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
)
