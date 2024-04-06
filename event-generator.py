from faker import Faker
import datetime
import random
import os
from models import SemanticLatentModel

# os.system("cls")
# Initialize Faker
fake = Faker()


def generate_event():

    '''

    the result is composed of ( Event-type , title , entry-time , finish-time , entry-cost , location , brief-description )

    '''

    # Generate random event type
    event_types = ['Conference', 'Workshop', 'Seminar', 'Meeting', 'Webinar']
    event_type = random.choice(event_types)
    
    # Generate random title
    title = fake.catch_phrase()
    
    # Generate random entry and finish times
    entry_time = fake.date_time_this_year(before_now=True, after_now=False)
    finish_time = fake.date_time_between(start_date='now', end_date='+1y')
    
    # Generate random entry cost
    entry_cost = round(random.uniform(10, 100), 2)
    
    # Generate random location
    location = fake.city()
    
    # Generate random brief description
    brief_description = fake.sentence(nb_words=50)
    
     # Generate random host name
    host_name = fake.name()
    
    # Generate random offer
    offers = ["meal after event", "meal during event", "lottery", "first five participant have a free drink", "autograph at closed doors", "low cost book selling", "record a documental on the event"]
    offer = random.choice(offers)
    
    return (event_type, title, entry_time, finish_time, entry_cost, location, brief_description, host_name, offer)

# Generate 100 events
events = [generate_event() for _ in range(100)]

# Print the events
def write_events_to_file(events, path):
        i=0
        for event in events:
            
            with open(path+f"{i}.txt", 'w') as file:
                # Convert the event tuple to a string and write it to the file
                file.write(f"{event}\n")
            
            i+=1

# Generate 100 events
# events = [generate_event() for _ in range(5000)]

# # Write the events to a file
# write_events_to_file(events, './data/')

# dataset = EventsDataset('.')
# event_processer = EventProcesser()

# dataset.Open()

# for i in range(10):
#     event = generate_event()
#     dataset.AddEvent(event_processer.ProcessEvent(event))
#     pass

# dataset.computeWordsIDF()

# dataset.setMatrix(weight_function)

# dataset.Close()

model = SemanticLatentModel('Events','.')

# events = []
# for i in range(100):
#     event = generate_event()
#     events.append(event)
#     pass

# model.AddEvents(events)

model.ParseQuery(input('>>> Type your query: '))