from faker import Faker
import datetime
import random
import os

os.system("cls")
# Initialize Faker
fake = Faker()

def generate_event():
    # Generate random event type
    event_types = ['Conference', 'Workshop', 'Seminar', 'Meeting', 'Webinar']
    event_type = random.choice(event_types)
    
    # Generate random entry and finish times
    entry_time = fake.date_time_this_year(before_now=True, after_now=False)
    finish_time = fake.date_time_between(start_date='now', end_date='+1y')
    
    # Generate random entry cost
    entry_cost = round(random.uniform(10, 100), 2)
    
    # Generate random location
    location = fake.city()
    
    # Generate random brief description
    brief_description = fake.sentence(nb_words=50)
    
    return (event_type, entry_time, finish_time, entry_cost, location, brief_description)

# Generate 100 events
events = [generate_event() for _ in range(100)]

# Print the events
for event in events:
    print(event)
