class CodeFixer:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def generate_fix(self, faulty_code, fault_locations):
        prompt = self._create_prompt(faulty_code, fault_locations)
        fix_suggestion = self.llm_client.call_llm(prompt)
        return fix_suggestion

    def _create_prompt(self, faulty_code, fault_locations):
        prompt = f"Given the following code with faults at the locations {fault_locations}:\n\n{faulty_code}\n\n"
        prompt += "Please suggest a corrected version of the code."
        return prompt