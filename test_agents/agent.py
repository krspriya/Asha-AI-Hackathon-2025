from google.adk.agents import LlmAgent, AgentTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.google_search_tool import google_search  # For general web searches
from google.adk.tools import built_in_code_execution  # For calculations, optional
from google.genai import types
from google.adk.tools.agent_tool import AgentTool

# Constants
APP_NAME = "AshaAI"
USER_ID = "user1234"
SESSION_ID = "session_code_exec_async"
GEMINI_MODEL = "gemini-2.0-flash"

# Sub-Agent 1: Greeter - Handles Greetings
greeter_agent = LlmAgent(
    name="GreeterAgent",
    model=GEMINI_MODEL,
    instruction="You greet users warmly when they say hello or hi."
)

# Sub-Agent 2: Job Listings Search Agent - Searches for jobs
job_search_agent = LlmAgent(
    name="JobSearchAgent",
    model=GEMINI_MODEL,
    instruction="You help users find job listings relevant to their skills and interests.",
    tools=[google_search]  # Replace with a custom tool for job listings if available
)

# Sub-Agent 3: Event Search Agent - Handles community events and mentorship
event_agent = LlmAgent(
    name="EventAgent",
    model=GEMINI_MODEL,
    instruction="You assist users in finding community events, mentorship programs, and session details.",
    tools=[google_search]  # Replace with a custom tool for events if available
)

# Sub-Agent 4: Mentorship Search Agent - Helps with mentorship opportunities
mentorship_agent = LlmAgent(
    name="MentorshipAgent",
    model=GEMINI_MODEL,
    instruction="You assist users in finding mentorship programs and connecting with mentors.",
    tools=[google_search]  # Replace with a custom tool for mentorship if available
)

# Wrap them as callable tools (agent delegation)
job_search_tool = AgentTool(agent=job_search_agent)
event_tool = AgentTool(agent=event_agent)
mentorship_tool = AgentTool(agent=mentorship_agent)
greeter_tool = AgentTool(agent=greeter_agent)

# Root Agent (Coordinator)
root_agent = LlmAgent(
    name="CoordinatorAgent",
    model=GEMINI_MODEL,
    description="Coordinates queries between greeting, job search, event search, and mentorship.",
    instruction=(
        "You decide:\n"
        "- If the user greets you, call the GreeterAgent.\n"
        "- If the user asks for job listings, call the JobSearchAgent.\n"
        "- If the user asks for community events or mentorship, call the EventAgent or MentorshipAgent.\n"
    ),
    tools=[
        greeter_tool,
        job_search_tool,
        event_tool,
        mentorship_tool
    ]
)

# Session + Runner setup
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

# Simple Runner function
def call_agent(query):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    for event in events:
        if event.is_final_response():
            print("Agent Response:", event.content.parts[0].text)

# Example usage for various use cases:
call_agent("Hi there")  # GreeterAgent
call_agent("Find me job opportunities for software developers")  # JobSearchAgent
call_agent("What events are available for women in tech this month?")  # EventAgent
call_agent("Can you help me find a mentor for career guidance?")  # MentorshipAgent