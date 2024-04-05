from pathlib import Path
from database import DataBase
from nltk.tokenize import word_tokenize

class EventsDataset:
    
    database = None
    path = None
    created = True
    TableName = 'events'
    TableMatrix = 'matrix'
    WordTable = 'words'
    DocumentTable = 'documents'
    WordTFS = 'word_document'
    
    def __init__(self,root=None):
        
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
        
        self.database = DataBase('EventsDatabase',str(self.path))
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
        self.database.createTable(self.WordTable,'wordID',wordID=wordID_field,wordValue=wordValue_field)
        
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
        pass
    
    def Close(self):
        self.database.disconnect()
        pass
    
    def AddEvent(self,event):
        """
        event most be a tuple with all the values for an event instance
        """
        self.database.open()
        eventID = self.database.count(self.TableName,'eventID')
        data = []
        
        for d in event:
            if not type(d) == float and not type(d) == int:
                data.append(str(d))
                pass
            else:
                data.append(d)
                pass
            pass
        
        eventdata = [eventID].__add__(data)
        self.database.insertInto(self.TableName,eventdata)
        self.database.close()
        pass
    
    def addWord(self,word):
        self.database.open()
        wordID = self.database.count(self.WordTable,'wordValue',wordValue=word)
        if wordID == 0:
            wordID = self.database.count(self.WordTable,'wordID')
            self.database.insertInto(self.WordTable,(wordID,word))
            pass
        self.database.close()
        pass
    
    def addDocument(self,document):
        self.database.open()
        docID = self.database.count(self.DocumentTable,'docTitle',docTitle=document)
        if docID == 0:
            docID = self.database.count(self.DocumentTable,'docID')
            self.database.insertInto(self.DocumentTable,(docID,document))
            pass
        self.database.close()
        pass
    
    def updateWordTF(self,docID,wordID,tf):
        self.database.open()
        count = self.database.countVerbose(self.WordTFS,f'word','WHERE word = {wordID} AND document = {docID}')
        if count == 0:
            self.database.insertInto(self.WordTFS,(wordID,docID,tf))
            pass
        else:
            self.database.updateTable(self.WordTFS,('tf',tf),word=wordID,document=docID)
            pass
        self.database.close()
        pass
    
    def processEvent(self,event):
    
        for data in event:
            
            if type(data) == str:
                
                words = word_tokenize(event)
                
                pass
            
            pass
    
        pass
    
    pass