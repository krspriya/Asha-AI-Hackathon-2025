Link: https://asha-ai-jet.vercel.app/


Asha AI 🌸 - Intelligent Multi-Agent Chatbot
Welcome to Asha AI — a smart, modular chatbot powered by Google's ADK (Agent Development Kit)!
It handles greetings, job searches, event discoveries, and mentorship opportunities through sub-agents — making your assistant feel more natural, helpful, and friendly. 🧠✨

✨ Features
Warm Greeter Agent: Welcomes users with a friendly tone.

Job Search Agent: Helps users find relevant job opportunities online.

Event Search Agent: Suggests community events, tech sessions, and more.

Mentorship Agent: Assists users in finding mentorship programs.

Coordinator Agent: Smartly decides which sub-agent to delegate the query to.

Session Management: Each user gets a persistent session for a smoother experience.

📂 Project Structure
bash
Copy
Edit
asha-ai/
├── agent.py        
├── README.md      
🛠️ Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/asha-ai.git
cd asha-ai
2. Install Dependencies
You need the Google ADK and Google Generative AI SDK installed.

bash
Copy
Edit
pip install google-generativeai
pip install google-adk
(If google-adk isn't publicly available yet, make sure you have access or required SDK files.)

🚀 Running the Project
bash
Copy
Edit
python agent.py
This will:

Start the session.

Initialize all sub-agents.

Simulate example interactions like greetings, job searches, event discovery, and mentorship finding.

You'll see responses printed directly in your terminal!

🧠 How it Works
CoordinatorAgent receives the user input.

It decides intelligently which sub-agent should handle the task:

GreeterAgent ➔ for greetings like "Hi", "Hello"

JobSearchAgent ➔ for queries about jobs

EventAgent ➔ for event-related queries

MentorshipAgent ➔ for mentorship assistance

Each agent uses Google's gemini-2.0-flash model for fast and smart responses.

If needed, Google Search APIs are used to fetch real-time information!

📋 Example Usage
python
Copy
Edit
call_agent("Hi there!") 
# → Response from GreeterAgent

call_agent("Find me job opportunities for software developers") 
# → Response from JobSearchAgent

call_agent("What tech events are happening this month?")
# → Response from EventAgent

call_agent("Can you find a mentor for career guidance?")
# → Response from MentorshipAgent
🎨 Customization Tips
You can add more sub-agents easily for things like news updates, weather forecasts, learning resources, etc.

Replace google_search tool with your own API endpoints if needed.

Adjust the instruction prompts to make the agents behave even more friendly, witty, or formal as you like.

📬 Connect
If you like this project, have ideas, or want to collaborate, feel free to reach out! 🌟
Built with lots of creativity and care for a better AI experience! 🌸🤖
