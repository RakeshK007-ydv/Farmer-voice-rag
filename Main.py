import chromadb
from google import genai
from dotenv import load_dotenv 
import os 
from pathlib import Path  
import sounddevice as sd
from scipy.io import wavfile

load_dotenv()
gemini_client = genai.Client()

file = open("wheat.txt" , "r" ,encoding="utf-8") 
content = file.read()
print(content) 
file.close() 

# Chunking the content  

chunk_size  = 500 
overlap = 50 
chunks = [] 

for i in range (0 , len(content), chunk_size - overlap):
    chunk = content[i:i + chunk_size]
    chunks.append(chunk) 
print("Total chunks:", len(chunks))
for i , chunk in enumerate(chunks):
    print(f"chunk{i+1}: {len(chunk)} characters ") 

# connecting to chromadb 
client = chromadb.PersistentClient(    
    path = "./farmer_database"
) 

# create collection 
collection = client.get_or_create_collection(
    name = "farmer_knowledge" 
) 

# check database 
print("Collection created successfully!")
print("Total records:" , collection.count()) 

# generating embeddings 
 # Store documents only if database is empty

if collection.count() == 0:

    response = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunks
    )

    embeddings = [
        item.values for item in response.embeddings
    ]

    collection.add(
        ids=[f"wheat_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings
    )

    print("Knowledge base created successfully!")

else:
    print("Existing knowledge base found!")
    print("Total records:", collection.count())

print("Stored records:", collection.count()) 

# similarity search 
# Record farmer's voice

duration = 8
sample_rate = 16000

print("Speak your question...")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

wavfile.write("farmer_question.wav", sample_rate, audio)


# Convert voice into text

audio_file = gemini_client.files.upload(
    file="farmer_question.wav"
)

transcription = gemini_client.interactions.create(
    model="gemini-3.5-transcribe",
    input=[
        {
            "type": "audio",
            "uri": audio_file.uri,
            "mime_type": audio_file.mime_type
        }
    ]
)

question = transcription.output_text.strip()

print("Farmer asked:", question)

query_response = gemini_client.models.embed_content(
    model="gemini-embedding-001",
    contents=question
)

query_embedding = query_response.embeddings[0].values 

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

print(results["documents"]) 

# gemini use information and will provide answer to user 

retrieved_chunks = results["documents"][0]

context = "\n\n".join(retrieved_chunks)

prompt = f"""
You are a helpful agricultural assistant for farmers.

Answer the farmer using only the provided context.

Follow these rules:
1. Answer in the same language as the farmer's question.
2. Use simple language that farmers can understand.
3. Never claim a disease is confirmed based only on symptoms.
4. Explain possible causes when multiple causes exist.
5. Never invent pesticide doses or treatment instructions.
6. If the context does not contain enough information,
   clearly say so.
7. Give practical guidance based on the available information.

Farmer's Question:
{question}

Agricultural Information:
{context}

Answer:
"""

response = gemini_client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

print("\nAI Answer:")
print(response.text)








