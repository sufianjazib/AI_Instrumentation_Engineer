from utils.groq_client import call_groq_llm

class TroubleshootingAgent:
    def run(self, evidence, root_causes):
        prompt = f"Given root causes: {root_causes}, generate step-by-step field technician procedure and decision tree."
        return call_groq_llm(prompt, agent_type="TROUBLESHOOTING")
