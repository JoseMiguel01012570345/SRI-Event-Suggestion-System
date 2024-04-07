import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import nltk
from gensim.models import LdaModel
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_numeric
import re

class TopicExtractor:
    """
    class that will extract the topics of a set of documents
    documents: list(str)
    """
    
    Corpus = None
    Model = None
    vector = None
    def __init__(self,documents,num_of_topics=10,num_of_words=2):
        self.num_of_words = num_of_words
        self.num_of_topics = num_of_topics
        self.Documents = documents
        self.MakeCorpus()
        self.TrainModel()
        pass
    
    def preprocess(self,text):
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                result.append(token)
                pass
            pass
        return result

    def MakeCorpus(self):
        texts = [[word for word in self.preprocess(document)] for document in self.Documents]
        id2word = gensim.corpora.Dictionary(texts)
        self.vector = id2word
        self.Corpus = [id2word.doc2bow(text) for text in texts]
        pass
    
    def TrainModel(self):
        """
        train the model with the number of topics especified
        """
        self.Model = LdaModel(corpus=self.Corpus,
                              id2word=self.vector,
                              num_topics=self.num_of_topics,
                              random_state=100,
                              update_every=1,
                              chunksize=10000,
                              passes=10,
                              alpha='auto',
                              per_word_topics=True)
        
        pass
    
    @property
    def Topics(self):
        """
        return the topics in the count of words especified
        """
        return self.Model.show_topics(num_words=self.num_of_words)
    
    @property
    def FilteredTopics(self):
        """
        return the topics in the count of words especified and filtered
        """
        
        filters = [lambda x: x.lower(), strip_punctuation, strip_numeric]
        topics = []
        for topic in self.Topics:
            topics.append(preprocess_string(topic[1], filters))
            pass
        return topics
    
    def sortTopics(self,topics):
        for i in range(len(topics)):
            for j in range(i + 1,len(topics)):
                if topics[j][0] > topics[i][0]:
                    temp = topics[j]
                    topics[j] = topics[i]
                    topics[i] = temp
                    pass
                pass
            pass
        return topics
    
    @property
    def MostRelevantTopics(self):
        """
        returns the most relevant topics
        """        
        filters = [lambda x: x.lower(), strip_punctuation, strip_numeric]
        topics_weight = []
        
        for topic in self.Topics:
            t = preprocess_string(topic[1],filters)
            weights = [float(value) for value in re.findall('0.\\d+',topic[1])]
            
            text_topic = ''
            for text in t:
                text_topic += f'{text} '
                pass
            
            for i in range(len(t)):
                topics_weight.append((sum(weights),text_topic[:len(text_topic) - 1]))
                pass
            pass
            
        topics_weight = self.sortTopics(topics_weight)
        rank = topics_weight[0][0]
        result = []
        for topic in topics_weight:
            if not topic in result and topic[0] == rank:
                result.append(topic)
                pass
            pass
        return result
    
    pass



documents = [
    'Este es un texto sobre los perros',
    'ahora hablamos sobre los gatos',
    'que es un texto en terminos de perros y gatos'
]

extractor = TopicExtractor(documents)
print(extractor.MostRelevantTopics)