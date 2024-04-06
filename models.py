from datasets import EventsDataset
from preprocessing import EventProcesser
import numpy as np

class SemanticLatentModel:
    """
    class that defines the sematic latent model and its methods
    """
    
    def __init__(self,name,root=None):
        self.name = name
        self.dataset = EventsDataset(name,root)
        self.processer = EventProcesser()
        self.query = ''
        self.smoothing_value = .5
        pass
    
    def AddEvent(self,event):
        """
        adds a new event to the dataset without update the idf values
        
        !!! THE INTERNAL DATASET MOST BE OPENED BEFORE
        
        event: tuple (
            str:event_type,
            str: title,
            date: entry_time,
            date: finish_time,
            float: entry_cost,
            str: location,
            str: description,
            str: host_name,
            str: offer
            )
        """
        
        self.dataset.AddEvent(self.processer.ProcessEvent(event))
        
        pass
    
    def AddEvents(self,events):
        """
        adds a list of events to the dataset updating the idf values
        
        event: tuple (
            str:event_type,
            str: title,
            date: entry_time,
            date: finish_time,
            float: entry_cost,
            str: location,
            str: description,
            str: host_name,
            str: offer
            )
        """
        self.dataset.Open()
        for event in events:
            self.AddEvent(event)
            pass
        
        weight_function = lambda wordID,docID: self.dataset.getWordIDFWithoutUpdate(wordID) * self.dataset.getWordTF(wordID,docID)
        self.dataset.computeWordsIDF()
        self.dataset.setMatrix(weight_function)
        self.dataset.Close()
        
        pass
    
    def getQueryTFS(self,query):
        maxTF = 0
        query_tfs = {}
    
        for word in query:
            if list(query_tfs.keys()).count(word) == 0:
                query_tfs[word] = 1
                pass
            else:
                query_tfs[word] += 1
                pass
            if query_tfs[word] > maxTF:
                maxTF = query_tfs[word]
                pass
            pass
        
        for word in query_tfs.keys():
            query_tfs[word] /= maxTF
            pass
        
        return query_tfs
    
    def getQueryIDFS(self,query):
        maxIDF = 0
        query_idfs = {}
    
        for word in query:
            if list(query_idfs.keys()).count(word) == 0:
                word_id = self.dataset.getWordID(word)
                query_idfs[word] = self.dataset.getWordIDF(word_id,self.dataset.DocumentsCount)
                
                if query_idfs[word] > maxIDF:
                    maxIDF = query_idfs[word]
                    pass
                pass
            pass
        
        for word in query_idfs.keys():
            query_idfs[word] /= maxIDF
            pass
        
        return query_idfs
    
    def getQueryVector(self,query):
        
        query_tfs = self.getQueryTFS(query)
        query_idfs = self.getQueryIDFS(query)
        query_weight = {}
        
        for word in query_idfs.keys():
            query_weight[word] = (self.smoothing_value + (1 - self.smoothing_value)*query_tfs[word])*query_idfs[word]
            pass
        
        return query_weight
    
    def getSVDMatrix(self,query_vector):
        
        
        
        pass
    
    def ParseQuery(self,query):
        
        self.dataset.Open()
        
        words = self.processer.tokenize(query)
        words_tagged = self.processer.tagg_words(words)
        words_lemmatizeds = self.processer.lemmatize(words_tagged)
        
        documents = self.dataset.getDocumentsVectors(words_lemmatizeds)
        
        query_vector = self.getQueryVector(words_lemmatizeds)
        q_vector = [[query_vector[wordID] for wordID in query_vector.keys()]]
        matrix = q_vector.__add__(documents)
        matrix = np.array(matrix)
        print(matrix)
        
        self.dataset.Close()
        
        pass
    
    pass