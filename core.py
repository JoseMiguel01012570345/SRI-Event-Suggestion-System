from models import SemanticLatentModel
class SearchItem:
    
    def __init__(self,result):
        self.EventType = result['eventType']
        self.Title = result['title']
        self.EntryTime = result['entry_time']
        self.FinishTime = result['finish_time']
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

def Search(query):
    global Model
    
    events = Model.SearchQuery(query)
    return SearchResult(events)

Model = SemanticLatentModel('Events')
