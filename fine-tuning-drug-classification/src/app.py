
# ### A. Import necessary packages

import pandas as pd
import json, os
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
from openai import OpenAI

# ### B. Data loading and preprocessing
# #### 1. Load data from excel file

# Randomly read 'n' samples from the excel file
n = 2000

file_path = '../data/medicine_description.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1', header=0)

rdn_data = data.sample(n=n, random_state=42) 
rdn_data = rdn_data.reset_index(drop=True)


rdn_data.head()

# #### 2. Map unique 'Reason' values to numerical indices

# Create a dictionary to assign a unique integer to each 'Reason'
med_data = rdn_data
reasons = med_data['Reason'].unique()
reasons_hash = {reason: idx for idx, reason in enumerate(reasons)}

# #### 3. Format the 'Drug_Name' column

# Add 'Drug:' and 'Malady:' prefixes for structured formatting
med_data['Drug_Name'] = 'Drug: ' + med_data['Drug_Name'] + '\n' + 'Malady:'
med_data['Drug_Name']

# #### 4. Replace 'Reason' values with numerical indices

# Use the dictionary created earlier to replace textual reasons with their corresponding indices
med_data['Reason'] = med_data['Reason'].apply(lambda x: str(reasons_hash[x]))
med_data['Reason']

# #### 5. Drop unnecessary columns

# Remove the 'Description' column
med_data.drop(['Description'], axis=1, inplace=True)

med_data.head()

# ### C. Split Data into Training and Validation Sets

# #### 6. Perform an 80-20 split

# Split the dataset into training and validation datasets
train_data, val_data = train_test_split(med_data, train_size=0.8, random_state=100)


val_data.head()

train_data.shape, val_data.shape

# ### D. Prepare Data for Fine-Tuning

# #### 7. Define a function to convert DataFrame to JSONL format

# Convert rows into JSONL format for fine-tuning
def convert_to_jsonl(df, output):
    result = []
    system_message = {'role': 'system', 'content': 'you are a drug classification assistant!'}

    for _, row in df.iterrows():
        user_message = {'role': 'user', 'content': row['Drug_Name']}
        assistant_message = {'role': 'assistant', 'content': row['Reason']}
        result.append({'messages': [system_message, user_message, assistant_message]})

    with open(output, 'w') as f:
        for entry in result:
            f.write(json.dumps(entry) + '\n')


# #### 8. Convert training and validation datasets

# Save the training and validation datasets as JSONL files
convert_to_jsonl(train_data, 'train_data.jsonl')
convert_to_jsonl(val_data, 'val_data.jsonl')

# ### E. Upload Data for Fine-Tuning

# #### 9. Set up OpenAI API

# Load API credentials and initialize OpenAI client
load_dotenv()
api_key = os.getenv('openai_api_key')
client = OpenAI(api_key=api_key)

# #### 10. Upload JSONL files to OpenAI

# Upload training and validation datasets for fine-tuning
train_data = client.files.create(
    file=open('train_data.jsonl', 'rb'),
    purpose='fine-tune'
)

val_data = client.files.create(
    file=open('val_data.jsonl', 'rb'),
    purpose='fine-tune'
)

# ### F. Fine-Tune the Model
# #### 11: Create a fine-tuning job

suffix = 'drug-classifier'

fine_tune_job = client.fine_tuning.jobs.create(
    training_file=train_data.id,
    model='gpt-3.5-turbo-0125',
    validation_file=val_data.id,
    suffix=suffix
)
print(f"Fine-tuning job '{suffix}' created with ID: {fine_tune_job.id}")

updated_job = client.fine_tuning.jobs.retrieve(fine_tune_job.id)
print(f"Fine-tuned Model ID: {updated_job.fine_tuned_model}")

jobs = client.fine_tuning.jobs.list()

for job in jobs.data:
    if job.fine_tuned_model:
        fine_tuned_model = job.fine_tuned_model
        print(f"Found model: {fine_tuned_model}")
        

drugs = [
    "A CN Gel(Topical) 20gmA CN Soap 75gm",
    "Addnok Tablet 20'S",                   
    "ABICET M Tablet 10's",                 
]

model = 'ft:gpt-3.5-turbo-0125:personalapis:drug-classifier:AWD9hDg8'

for drug_name in drugs:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": f"Drug: {drug_name}\nMalady:"}
        ],
        max_tokens=10,
        temperature=0
    )
    predicted_malady = response.choices[0].message.content.strip()
    print(f"Drug: {drug_name}\nPredicted Malady: {predicted_malady}\n")

class_map = {
    0: "Acne",
    1: "ADHD",
    2: "Allergies",
}

for drug in drugs:
    drug_name = drug.split("'")[1]
    prompt = "Drug: {}\nMalady:".format(drug)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    response = completion.choices[0].message.content

    try:
        print(f"{drug_name} is used for {class_map[int(response)]}.")
    except:
        print(f"I don't know what {drug_name} is used for.")



