from fastapi import FastAPI, File, UploadFile
from typing import List
import io
import csv
from pydantic import BaseModel
import random
from func import generate_dna_sequence

app = FastAPI()


ancient_remains_data = {}


class DNAComparisonRequest(BaseModel):
    id1: str
    id2: str


@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    decoded_content = io.StringIO(content.decode())
    csv_reader = csv.DictReader(decoded_content)
    
    for row in csv_reader:
        ancient_remains_data[row['id']] = row
    
    return {"message": "File uploaded successfully"}


@app.get("/generate_sequence/{id}")
async def generate_sequence(id: str):
    sample = ancient_remains_data.get(id)
    if not sample:
        return {"error": "Sample ID not found"}

    dna_sequence = generate_dna_sequence(
        sample['id'], 
        sample['region'], 
        int(sample['age']), 
        sample['seed']
    )
    return {"id": id, "dna_sequence": dna_sequence}


def longest_common_substring(seq1: str, seq2: str) -> str:
    m = len(seq1)
    n = len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    length_of_lcs = 0
    end_pos_seq1 = 0
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > length_of_lcs:
                    length_of_lcs = dp[i][j]
                    end_pos_seq1 = i - 1
            else:
                dp[i][j] = 0
    
    return seq1[end_pos_seq1 - length_of_lcs + 1:end_pos_seq1 + 1]




@app.get("/compare_sequences/")
async def compare_sequences(id1: str, id2: str):
    sample1 = ancient_remains_data.get(id1)
    sample2 = ancient_remains_data.get(id2)

    if not sample1 or not sample2:
        return {"error": "One or both sample IDs not found"}

    dna_sequence1 = generate_dna_sequence(
        sample1['id'], 
        sample1['region'], 
        int(sample1['age']), 
        sample1['seed']
    )

    dna_sequence2 = generate_dna_sequence(
        sample2['id'], 
        sample2['region'], 
        int(sample2['age']), 
        sample2['seed']
    )
    
    common_substring = longest_common_substring(dna_sequence1, dna_sequence2)
    
    similarity_score = len(common_substring) / max(len(dna_sequence1), len(dna_sequence2))
    
    return {
        "id1": id1,
        "id2": id2,
        "common_substring": common_substring,
        "similarity_score": similarity_score
    }


from fastapi import FastAPI
from pydantic import BaseModel
import requests

class Question(BaseModel):
    question: str

GEMINI_API_KEY = "AIzaSyALAe2YHxl5EOF0FHbqM6sQwXbAjsqyzG4"

GEMINI_MODEL = "models/gemini-1.5-pro-001"

def query_gemini(user_question: str) -> str:
    system_prompt = (
        "You are an assistant for an API server that works with ancient DNA remains. "
        "The server supports these features:\n"
        "1. Upload CSV files containing ancient remains (ID, region, age, seed).\n"
        "2. Generate DNA sequences based on seed and metadata using a specific function.\n"
        "3. Compare DNA sequences between two samples and return a similarity score.\n"
        "4. Answer natural language questions about what this API can do.\n\n"
        "5. LCS based algorithm for dna sequence comparison.\n" 
        "Answer the user's question using only this context."
    )

    full_prompt = f"{system_prompt}\n\nUser Question: {user_question}"

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro-001:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "parts": [{"text": full_prompt}]
            }
        ]
    }

    response = requests.post(url, headers=headers, params=params, json=data)

    if response.status_code != 200:
        return f"Gemini API Error: {response.status_code} - {response.text}"

    try:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return "Unexpected response format from Gemini API."


@app.post("/ask-me-anything/")
async def ask_me_anything(question: Question):
    answer = query_gemini(question.question)
    return {"response": answer}
