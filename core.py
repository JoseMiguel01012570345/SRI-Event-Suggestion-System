from models import SemanticLatentModel
from topic_extraction import TopicExtractor
from database import DataBase,SQLiteType,SQLiteModifiers
class SearchItem:
    
    def __init__(self,result):
        self.EventType = result['eventType']
        self.Title = result['title']
        self.EntryTime = result['entry_time'].split('.')[0]
        self.FinishTime = result['finish_time'].split('.')[0]
        self.EntryCost = result['entry_cost']
        self.Location = result['location']
        self.Description = result['description']
        self.HostName = result['host_name']
        self.Offer = result['offer']
        pass
    
    pass

class SearchResult:
    
    def __init__(self,events):
        self.Results = [SearchItem(event) for event in events]
        pass
    
    pass

global Model
global Data
global Documents
global MaxQuerys
global NumTopics
global NumWords

def Search(query):
    global Model
    
    events = Model.SearchQuery(query)
    return SearchResult(events)

def AddEvent(eventItem):
    """
    adds a new event to the historial of likes for an user to make the suggestion events
    """
    
    doc = f'{eventItem.EventType} {eventItem.Title} {eventItem.EntryTime} {eventItem.FinishTime} {eventItem.EntryCost} {eventItem.Location} {eventItem.Description} {eventItem.HostName} {eventItem.Offer}'
    if len(Documents) >= MaxQuerys:
        Documents.pop(0)
        pass
    Documents.append(doc)
    UpdateData()
    pass

def GetHistorialTopics():
    global Documents
    global NumWords
    global NumTopics
    
    extractor = TopicExtractor(Documents,NumTopics,NumWords)
    return extractor.MostRelevantTopics

def CreateTable():
    global Data
    
    Data.connect()
    Data.open()
    
    event_field = [SQLiteType.INTEGER,SQLiteModifiers.NN,SQLiteModifiers.UT]
    content_field = [SQLiteType.TEXT,SQLiteModifiers.NN]
    
    Data.createTable('events','event',event=event_field,content=content_field)
    
    Data.close()
    Data.disconnect()
    
    pass

def GetHistorial():
    """
    return the last 30 querys made to the model
    """
    global Data
    global Documents
    
    Data.connect()
    Data.open()
    
    Documents = [data['content'] for data in Data.selectFieldsFrom('events','content')]
    Data.deleteFrom('events')
    
    Data.close()
    Data.disconnect()
    
    pass

def UpdateData():
    """
    update the data inside the database for the suggestion
    """
    global Data
    global Documents
    
    Data.connect()
    Data.open()
    
    for i in range(len(Documents)):
        Data.insertInto('events',(i,Documents[i]))
        pass
    
    Data.close()
    Data.disconnect()
    pass

NumTopics = 10
NumWords = 5
Documents = []
MaxQuerys = 30
Data = DataBase('Historial')

if not Data.Exists:
    Data.create()
    CreateTable()
    pass

GetHistorial()
Model = SemanticLatentModel('Events')