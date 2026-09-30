from utils.groq_client import call_groq_llm

class RootCauseAgent:
    def run(self, evidence, diagnostic_findings):
        prompt = f"Given diagnostic findings: {diagnostic_findings} and evidence: {evidence}, generate ranked probable root causes."
        return call_groq_llm(prompt, agent_type="ROOT_CAUSE")
