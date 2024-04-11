document = open('DataSet.txt','r')
text = document.read().split('\n')

# Define a function to parse the document
def parse_document(doc):
    # Split the document into lines
    lines = doc.strip().split('\n')
    
    # Initialize an empty dictionary to store the parsed data
    parsed_data = {}
    
    # Iterate over each line
    for line in lines:
        
        if ':' in line:
            # Split the line into key and value based on the first colon
            key, value = line.split(':', 1)
        
            # Strip any leading or trailing whitespace from the key and value
            key = key.strip()
            value = value.strip()
            
            # Add the key-value pair to the dictionary
            parsed_data[key] = value
    
    return parsed_data
