import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
import os
from main import data

with open('sample.json', 'r') as f:
    sample_data = json.load(f)

queries = sample_data['queries']
responses = sample_data['responses']
past_data = [{"query": q, "response": r} for q, r in zip(queries, responses)]

with open('merged_data.json', 'r') as f:
    weather_json = json.load(f)

weather_data = weather_json['weather_forecast']['data'][0] 
embedder = SentenceTransformer('all-MiniLM-L6-v2')
query_embeddings = embedder.encode(queries)
knn = NearestNeighbors(n_neighbors=1, algorithm='auto', metric='cosine')
knn.fit(query_embeddings)

def get_weather_info(weather):
    return {
        "temperature": weather.get('t2', None),
        "humidity": weather.get('rh2', None),
        "wind_speed": weather.get('ws10', None),
        "wind_direction": weather.get('wd10', None),
        "rain": weather.get('rainc', None)
    }

current_weather = get_weather_info(weather_data)

def find_similar_query(user_query):
    user_emb = embedder.encode([user_query])
    distances, indices = knn.kneighbors(user_emb)
    return past_data[indices[0][0]] 

def generate_response(user_query, matched_response, weather_info):
    q_lower = user_query.lower()
    if "temperature" in q_lower or "hot" in q_lower or "cold" in q_lower:
        return f"The current temperature is {weather_info['temperature']}°C."
    elif "humidity" in q_lower:
        return f"The humidity level is {weather_info['humidity']}%."
    elif "rain" in q_lower:
        if float(weather_info['rain']) == 0.0:
            return "No rain expected today. Clear skies."
        else:
            return "Rain is expected today. Carry an umbrella!"
    elif "wind" in q_lower:
        return f"The wind speed is {weather_info['wind_speed']} m/s, direction {weather_info['wind_direction']}°."
    else:
        return matched_response['response'] 

FEEDBACK_FILE = "feedback_data.json"
TRAINED_MODEL_FILE = "trained_model_data.json"

def store_feedback(user_query, generated_response, feedback):
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            feedback_data = json.load(f)
    else:
        feedback_data = []
    feedback_data.append({
        "query": user_query,
        "response": generated_response,
        "feedback": feedback
    })

    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_data, f, indent=4)
    bad_feedback_count = sum(1 for feedback in feedback_data if feedback['feedback'] == "bad")
    if bad_feedback_count >= 10:
        print("10+ 'bad' feedbacks collected. Retraining the model...")
        retrain_model(feedback_data)

def retrain_model(feedback_data):
    bad_feedback_queries = [item['query'] for item in feedback_data if item['feedback'] == "bad"]
    bad_feedback_responses = [item['response'] for item in feedback_data if item['feedback'] == "bad"]
    global queries, responses, past_data
    queries.extend(bad_feedback_queries)
    responses.extend(bad_feedback_responses)
    past_data = [{"query": q, "response": r} for q, r in zip(queries, responses)]
    new_query_embeddings = embedder.encode(queries)
    knn.fit(new_query_embeddings)

    with open(TRAINED_MODEL_FILE, 'w') as f:
        json.dump(past_data, f, indent=4)
    print("Model retrained and saved.")

MEMORY_FILE = "memory_data.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    else:
        return []

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=4)

def get_memory():
    memory = load_memory()
    return memory[-3:]

def update_memory(user_query, generated_response):
    memory = load_memory()
    memory.append({"query": user_query, "response": generated_response})
    save_memory(memory)

def main():
    print("=== Weather Chatbot ===")
    user_query = data()
    memory = get_memory()
    if memory:
        print("\nMemory of last conversation(s):")
        for m in memory:
            print(f"User: {m['query']} | Bot: {m['response']}")
    
    matched = find_similar_query(user_query)
    answer = generate_response(user_query, matched, current_weather)
    
    print("\nBot Answer:")
    print(answer)
    update_memory(user_query, answer)

    feedback = input("\nWas the answer good? (good/bad): ").strip().lower()
    if feedback in ["good", "bad"]:
        store_feedback(user_query, answer, feedback)
        print("Feedback recorded. Thank you!")
    else:
        print("Wrong feedback. Skipping.")

if __name__ == "__main__":
    main()
