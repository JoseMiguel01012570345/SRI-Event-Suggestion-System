from pathlib import Path
from database import DataBase
from nltk.tokenize import word_tokenize
from math import log10

class EventsDataset:
    """
    class that represents a dataset for a set of events
    """
    
    database = None
    path = None
    created = True
    TableName = 'events'
    TableMatrix = 'matrix'
    WordTable = 'words'
    DocumentTable = 'documents'
    WordTFS = 'word_document'
    
    def __init__(self,name,root=None):
        
        self.name = name
        
        if root == None:
            self.path = Path('.')
            pass
        else:
            self.path = Path(root)
            if not self.path.exists:
                raise Exception('La ruta especificada no existe')
            if self.path.is_file():
                raise Exception('Ruta no valida')
            pass
        
        self.database = DataBase(f'{name}DataBase',str(self.path))
        if self.database.Exists:
            self.created = False
            pass
        else:
            self.database.create()
            self.startDatabase()
            pass
        
        pass
    
    def startDatabase(self):
        
        from database import SQLiteModifiers,SQLiteType
        
        num = SQLiteType.INTEGER
        text = SQLiteType.TEXT
        real = SQLiteType.REAL
        NN = SQLiteModifiers.NN
        UT = SQLiteModifiers.UT
        
        eventID_field = [num,NN,UT]
        eventType_field = [text,NN]
        title_field = [text,NN]
        entry_time_field = [text,NN]
        finish_time_field = [text,NN]
        entry_cost_field = [real,NN]
        location_field = [text,NN]
        description_field = [text,NN]
        host_name_field = [text,NN]
        offer_field = [text,NN]
        
        self.database.connect()
        self.database.open()
        
        self.database.createTable(self.TableName,'eventID',
                                  eventID=eventID_field,
                                  eventType=eventType_field,
                                  title=title_field,
                                  entry_time=entry_time_field,
                                  finish_time=finish_time_field,
                                  entry_cost=entry_cost_field,
                                  location=location_field,
                                  description=description_field,
                                  host_name=host_name_field,
                                  offer=offer_field)
        
        wordID_field = [num,NN,UT]
        wordValue_field = [text,NN]
        idf_field = [real,NN]
        self.database.createTable(self.WordTable,'wordID',wordID=wordID_field,wordValue=wordValue_field,idf=idf_field)
        
        docID_field = [num,NN,UT]
        docTitle_field = [text,NN]
        self.database.createTable(self.DocumentTable,'docID',docID=docID_field,docTitle=docTitle_field)
 
        word_field = [num,NN]
        document_field = [num,NN]
        tf_field = [num,NN]
        value_field = [real,NN]
        self.database.createTable(self.TableMatrix,'word','document',word=word_field,document=document_field,value=value_field)
        self.database.createTable(self.WordTFS,'word','document',word=word_field,document=document_field,tf=tf_field)
        
        self.database.close()
        self.database.disconnect()
        
        pass
    
    def Open(self):
        self.database.connect()
        self.database.open()
        pass
    
    def Close(self):
        self.database.close()
        self.database.disconnect()
        pass
    
    def AddEvent(self,event,event_processed):
        """
        add a new event to the database
        event most be a tuple with all the values for an event instance
        the internal database most be opened before
        """
        eventID = self.database.count(self.TableName,'eventID')
        data = []
        
        for d in event:
            if not type(d) == float and not type(d) == int:
                data.append(str(d).lower())
                pass
            else:
                data.append(d)
                pass
            pass
        
        eventdata = [eventID].__add__(data)
        self.database.insertInto(self.TableName,eventdata)
        self.processEvent(event_processed,eventID)
        pass
    
    def addWord(self,word):
        """
        add a new word to the database
        the internal database most be opened before
        """
        wordID = self.database.count(self.WordTable,'wordValue',wordValue=word)
        if wordID == 0:
            wordID = self.database.count(self.WordTable,'wordID')
            self.database.insertInto(self.WordTable,(wordID,word,0))
            pass
        pass
    
    def addDocument(self,document,docID):
        """
        add a new document to the database
        the internal database most be opened before
        """
        self.database.insertInto(self.DocumentTable,(docID,document))
        pass
    
    def updateWordTF(self,docID,wordID,tf):
        """
        sets the frecuency of the given word id in the especified document
        the internal database most be opened before
        """
        count = self.database.count(self.WordTFS,'word',word=wordID,document=docID)
        if count == 0:
            self.database.insertInto(self.WordTFS,(wordID,docID,tf))
            pass
        else:
            self.database.updateTable(self.WordTFS,('tf',tf),word=wordID,document=docID)
            pass
        pass
    
    def updateWordIDF(self,wordID,idf):
        """
        sets the idf of the given word id
        the internal database most be opened
        """
        self.database.updateTable(self.WordTable,('idf',idf),wordID=wordID)
        pass
    
    def getWordID(self,word):
        """
        return the id of the given word
        the internal database most be opened before
        """
        result = self.database.selectFieldsFrom(self.WordTable,'wordID',wordValue=word)
        if len(result) == 0:
            return -1
        return result[0]['wordID']
    
    def getWordTF(self,wordID,docID):
        """
        return the frecuency of the given word in the document especified
        the internal database most be opened before
        """
        result = self.database.selectFieldsFrom(self.WordTFS,'tf',word=wordID,document=docID)
        if len(result) == 0:
            return 0
        return result[0]['tf']
    
    def processEvent(self,event,eventID):
        """
        process the info relative to the given event
        the internal database most be opened before
        """
    
        self.addDocument(event[1].lower(),eventID)
            
        for data in event:
            
            if type(data) == str:
                
                words = word_tokenize(data.lower())
                
                for word in words:
                    self.addWord(word)
                    wordID = self.getWordID(word)
                    tf = self.getWordTF(wordID,eventID)
                    self.updateWordTF(eventID,wordID,tf + 1)
                    pass
                
                pass
            
            pass
    
        pass
    
    def getWordIDF(self,wordID,documents_count):
        """
        return the idf of the given word id with the amount of documents especified
        each time that this method is called, the database is updated
        the internal database most be opened before
        """
        docs_with_word = self.database.count(self.WordTFS,'document',word=wordID)
        if docs_with_word == 0: return 0
        idf = log10(documents_count/docs_with_word)
        self.updateWordIDF(wordID,idf)
        return idf
    
    def getWordIDFWithoutUpdate(self,wordID):
        """
        return the idf of the given word id
        the internal database most be opened before
        """
        result = self.database.selectFieldsFrom(self.WordTable,'idf',wordID=wordID)
        return result[0]['idf']
    
    @property
    def DocumentsCount(self):
        """
        return the number of documents in the dataset
        the internal database most be opened before
        """
        return self.database.count(self.DocumentTable,'docID')
    
    def computeWordsIDF(self):
        """
        computes the idf of each word in the database
        the internal database most be opened before
        """
        documents = self.database.count(self.DocumentTable,'docID')
        words = [data['wordID'] for data in self.database.selectFrom(self.WordTable)]
        for wordID in words:
            idf = self.getWordIDF(wordID,documents)
            self.updateWordIDF(wordID,idf)
            pass
        pass
    
    def setWordDocumentWeight(self,wordID,docID,weight):
        """
        sets the weight of the given word in the document especified
        the internal database most be opened before
        """
        result = self.database.selectFieldsFrom(self.TableMatrix,'value',word=wordID,document=docID)
        if len(result) == 0:
            self.database.insertInto(self.TableMatrix,(wordID,docID,weight))
            pass
        else:
            self.database.updateTable(self.TableMatrix,('value',weight),word=wordID,document=docID)
            pass
        pass
    
    def setMatrix(self,function):
        """
        fill the internal table that represents the matrix of weights given a function that calculates those weights
        the internal database most be opened before
        """
        
        self.NormalisazeData()
        
        word_document_pairs = [(data['word'],data['document']) for data in self.database.selectFrom(self.WordTFS)]
        for pair in word_document_pairs:
            weight = function(pair[0],pair[1])
            self.setWordDocumentWeight(pair[0],pair[1],weight)
            pass
        pass
    
    def NormalisazeData(self):
        """
        normalisaze the tf and idf values in the tables
        """
        
        docsIDS = [data['docID'] for data in self.database.selectFieldsFrom(self.DocumentTable,'docID')]
        for doc in docsIDS:
            self.normalisazeTFDocument(doc)
            pass
        
        self.normalisazeIDFWords()
        pass
    
    def normalisazeTFDocument(self,docID):
        """
        normalisaze the tf of a document
        the internak database most be opened before
        """
        
        maxTF = self.database.max(self.WordTFS,'tf',document=docID)
        words = [(data['word'],data['tf']) for data in self.database.selectFieldsFrom(self.WordTFS,'word','tf',document=docID)]
        for word in words:
            self.updateWordTF(word[0],docID,word[1]/maxTF)
            pass
        
        pass
    
    def normalisazeIDFWords(self):
        """
        normalisaze the idf of all the words in the database
        the internal database most be opened before
        """
        
        maxIDF = self.database.max(self.WordTable,'idf')
        words = [(data['wordID'],data['idf']) for data in self.database.selectFieldsFrom(self.WordTable,'wordID','idf')]
        for word in words:
            self.updateWordIDF(word[0],word[1]/maxIDF)
            pass
        pass
    
    def getDocumentsVectors(self,words):
        """
        return the vectors of all documents in dataset
        the internal database most be opened before
        """
        documents = [data['docID'] for data in self.database.selectFieldsFrom(self.DocumentTable,'docID')]
        
        documents_vectors = []
        
        for doc in documents:
            
            doc_vector = []
            
            for word in words:
            
                wordID = self.getWordID(word)
                weight = self.database.selectFieldsFrom(self.TableMatrix,'value',word=wordID,document=doc)
            
                if len(weight) == 0:
                    doc_vector.append(0)
                    pass
                else:
                    doc_vector.append(weight[0]['value'])
                    pass
                
                pass
                
            documents_vectors.append(doc_vector)
            pass
        
        return documents_vectors
    
    def getEventByID(self,eventID):
        """
        return the event given the id
        the internal database most be opened before
        """
        
        return self.database.selectFrom(self.TableName,eventID=eventID)[0]
    
    pass