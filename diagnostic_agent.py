from utils.groq_client import call_groq_llm

class DiagnosticAgent:
    def run(self, evidence):
        prompt = f"Analyze industrial telemetry evidence: {evidence}. State what is abnormal."
        return call_groq_llm(prompt, agent_type="DIAGNOSTIC")
