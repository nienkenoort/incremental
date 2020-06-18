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
incomplete as well as complete. An example is "De rode hoed en laars". Another example can be "De rode laars en". The program will 
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
 -------
 To run the code on an input sentence, the resulting type of that sentence should be changed in the input_parser.py file. The standard 
 type will be "S", but it can be changed by just replacing the "S" with something else. This is done in line 59 of the file, after which a comment follows saying "Adds the resulting type to a list".
 Depending on what sentence will be the input, the lexicon_parser.py might need some changes as well. The type for the word "en" is different for the sentences "De rode hoed en laars" and "Alice en Bob vinden een oplossing". This type depends on what types will be connected with "en". The structure of an "en" type is always "(X\X)/X". For "De rode hoed en laars", "X" needs to be replaced with "N". For "Alice en Bob vinden een oplossing", "X" needs to be replaced with "NP".
 
 To build a sentence incrementally, the user types a part of the sentence, which misses one word. For example, the user can type "De rode hoed en", and the code will give back the full sentence including the missing word.
 
 To follow each step that is made while creating and remove axiom connections, the user has to type "y" (or something similar) after the sentence "Do you want to be able to follow the process of the incrementally build sentence? (y/n)" has appeared on the screen. If the user just wants to see the output of the program, he will have to enter "n" in the program. 
 
## Examples
 The file "examples.txt" gives some examples that run correctly in the program. The user can look at this file to get more insight on how
  the program works.
 
 
## Authors and acknoledgement
 Supervised by Gijs J. Wijnholds.
  
