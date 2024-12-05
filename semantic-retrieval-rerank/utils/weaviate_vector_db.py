import weaviate, os, json 
from dotenv import load_dotenv 
from weaviate.classes.init import Auth 
import weaviate.classes.config as wvc  

load_dotenv()  

wcd_url = os.getenv('weaviate_api_url') 
wcd_api_key = os.getenv('weaviate_api_key') 
openai_api_key = os.getenv('openai_api_key')
cohere_api_key = os.getenv('cohere_api_key')

# Connect to wcd instance
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,
    auth_credentials=Auth.api_key(wcd_api_key),
    headers={
        'X-OpenAI-Api-key': openai_api_key,
        'X-Cohere-Api-Key': cohere_api_key
    },
    skip_init_checks=True
)

print(f'Connected to weaviate cloud instance? {client.is_ready()}')

# Create collection with reranker configuration
try:
    # Create the "MarcusAurelius" collection with Cohere reranker
    marcus_aurelius = client.collections.create(
        name='MarcusAurelius',
        properties=[
            wvc.Property(name='category', data_type=wvc.DataType.TEXT, skip_vectorization=True),
            wvc.Property(name='question', data_type=wvc.DataType.TEXT, skip_vectorization=False),
            wvc.Property(name='answer', data_type=wvc.DataType.TEXT, skip_vectorization=False),
        ],
        vectorizer_config=wvc.Configure.Vectorizer.text2vec_openai(),
        generative_config=wvc.Configure.Generative.openai(),

        inverted_index_config=wvc.Configure.inverted_index(
            index_property_length=True
        ),
        vector_index_config=wvc.Configure.VectorIndex.hnsw(
            distance_metric=wvc.VectorDistances.COSINE
        )
    )
    print('Collection created successfully!')

except Exception as e:
    print(f"Error creating the 'MarcusAurelius' collection: {e}")

# Load data from the JSON file
with open('./aurelius.json', 'r') as f:
    data = json.load(f)

# Prepare data for insertion
question_objs = []
for d in data:
    question_objs.append({
        "answer": d["Answer"],
        "question": d["Question"],
        "category": d["Category"],
    })

collection = "MarcusAurelius"
# Add objects to Weaviate using batch processing
with client.batch.dynamic() as batch:
    for obj in question_objs:
        batch.add_object(
            properties=obj,
            collection=collection
        )

    print("Data inserted successfully!")

client.close()
