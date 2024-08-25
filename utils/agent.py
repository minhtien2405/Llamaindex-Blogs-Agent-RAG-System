import os
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.core.postprocessor.llm_rerank import LLMRerank
from dotenv import load_dotenv

load_dotenv(".env")

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

class MyAgent():
    """
    MyAgent is a class that implements a chatbot powered by Retrieval-Augmented Generation (RAG) technology.
    It utilizes OpenAI's GPT-4 model, Qdrant for vector storage, and various tools for querying and summarizing data.
    """
    def __init__(self):
        super().__init__()
        
        # Initialize the OpenAI LLM with specified parameters
        self.llm = OpenAI(model="gpt-4o", 
                        max_tokens=4000, 
                        temperature=0.5, 
                        top_p=1.0, 
                        frequency_penalty=0.0, 
                        presence_penalty=0.0, 
                        stop=["\n"]
                    )
        
        # Set the LLM in the Settings for usage across the agent
        Settings.llm = self.llm
        
        # Initialize the Qdrant client with the specified environment variables
        self.qdrant_client = QdrantClient(
            host=os.getenv('QDRANT_HOST'),
            port=os.getenv('QDRANT_PORT'),
            api_key=os.getenv('QDRANT_API_KEY'),
            timeout=10
        )
        
        # Create a QdrantVectorStore instance for vector storage
        self.vector_store = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name=os.getenv('QDRANT_COLLECTION_NAME'),
        )
        
        # Initialize a VectorStoreIndex from the Qdrant vector store
        self.index = VectorStoreIndex.from_vector_store(vector_store=self.vector_store)
        
        # Initialize an LLMRerank instance for post-processing and ranking of results
        self.reranker = LLMRerank(
            choice_batch_size=5, top_n=3, llm=self.llm
        )
        
        # Create a QueryEngineTool for performing vector searches
        self.vector_tool = QueryEngineTool(
            self.index.as_query_engine(),
            metadata=ToolMetadata(
                name="vector_search",
                description="Useful for searching for information."
            )
        )
        
        # Create a QueryEngineTool for summarizing information from the index
        self.summary_tool = QueryEngineTool(
            self.index.as_query_engine(response_mode = "tree_summarize"),
            metadata=ToolMetadata(
                name="summary",
                description="Useful for summarizing information."
            )
        )
        
        # Define the context for the agent, describing its capabilities
        self.context = """\
            You are an intelligent chatbot powered by Retrieval-Augmented Generation (RAG) technology. Your primary goal is to assist users by providing accurate and relevant information based on the content of the blogs from the LlamaIndex website.
        """
        
        # Initialize the ReActAgent with the defined tools and context
        self.agent = ReActAgent.from_tools(
            [self.vector_tool, self.summary_tool],
            llm=self.llm,
            node_post_processor=[self.reranker],
            verbose=True,
            context=self.context
        )

        