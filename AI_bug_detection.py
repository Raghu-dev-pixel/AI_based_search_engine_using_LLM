import pandas as pd
import re
from transformers import pipeline

# Sample syslog entries
syslogs = [
    "2024-06-06 12:00:00 INF Starting system update",
    "2024-06-06 12:01:00 ERR Failed to connect to database",
    "2024-06-06 12:02:00 WRN Low disk space on /dev/sda1",
    "2024-06-06 12:03:00 INF System update completed successfully",
    "2024-06-06 12:04:00 INF Invalid memory access detected",
    "2024-06-06 12:05:00 INF Success"
]


# Create a DataFrame from the syslogs
df = pd.DataFrame(syslogs, columns=['log'])

# Example regex to extract timestamps, log levels, and messages
regex_pattern = r'^(?P<timestamp>\S+ \S+) (?P<log_level>\S+) (?P<message>.+)$'

def parse_log(log):
    match = re.match(regex_pattern, log)
    if match:
        return match.groupdict()
    return {'timestamp': None, 'log_level': None, 'message': log}


# Apply parsing to the DataFrame
df = df['log'].apply(parse_log).apply(pd.Series)
classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')

# Function to classify logs
def classify_log(log_message, keyword):
    result = classifier(log_message, candidate_labels=["Normal", keyword])
    return 'found' if keyword in result['labels'][0] else 'Normal'
    

# Make the program generic, read multiple inputs 
keyword = ""
val = 0
while True:
    print("Enter an input")
    print("1: Select Language, 2: Search operation, 3: Exit")
    val = int(input())
    if val == 1:
        print("Enter a string")
        keyword = str(input())
        exit()
    elif val == 2:
        print("Enter a string")
        keyword = str(input())
        
        #Apply the classification to the dataframe
        df['found'] = df['message'].apply(classify_log, keyword=keyword)
        
        #Filter and print the findings
        findings = df[df['found'] == 'found']
        #print("Findings for your search:")
        print(findings[['timestamp', 'log_level', 'message']])
        continue
    elif val == 3:
        print("Exiting the program")
        exit()
    else:
        print("Invalid input")
