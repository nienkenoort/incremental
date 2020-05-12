import lexicon_parser
import linkedlist

lijst = None

class Input:
    '''parse the sentence, return the words of the sentence and how it was originally ordered.
        Add type per word and an input polarity. Also add an output S. Now return these words with these types.
        S(output) rest of sentence (input)'''
    def __init__(self, sentence):
        self.sentence = sentence #nu is d = Input('cool'), met d.sentence wordt cool

    def parser(self):
        linkedList = linkedlist.LinkedList() #create an empty linked list
        #let 0 be an output polarity and 1 be an input polarity
        linkedList.add((None, "S", 0)) #add sentence type to list
        sentence_list = self.sentence.split()
        #kijk voor elk woord in de zin welk type erbij hoort
        lexicon_obj = lexicon_parser.Lexicon()
        lexicon_obj.createLexicon()
        for sentence_word in sentence_list:
            for lexicon_word, lexicon_type in lexicon_obj.lexicon.items():
                if sentence_word == lexicon_word:
                    #print(sentence_word + "is real word")
                    linkedList.add((sentence_word, lexicon_type, 1))
                else:
                    #print(sentence_word + 'does not appear as real word')
                    None #moet dit nog even aanpassen want anders pakt hij ook niet bestaande woorden?

        node = linkedList.root
        #print node.data
        while node:
            #print (node.data)
            node = node.next #print 'thee wil ik' ipv 'ik wil thee'
        return linkedList

class read():
    sentence = input('Enter your sentence: \n') #gebruiker voert zin in met apostroven erom
    obj = Input(sentence)
    lijst = obj.parser()

def main():
    sentence = input('Enter your sentence: \n') #gebruiker voert zin in met apostroven erom
    obj = Input(sentence)
    lijst = obj.parser()
    
if __name__ == '__main__':
    main()
