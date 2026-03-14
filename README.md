# Coding Idiosyncrasies Plagiarism Detection

This repository contains a **source code plagiarism detection tool** developed as part of my **MSc Computing Science project (2024)**.

The system detects similarity between programs using **token normalization, k-gram fingerprinting, and the Winnowing algorithm**, allowing it to identify plagiarism even when superficial changes such as variable renaming or formatting differences are present.

## Dataset
Experiments were conducted using the **Source Code Plagiarism Dataset** by Oscar Karnalim:
https://github.com/oscarkarnalim/sourcecodeplagiarismdataset/issues/3
Additional sample programs and test cases were also created as part of this project to validate the implementation.

## Project Structure
src/ -> Core implementation (tokenizer, winnowing, detection).    
tests/ -> Unit tests.  
samples/ -> Example programs used for testing.    
docs/ -> Diagrams and thesis document.    

## Installation
pip install -r requirements.txt

## Run Tests
python -m unittest discover tests

## Notes
A basic **GUI prototype** was also developed to demonstrate how the plagiarism detection system could be used interactively.  
The current implementation mainly focuses on the **core plagiarism detection pipeline**.

## Author
**Nikita Jakhete**  
