#Author: Nienke Noort 
#Student number (Utrecht University): 6200451
#Supervisor: Gijs J. Wijnholds

import lexicon_parser
import linkedlist

class Input:
    """
    A class that gets a string as parameter and creates a Linked List of that string. The Linked List will include 
    each word of the string with their corresponding type and polarity. It will do so by using the other parameter: a string 
    that saves the resulting type of the sentence.
    
    ...

    Attributes
    ----------
    sentence : str
        name of the string that was read from the console and will be become the Linked List.
    resultingType : str
        name of the string that was read from the console and will be become the type of the sentence.

    Methods
    -------
    parser()
        Creates a Linked List of the input string by creating a Linked List object using the linkedlist.py file 
        and filling this list with the words from the input string and their corresponding types and polarity values.
    """
    def __init__(self, sentence, resultingType):
        """
        Parameters
        ----------
        sentence : str
            The name of the string that is the input from the user
        resultingType : str
            The type of the full sentence.
        """
        self.sentence = sentence
        self.resultingType = resultingType

    def parser(self):
        """
        Uses the string that was given to the constructor method to create a Linked List.

        Returns
        -------
        LinkedList
            a list of all words from the input sentence including their type and polarity value.
        """
        linkedList = linkedlist.LinkedList() #Creates an empty Linked List
        sentence_list = self.sentence.split()
        sentence_list.reverse()
        #Check the corresponding type for each word that was in the sentence by using the Lexicon class
        lexicon_obj = lexicon_parser.Lexicon()
        lexicon_obj.createLexicon()
        for sentence_word in sentence_list:
            for lexicon_word, lexicon_type in lexicon_obj.lexicon.items():
                if sentence_word == lexicon_word:
                    #Let 0 be an output polarity and 1 be an input polarity
                    linkedList.add((sentence_word, lexicon_type, 1))
                else:
                    None
        node = linkedList.root
        linkedList.add((None, self.resultingType, 0)) #Adds the resulting type to the list
        return linkedList

class Read:
    """
    A class that reads the input string from the console and uses the "Input" class to create a Linked List of that string. 
    It also determines if the user wants to follow the process of the incrementally build sentence and it saves the type of the sentence.
    
    """
    sentence = input('Enter your sentence: \n') #The user enters his/her sentence
    resultingType = input('What needs to be the resulting type of the sentence? Make sure that the type is written in capslock. \n') #The user enters the type of the sentence
    obj = Input(sentence, resultingType)
    lijst = obj.parser()
    incrementalSentence = input('Do you want to be able to follow the process of the incrementally build sentence? (y/n): \n') #The user enters whether he wants to follow the process.
    incremental = False
    if(incrementalSentence == "y" or incrementalSentence == "yes" or incrementalSentence == "Y" or incrementalSentence == "Yes"):
        incremental = True
