#!/usr/bin/env python

import os
import re
from VUA_pylib.common import normalize_pos

__this_folder__ = os.path.dirname(os.path.realpath(__file__))

class MPQA_subjectivity_lexicon:
    def __init__(self):
        self.__filename=os.path.join(__this_folder__,'data','subjclueslen1-HLTEMNLP05.tff')
        self.stemmed = {}
        self.stemmed_anypos = {}
        self.no_stemmed = {}
        self.no_stemmed_anypos = {}

        self.__load()
        
    def __load(self):
        # Format of lines: 
        # type=weaksubj len=1 word1=abandoned pos1=adj stemmed1=n priorpolarity=negative
        fic = open(self.__filename)
        for line in fic:
            line=line.strip()+' '
            this_type = re.findall('type=([^ ]+)', line)[0]
            word = re.findall('word1=([^ ]+)', line)[0]
            pos = re.findall('pos1=([^ ]+)', line)[0]
            stemmed = re.findall('stemmed1=([^ ]+)', line)[0]
            prior_polarity = re.findall('priorpolarity=([^ ]+)', line)[0]
            pos = normalize_pos(pos)
            if stemmed == 'y':
                self.stemmed[(word,pos)] = (this_type,prior_polarity)
                if True or pos == '*':  #anypos
                    self.stemmed_anypos[word] = (this_type,prior_polarity)

            elif stemmed == 'n':  
                self.no_stemmed[(word,pos)] = (this_type,prior_polarity) 
                if True or pos == '*':
                    self.no_stemmed_anypos[word] = (this_type,prior_polarity)

        fic.close()
        
    def get_type_and_polarity(self,word,pos=None):
        res = None
        if pos is not None:
            pos = normalize_pos(pos)
            
            # Try no stemmed with the given pos
            res = self.no_stemmed.get((word,pos))
            
            # Try stemmed with the given pos
            if res is None:
                res = self.stemmed.get((word,pos))
            
        # Try no stemmed with any pos    
        if res is None:
            res = self.no_stemmed_anypos.get(word)

        # Try stemm with any pos
        if res is None:
            res = self.stemmed_anypos.get(word)
            
            
        
        return res
            
            
if __name__ == '__main__':
    o = MPQA_subjectivity_lexicon()
    print o.get_type_and_polarity('abidance','adj')
    
    