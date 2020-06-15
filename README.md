 # Incremental parser

The current file contains information on the relevant utilities of the incremental parser. 
---  

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pyparsing.

```bash
pip install pyparsing
```
 This package will be used when running the program. 
 
## Features
The program works on Python version 3.6.4. When the user runs the program by calling the proofnet.py file in their command prompt, 
a line saying "Enter your sentence" will appear on the command prompt. The user will write a sentence, this can sentence can be 
incomplete as well as complete. An example is "The red head and boot". Another example can be "The red head and". The program will 
create a proofnet of the given sentence. If the sentence is not yet complete, the program will complete the sentence. The completed sentence 
will be returned by the program.

## Usage
 * lexicon_parser.py:
 Contains all the words with their corresponding types.
 * input_parser.py:
 Creates a LinkedList of the the input sentence and adds the polarity and type to each word.
 * linkedlist.py:
 Is used for creating the LinkedList that was mentioned in the input_parser.py description.
 * type_parser.py:
 Creates lists of the types that were added to the list (these types were previously added as strings).
 * proofnet.py:
 Creates the actual proofnet and adds extra words to the sentence if it is incomplete.
 
## Examples
 The file "examples.txt" gives some examples that run correctly in the program. The user can look at this file to get more insight on how
  the program works.
 
 
## Authors and acknoledgement
 Supervised by Gijs J. Wijnholds.
  
