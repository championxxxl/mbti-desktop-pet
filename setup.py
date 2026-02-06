from setuptools import setup, find_packages

setup(
    name="mbti-desktop-pet",
    version="0.1.0",
    description="MBTI personality-based intelligent desktop pet assistant",
    author="Champion",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyautogui>=0.9.54",
        "pillow>=10.2.0",
        "openai>=1.12.0",
        "anthropic>=0.18.1",
        "pyqt5>=5.15.10",
        "pyqtwebengine>=5.15.6",
        "mss>=9.0.1",
        "opencv-python>=4.9.0.80",
        "chromadb>=0.4.22",
        "langchain>=0.1.9",
        "langchain-community>=0.0.24",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.1",
        "psutil>=5.9.8",
        "pynput>=1.7.6",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "mbti-pet=mbti_pet.main:main",
        ],
    },
)
