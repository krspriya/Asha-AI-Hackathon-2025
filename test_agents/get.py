from core.memory import ConversationMemory
from utils.api_utils import get_realtime_info
from config import Config
from google.adk.agents import Agent
from google.adk.models.gemini import Gemini

class AshaAgent(Agent):
    """
    The ASHA AI Chatbot agent. Handles user interactions.
    """
    def __init__(
        self,
        session_details: List[Dict],
        job_listings: List[Dict],
        rules: Dict,
        model_name: str = Config.GEMINI_MODEL_NAME
    ):
        super().__init__(
            name="asha_agent",
            model=Gemini(model_name),
            instruction="You are ASHA, an AI assistant providing information on women's careers, jobs, events, and mentorship on the JobsForHer platform. Be inclusive and helpful.",
            description="An AI assistant for the JobsForHer platform.",
            tools=[google_search]  # Add google_search tool
        )
        self.session_details = session_details
        self.job_listings = job_listings
        self.rules = rules
        self.memory = ConversationMemory()


    def get_relevant_sessions(self, query: str) -> List[Dict]:
        """Retrieves relevant sessions based on the user query."""
        query = preprocess_text(query)
        relevant_sessions = [
            session for session in self.session_details
            if query in preprocess_text(session.get('title', '')) or
            query in preprocess_text(session.get('description', '')) or
            query in preprocess_text(" ".join(session.get('tags', []))) #search in tags
        ]
        return relevant_sessions[:5]  # Limit to top 5

    def get_relevant_jobs(self, query: str) -> List[Dict]:
        """Retrieves relevant job listings based on the user query."""
        query = preprocess_text(query)
        relevant_jobs = [
            job for job in self.job_listings
            if query in preprocess_text(job.get('title', '')) or
            query in preprocess_text(job.get('description', '')) or
            query in preprocess_text(job.get('skills', '')) or
            query in preprocess_text(job.get('company','')) or
            query in preprocess_text(job.get('role','')) or
            query in preprocess_text(job.get('location',''))
        ]
        return relevant_jobs[:5] # Limit to top 5

    def handle_query(self, query: str) -> str:
        """Handles a user query and generates a response."""
        self.memory.add_message(role='user', content=query)

        # Use Gemini for bias detection and general response generation
        prompt = f"""
        You are ASHA, an AI assistant on the JobsForHer platform.
        Provide helpful and inclusive responses.  Follow these rules:

        {yaml.dump(self.rules)}

        Here is the conversation history:
        {self.memory.get_history()}

        User Query: {query}

        Respond as ASHA:
        """
        try:
            response = self.model.generate_content(prompt=prompt).text
        except Exception as e:
            print(f"Error generating response: {e}")
            response = self.rules.get("general_error_response", "I encountered an error. Please try again.")
            self.memory.add_message(role='agent', content=response)
            return response

        if "bias_response" in response: # Check if Gemini detected bias
            self.memory.add_message(role='agent', content=response)
            return response

        sessions = self.get_relevant_sessions(query)
        jobs = self.get_relevant_jobs(query)

        if sessions:
            response = self.rules.get("session_response_header", "Here are some upcoming sessions:\n")
            for session in sessions:
                response += f"- {session.get('title', 'No Title')}: {session.get('description', 'No Description')} (Date: {session.get('date', 'N/A')}, Time: {session.get('time', 'N/A')}, Location: {session.get('location','N/A')})\n"
        elif jobs:
            response = self.rules.get("job_response_header", "Here are some job listings that might interest you:\n")
            for job in jobs:
                response += f"- {job.get('title', 'No Title')} at {job.get('company', 'No Company')} in {job.get('location', 'N/A')} ({job.get('job_type', 'N/A')}).  Experience: {job.get('experience', 'N/A')} years. Skills: {job.get('skills', 'N/A')}. Apply Here: {job.get('apply_link','N/A')}\n"
        else:
            realtime_info = get_realtime_info(query) # use google search
            response = self.rules.get("no_results_response", "I'm sorry, I couldn't find specific information. ") + realtime_info

        self.memory.add_message(role='agent', content=response)
        return response

    def get_conversation_history(self) -> List[Dict]:
        """Retrieves the conversation history."""
        return self.memory.get_history()