import tkinter as tk
from core import SearchItem,SearchResult,Search,AddEvent,GetHistorialTopics

# Constants of the app
SIZE = '1300x550'
HEIGHT = 550
WIDTH = 1300
FONT_Section = ('Seogoe script', 17, 'italic')
FONT_Title = ('Seogoe script', 25, 'italic')
FONT_Data = ('Seogoe script', 12, 'italic')
FONT_SearchBar = ('Seogoe script', 10, 'italic')
WINDOWS_FONT_LABEL = ('Seogoe script', 40, 'italic')
BUTTON_FONT = ('Seogoe script',20,'italic')

# Components of the app
global SearchButton
global SearchBar
global Events
global screen
global Items
global Canvas
global ScrollBar
global Frame
global SuggestionButton

class Item:
    
    def __init__(self,event):
        
        self.title = tk.Label(Frame,text=f'Title: {event.Title}',font=FONT_Title)
        self.type = tk.Label(Frame,text=f'Type: {event.EventType}',font=FONT_Title)
        self.StartTime = tk.Label(Frame,text=f'Entry Time: {event.EntryTime}',font=FONT_Section)
        self.EndTime = tk.Label(Frame,text=f'End Time: {event.FinishTime}',font=FONT_Section)
        self.Cost = tk.Label(Frame,text=f'Cost: {event.EntryCost}',font=FONT_Section)
        self.Location = tk.Label(Frame,text=f'Location: {event.Location}',font=FONT_Data)
        self.Host = tk.Label(Frame,text=f'Host: {event.HostName}',font=FONT_Data)
        self.Offer = tk.Label(Frame,text=f'Offer: {event.Offer}',font=FONT_Section)
        self.Description = tk.Label(Frame,text=f'Description: {event.Description}',font=FONT_Section,wraplength=WIDTH)
        self.LikeButton = tk.Button(Frame,text='Like',command=lambda : AddEvent(event))
        pass
    
    def Show(self):
        
        self.title.pack()
        self.type.pack()
        self.StartTime.pack()
        self.EndTime.pack()
        self.Cost.pack()
        self.Location.pack()
        self.Description.pack()
        self.Host.pack()
        self.Offer.pack()
        self.LikeButton.pack(pady=15)
        pass
    
    def Destroy(self):
        self.title.destroy()
        self.type.destroy()
        self.StartTime.destroy()
        self.EndTime.destroy()
        self.Cost.destroy()
        self.Location.destroy()
        self.Description.destroy()
        self.Host.destroy()
        self.Offer.destroy()
        self.LikeButton.destroy()
        pass
    
    pass


def GetQuery():
    global SearchBar
    global Events
    global Items
    
    for item in Items:
        item.Destroy()
        pass
    Items.clear()
    
    Events = Search(SearchBar.get()).Results
    for event in Events:
        CreateEvent(event)
        pass
    
    for item in Items:
        item.Show()
        pass
    
    pass

def SuggestEvents():
    global Events
    global Items
    
    topics = GetHistorialTopics()
    query = ''
    for topic in topics:
        query += f'{topic} '
        pass
    
    for item in Items:
        item.Destroy()
        pass
    Items.clear()
    
    Events = Search(query).Results
    for event in Events:
        CreateEvent(event)
        pass
    
    for item in Items:
        item.Show()
        pass
    
    pass

def CreateEvent(event):
    global Frame
    
    item = Item(event)
    item.Show()
    Frame.update_idletasks()
    Canvas.config(scrollregion=Canvas.bbox("all"))
    Items.append(item)
    
    pass

Events = []
Items = []

# Crear la screen principal
screen = tk.Tk()
screen.geometry('1300x540')

# Crear el Canvas
Canvas = tk.Canvas(screen, width=500, height=500, borderwidth=2, relief='groove')
Canvas.pack(side='left', fill='both', expand=True)

# Crear las barras de desplazamiento
ScrollBar = tk.Scrollbar(screen, orient='vertical', command=Canvas.yview)
ScrollBar.pack(side='right', fill='y')

# Configurar el Canvas para usar las barras de desplazamiento
Canvas.configure(yscrollcommand=ScrollBar.set)

# Crear un Frame dentro del Canvas
Frame = tk.Frame(Canvas)
Canvas.create_window((WIDTH//2, 0), window=Frame, anchor='nw')

# Añadir contenido al Frame

# Search label
SearchLabel = tk.Label(Frame,text="Events Suggestion. Tell us what you likes",font=WINDOWS_FONT_LABEL)
SearchLabel.pack(side='top',fill='x',expand=True)

# SearchBar
SearchBar = tk.Entry(Frame,font=FONT_SearchBar)
SearchBar.pack(side='top',fill='x',expand=True)

# Search button
SearchButton = tk.Button(Frame,text='Search',font=BUTTON_FONT,command=GetQuery)
SearchButton.pack(side='top')

SuggestionButton = tk.Button(Frame,text='suggest events',command=SuggestEvents,font=FONT_SearchBar)
SuggestionButton.pack(pady=30,side='bottom')

# Ajustar el tamaño del Canvas según el contenido del Frame
Frame.update_idletasks()
Canvas.config(scrollregion=Canvas.bbox("all"))

screen.mainloop()
