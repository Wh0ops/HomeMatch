# HomeMatch Real Estate Application

## Project Overview

**HomeMatch** is a personalized real estate listing platform that helps buyers find the perfect property based on their preferences. The platform leverages language models and semantic search to provide tailored listings by matching buyer preferences with property descriptions. This project was developed using Python and integrates several key technologies including FAISS for similarity search, GPT-based models for personalized listing descriptions, and a vector database for managing property data.

### Key Features:
1. **Property Listing Generation**: Automatically generates property listings using OpenAI's GPT-3.5-turbo.
2. **Preference-based Search**: Uses FAISS to perform similarity searches based on buyer preferences.
3. **Personalized Descriptions**: Enhances property descriptions by tailoring them to the buyer's needs.
4. **Semantic Embedding Matching**: Employs sentence-transformers to embed both property descriptions and buyer preferences for better matches.
5. **Listing Output**: Outputs personalized listing descriptions as text files, ensuring easy access and documentation.

## Installation Instructions

To install and run this project, please follow these steps:

1. **Python 3.7** or **higher** must be installed on your machine.
2. **OpenAI API key**: You will need an **OpenAI API key** to use the **GPT-3.5 Turbo** model.

## Setup
1. **Clone the repository:**
```bash
git clone https://github.com/Wh0ops/HomeMatch.git
```
```bash
cd HomeMatch
```
2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate      # For Windows
```
3.**Install dependencies:**
```bash
pip install -r requirements.txt
```
3.**Set up OpenAI API key:**
Replace your_api_key with your own OpenAI API key in the HomeMatch.py file or export it to your environment:
```
os.environ["OPENAI_API_KEY"] ="your_api_key"
```
## Running the Application
1.**Run the main script:**
```bash
python HomeMatch.py"
```
2. **Follow the prompts** to enter your preferences (e.g., house size, desired amenities, etc.).
3. **View personalized property listings** with AI-enhanced descriptions based on your preferences.

## Project Structure
```
HomeMatch/
│
├── HomeMatch.py          # Main script for running the application
├── listings.txt          # Generated property listings
├── README.md             # This file
└── requirements.txt      # Python dependencies for the project
```
## Output Files
The application will save the generated property listings in a text file `(listings.txt)`. The listings will include both original and AI-enhanced descriptions.
## Key Dependencies

- **OpenAI**: `openai==0.28.0`  
This is used to interact with the OpenAI API, specifically for generating property listings and enhancing descriptions using GPT-3.5-turbo.

- **sentence-transformers**: `sentence-transformers==3.1.1`  
This is used for encoding buyer preferences into embeddings to perform semantic searches on property listings.

- **faiss-cpu**: `faiss-cpu==1.8.0.post1`  
FAISS is a library for efficient similarity search and clustering of dense vectors, used here to match buyer preferences with property listings.

- **numpy**: `numpy==1.26.4`  
A fundamental package for array computing with Python, used for handling embeddings and other numeric data in the project.

- **pandas**: `pandas==2.2.3`  
A library providing high-performance, easy-to-use data structures for data manipulation and analysis. Used in managing property listing data.

## How to Use

Once the application is running, the user will be prompted to answer a series of questions regarding their property preferences, such as:
- Preferred number of bedrooms and bathrooms
- Important features (e.g., modern kitchen, pool)
- Neighborhood preferences (e.g., suburban, urban)
- Desired amenities and proximity to transportation

Based on these inputs, the platform will generate a set of matching listings with enhanced descriptions to suit the user's preferences.

## Output

After running the application, the results will be stored in a text file called `listings.txt`. This file will contain the following information for each property:
- Property Name
- Price
- Bedrooms
- Bathrooms
- Size
- Location (randomly generated)
- Enhanced Description based on buyer preferences

