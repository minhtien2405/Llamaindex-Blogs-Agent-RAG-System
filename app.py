import os
import chainlit as cl
from dotenv import load_dotenv
load_dotenv()

from utils import MyAgent

@cl.on_chat_start
async def start():
    # Initialize the chatbot agent
    chat_engine = MyAgent()
    cl.user_session.set("chat_engine", chat_engine.agent)
    
    # Send a welcome message
    await cl.Message(
        author="Assistant", 
        content="Hello! I am a Llama-index chatbot that can help you with your queries. Ask me anything!"
    ).send()   

@cl.on_message
async def main(message: cl.Message):
    chat_engine = cl.user_session.get("chat_engine")
    
    # Get the response from the chat engine
    response = chat_engine.chat(message.content)

    try: 
        # Attempt to access metadata for the source of the response
        metadata = response.sources[0].raw_output.metadata
        
        if metadata:
            key_first = list(metadata.keys())[0]
            # Prepare the response with source details
            await cl.Message(
                author="Assistant",
                content=f"{response} \n\n"
                        f"Source: \n"
                        f"Title: {metadata[key_first]['title']} \n"
                        f"URL: {metadata[key_first]['url']} \n"
                        f"Date: {metadata[key_first]['date']}"
            ).send()
        else:
            # Send a response without source details if metadata is not available
            await cl.Message(author="Assistant", content=response).send()

    except IndexError:
        # Handle case where no sources are available
        await cl.Message(author="Assistant", content=response).send()
    
    except Exception as e:
        # Log unexpected errors for debugging
        print(f"Error: {e}")
        await cl.Message(author="Assistant", content="An error occurred while processing your request.").send()


if __name__ == "__main__":
    cl.run()
