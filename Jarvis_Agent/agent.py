from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool


# Create a research agent with google search capabilities
research_agent = LlmAgent(
    name="ResearchAgent",
    model="gemini-2.0-flash",
    instruction="You are a research assistant that can search the web for information.",
    description="You can use google search to find information.",
    tools=[google_search],
    output_key="research_results" # save result of the research to state
)

# Create the root agent
main_agent = LlmAgent(
    name="RootAgent",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant called Jarvis that can use the internet to answer questions. The result of search is saved in the state['research_results']",
    description="You are JARVIS, an AI assistant that can use the internet to answer questions.",
    tools=[AgentTool(agent=research_agent)] 
)

root_agent = main_agent

from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from dotenv import load_dotenv
import os
import sys
import time
import threading

load_dotenv()

APP_NAME = "Jarvis"
USER_ID = "12345"
SESSION_ID = "1223344"

session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)


def call_agent(query):
    # Create a threading event to signal when processing is done
    stop_event = threading.Event()
    
    # Start the thinking animation in a separate thread
    thinking_thread = threading.Thread(target=display_thinking_animation, args=(stop_event,))
    thinking_thread.daemon = True
    thinking_thread.start()
    
    try:
        content = types.Content(role='user', parts=[types.Part(text=query)])
        events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

        for event in events:
            if event.is_final_response():
                # Stop the thinking animation
                stop_event.set()
                thinking_thread.join()
                # Clear the thinking animation line
                sys.stdout.write("\r" + " " * 30 + "\r")
                sys.stdout.flush()
                
                final_response = event.content.parts[0].text
                print("\nJarvis: ", final_response)
                return final_response
    except Exception as e:
        # Stop the thinking animation
        stop_event.set()
        thinking_thread.join()
        # Clear the thinking animation line
        sys.stdout.write("\r" + " " * 30 + "\r")
        sys.stdout.flush()
        
        print(f"\nJarvis: I'm sorry, I encountered an error: {str(e)}")
        return None

def display_thinking_animation(stop_event):
    """Display a 'thinking' animation while the agent is processing."""
    animation = [".  ", ".. ", "..."]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\rJarvis is thinking {animation[i % len(animation)]}")
        sys.stdout.flush()
        time.sleep(0.3)
        i += 1

def run_interactive():
    print("=" * 50)
    print("Welcome to Jarvis! Type 'exit' or 'quit' to end the conversation.")
    print("=" * 50)
    
    try:
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\nJarvis: Goodbye! Have a great day!")
                    break
                    
                if user_input:
                    call_agent(user_input)
            except KeyboardInterrupt:
                print("\n\nJarvis: Interrupted. Type 'exit' to quit or continue with your question.")
                continue
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        print("\nThank you for using Jarvis!")

if __name__ == "__main__":
    run_interactive()






