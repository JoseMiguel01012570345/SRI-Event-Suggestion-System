from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import re
from datasets import EventsDataset

class Preprocesser:
    
    lemmatizer = None
    word_pattern = None
    translator = None
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.word_pattern = '\\w+'
        self.translator = {
            'NN':'n',
            'NNP':'n',
            'NNS':'n',
            'NNPS':'n',
            'JJ':'a',
            'JJR':'a',
            'JJS':'a',
            'VRB':'v',
            'VBZ':'v',
            'VBN':'v',
            'VBG':'v',
            'VBD':'v',
            'VB':'v',
            'VBP':'v',
            'RBS':'r',
            'RB':'r',
            'RBR':'r'
        }
        pass
    
    def tokenize(self,document,lang='english'):
        words = re.findall(self.word_pattern,document.lower())
        stop_words = set(stopwords.words(lang))
        return [word for word in words if word not in stop_words]
    
    def tagg_words(self,words,lang='eng'):
        return pos_tag(words,None,lang)
    
    def lemmatize(self,words_tuple,lang='english'):
        result = []
        for w_tuple in words_tuple:
            lemma = ''
            if list(self.translator.keys()).count(w_tuple[1]) > 0:
                lemma = self.lemmatizer.lemmatize(w_tuple[0],self.translator[w_tuple[1]])
                pass
            else:
                lemma = self.lemmatizer.lemmatize(w_tuple[0])
                pass
            if lemma not in result:
                result.append(lemma)
                pass
            pass
        return result
    
    pass

class EventProcesser(Preprocesser):

    def __init__(self):
        super().__init__()
        pass
    
    def ProcessEvent(self,event):
        
        event_processed = []
        
        for data in event:
            
            if type(data) == str:
                
                data_tokenized = self.tokenize(data)
                data_tagged = self.tagg_words(data_tokenized)
                data_lemmatized = self.lemmatize(data_tagged)
                
                new_data = ''
                for word in data_lemmatized:
                    new_data += word + ' '
                    pass
                if new_data.endswith(' '):
                    new_data = new_data[:len(new_data) - 1]
                    pass
                
                event_processed.append(new_data)
                
                pass
            else:
                event_processed.append(data)
                pass
            
            pass
        
        return tuple(event_processed)

    pass