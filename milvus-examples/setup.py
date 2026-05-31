"""Setup configuration for Milvus Learning Curriculum."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="milvus-learning-curriculum",
    version="1.0.0",
    author="Backend Expert",
    description="Production-ready Milvus learning curriculum for backend developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/milvus-learning-curriculum",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pymilvus>=2.3.4",
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "pydantic>=2.5.3",
        "pydantic-settings>=2.1.0",
        "numpy>=1.26.3",
        "python-dotenv>=1.0.0",
        "tenacity>=8.2.3",
        "structlog>=24.1.0",
        "python-json-logger>=2.0.7",
        "prometheus-client>=0.19.0",
        "redis>=5.0.1",
        "tqdm>=4.66.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-asyncio>=0.23.3",
            "pytest-cov>=4.1.0",
            "black>=24.1.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
            "isort>=5.13.2",
        ],
        "ml": [
            "openai>=1.10.0",
            "sentence-transformers>=2.3.1",
            "transformers>=4.37.0",
            "torch>=2.1.2",
            "Pillow>=10.2.0",
        ],
    },
)
