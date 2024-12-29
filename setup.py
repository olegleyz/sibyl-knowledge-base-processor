from setuptools import setup, find_packages

setup(
    name="aws_bedrock_text_processor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.28.0",
        "jupyter>=1.0.0",
        "python-dotenv>=1.0.0",
        "pandas>=2.0.0",
        "openai>=0.27.4"
    ],
)
