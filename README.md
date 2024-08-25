# **LlamaIndex Blog RAG System**

This project is designed to build a Retrieval-Augmented Generation (RAG) system using LlamaIndex, Qdrant, OpenAI, and other tools. The system is designed to scrape blog posts from the LlamaIndex website, index them in a vector database, and enable querying through a chatbot interface.

## **Table of Contents**

- [Project Overview](#project-overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Project](#running-the-project)
- [Usage](#usage)

## **Project Overview**

This project involves the development of a RAG system that is capable of:

- Scraping blog posts from the LlamaIndex website.
- Indexing the content in a Qdrant vector database.
- Querying the database using OpenAI's GPT models to provide intelligent responses.

## **Features**

- **Web Scraping**: Automatically fetches blog content from the LlamaIndex website.
- **Content Indexing**: Uses Qdrant for efficient vector-based indexing and retrieval.
- **Natural Language Processing**: Employs OpenAI's GPT-4o for generating human-like responses based on retrieved information.
- **Modular Design**: The project is divided into different modules for scraping, processing, indexing, and querying.
- **Chainlit Interface**: Provides a user-friendly interface for interacting with the RAG system.

## **Getting Started**

### **Prerequisites**

Ensure you have the following installed:

- Docker and Docker Compose
- OpenAI API Key
- Qdrant API Key and Host Information
- `.env` file with necessary environment variables (as specified below)

### **Installation**

1. **Clone the Repository**:

   ```bash

   ```

2. **Set Up Environment Variables**:

   Create a `.env` file in the root directory of the project with the following content:

   ```
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_HOST=your_qdrant_host
   QDRANT_PORT=your_qdrant_port
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_COLLECTION_NAME=your_collection_name
   DATA_PATH=path_to_your_data.csv
   ```

3. **Build Docker Containers**:

   Use Docker Compose to build the necessary containers:

   ```bash
   docker-compose build
   ```

4. **Run the Project**:

   Start the application using Docker Compose:

   ```bash
   docker-compose up
   ```

   This will start the services including the web scraper, data processing pipeline, and the RAG system.
   After the services are up and running, you can access the Chainlit interface at `http://localhost:8000`.

## **Usage**

Once the project is running, you can interact with the system via the Chainlit interface. Queries can be entered, and the system will retrieve relevant blog content from the vector database and generate responses using GPT-4o.