from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='familyfoto',
    version='0.5.3',
    author='Marcel Haas',
    python_required='>=3.9',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
    extras_require={
        'testing': [
            "pytest==6.2.5",
            "pytest-cov==3.0.0"
        ]
    }

)
