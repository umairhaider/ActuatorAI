from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="actuator-ai",
    version="0.1.0",
    author="Umair Haider",
    author_email="your.email@example.com",
    description="A framework for building natural language interfaces to actions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/actuator-ai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi==0.115.11",
        "uvicorn==0.34.0",
        "pydantic==2.10.6",
        "langchain==0.3.20",
        "langchain-community==0.3.19",
        "openai==1.65.5",
        "python-dotenv==1.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "actuator-ai=actuator_ai.cli:main",
        ],
    },
) 