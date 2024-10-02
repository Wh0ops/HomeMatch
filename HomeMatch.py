import os
import openai
import json
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss  
import pandas as pd
import random
import re

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "voc-239646155126677350547366e30fc1cf22a8.48832933"
os.environ["OPENAI_API_BASE"] = "https://openai.vocareum.com/v1"  

openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = os.environ["OPENAI_API_BASE"]

# Load SentenceTransformer model for embedding buyer preferences
model = SentenceTransformer('all-MiniLM-L6-v2')

# FAISS setup
dimension = 384  # The dimensionality of the sentence embeddings used by all-MiniLM-L6-v2
index = faiss.IndexFlatL2(dimension)  # L2 distance-based index

# Function to randomly generate neighborhood names
def generate_random_location():
    neighborhoods = ["Sunset Park", "Oakwood", "Green Valley", "Silverlake", "Westwood", "Brookfield", "Riverfront Estates", "Sunnyvale"]
    return random.choice(neighborhoods)

# Function to generate personalized listing descriptions using GPT
def personalize_listing_description(original_description, buyer_preferences):
    messages = [
        {
            "role": "system",
            "content": "You are a real estate assistant that personalizes property listings based on buyer preferences. Emphasize features important to the buyer without adding new information."
        },
        {
            "role": "user",
            "content": f"""Given the following property listing and buyer preferences, enhance the description while maintaining factual accuracy.

Property Listing:
{original_description}

Buyer Preferences:
{buyer_preferences}

Enhanced Description:"""
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    augmented_description = response['choices'][0]['message']['content'].strip()
    return augmented_description

# Function to generate property listings using GPT
def generate_property_listings_gpt(num_listings):
    listings = []
    for _ in range(num_listings):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a real estate assistant generating property listings for real estate agents."
                },
                {
                    "role": "user",
                    "content": "Generate a property listing with information about neighborhood, price, bedrooms, bathrooms, and a description of the property."
                }
            ],
            max_tokens=500,
            temperature=0.7
        )
        listing = response['choices'][0]['message']['content'].strip()
        listings.append(listing)
    return listings

# Store listings in FAISS
def store_listings_in_faiss():
    global properties
    properties = []
    property_descriptions = generate_property_listings_gpt(10)

    property_embeddings = np.array([model.encode(description) for description in property_descriptions])

    for idx, description in enumerate(property_descriptions):
        location = generate_random_location()  # Generate random location
        properties.append({
            "name": f"Property {idx + 1}",
            "price": "$" + str(np.random.randint(300000, 900000)),
            "bedrooms": str(np.random.randint(2, 6)),
            "bathrooms": str(np.random.randint(1, 4)),
            "size": str(np.random.randint(1500, 3000)) + " sqft",
            "location": location,  # Use generated location
            "description": description
        })

    index.add(property_embeddings)
    print(f"Stored {len(properties)} GPT-generated listings in FAISS")
    return properties, property_descriptions

# Function to collect buyer preferences
def collect_buyer_preferences():
    questions = [
        "What size do you want your house to be? (e.g., 3 bedrooms, 2 bathrooms)",
        "What are the 3 most important features for you in a property? (e.g., backyard, modern kitchen)",
        "Which amenities would you prefer? (e.g., pool, gym, parking)",
        "Which transportation options are important to you? (e.g., proximity to highways or public transit)",
        "Do you prefer a more urban or suburban neighborhood?"
    ]
    preferences = {}
    for question in questions:
        answer = input(question + "\n")
        preferences[question] = answer
    return preferences

# Function to embed buyer preferences using SentenceTransformers
def embed_buyer_preferences(preferences):
    preferences_text = " ".join(preferences.values())
    preferences_embedding = model.encode(preferences_text)
    print("Preferences embedding generated: ", preferences_embedding)  # Debugging print
    return preferences_embedding

# Perform semantic search in FAISS
def search_listings_faiss(preferences_embedding):
    distances, indices = index.search(np.array([preferences_embedding]), 10)  # Changed to 10 results
    results = [properties[i] for i in indices[0]]
    return results

# Function to display the search results with enhanced descriptions
def display_search_results(search_results, buyer_preferences):
    for result in search_results:
        original_description = result['description']
        personalized_description = personalize_listing_description(original_description, buyer_preferences)
        
        # Ensure the original and enhanced descriptions are clearly printed
        print(f"\nMatched Listing:")
        print(f"Neighborhood: {result['location']}")
        print(f"Original Description: {original_description}")
        print(f"Enhanced Description: {personalized_description}")

# Function to save listings to a file with UTF-8 encoding
def save_listings_to_file(listings, filename="listings.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for listing in listings:
            f.write(f"Name: {listing['name']}\n")
            f.write(f"Price: {listing['price']}\n")
            f.write(f"Bedrooms: {listing['bedrooms']}\n")
            f.write(f"Bathrooms: {listing['bathrooms']}\n")
            f.write(f"Size: {listing['size']}\n")
            f.write(f"Neighborhood: {listing['location']}\n")
            f.write(f"Property Description: {listing['description']}\n")
            f.write("\n")  # Add a new line for spacing between listings
    print(f"Listings saved to {filename}")

# Main function to run the HomeMatch project
def main():
    properties, property_descriptions = store_listings_in_faiss()

    # Save generated listings to a file
    save_listings_to_file(properties)

    # Collect buyer preferences
    buyer_preferences = collect_buyer_preferences()

    # Embed buyer preferences
    preferences_embedding = embed_buyer_preferences(buyer_preferences)

    # Perform semantic search based on buyer preferences
    print("\nPerforming semantic search based on buyer preferences...")
    search_results = search_listings_faiss(preferences_embedding)

    # Display the search results with personalized descriptions
    display_search_results(search_results, buyer_preferences)

# Run the main function
if __name__ == "__main__":
    main()