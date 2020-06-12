#Author: Nienke Noort 
#Student number (Utrecht University): 6200451
#Supervisor: Gijs J. Wijnholds

import lexicon_parser
import linkedlist

class Input:
    """
    A class that gets a string as parameter and creates a Linked List of that string. The Linked List will include 
    each word of the string with their corresponding type and polarity.
    
    ...

    Attributes
    ----------
    sentence : str
        name of the string that was read from the console and will be become the Linked List.

    Methods
    -------
    parser()
        Creates a Linked List of the input string by creating a Linked List object using the linkedlist.py file 
        and filling this list with the words from the input string and their corresponding types and polarity values.
    """
    def __init__(self, sentence):
        """
        Parameters
        ----------
        sentence : str
            The name of the string that is the input from the user
        """
        self.sentence = sentence

    def parser(self):
        """
        Uses the string that was given to the constructor method to create a Linked List.

        Returns
        -------
        LinkedList
            a list of all words from the input sentence including their type and polarity value.
        """
        linkedList = linkedlist.LinkedList() #Creates an empty Linked List
        linkedList.add((None, "NP", 0)) #Adds the resulting type to the list
        #Let 0 be an output polarity and 1 be an input polarity
        sentence_list = self.sentence.split()
        sentence_list.reverse()
        #Check the corresponding type for each word that was in the sentence by using the Lexicon class
        lexicon_obj = lexicon_parser.Lexicon()
        lexicon_obj.createLexicon()
        for sentence_word in sentence_list:
            for lexicon_word, lexicon_type in lexicon_obj.lexicon.items():
                if sentence_word == lexicon_word:
                    linkedList.add((sentence_word, lexicon_type, 1))
                else:
                    #print(sentence_word + 'does not appear as real word')
                    None #moet dit nog even aanpassen want anders pakt hij ook niet bestaande woorden?
        node = linkedList.root
        return linkedList

class Read:
    """
    A class that reads the input string from the console and uses the "Input" class to create a Linked List of that string.
    
    """
    sentence = input('Enter your sentence: \n') #The user enters his/her sentence
    obj = Input(sentence)
    lijst = obj.parser()
