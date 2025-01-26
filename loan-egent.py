import openai
import re
import os
from dotenv import load_dotenv

_ = load_dotenv()
from openai import OpenAI

# OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Mock Functions to get CIBIL score from PAN. This can be changed to real CIBIL integration
def check_cibil_score(pan_number):
    # Simulated CIBIL score check
    scores = {
        "ABCDE1234F": 780,
        "PQRST5678G": 680,
        "LMNOP9012H": 550
    }
    return f"CIBIL Score: {scores.get(pan_number, 600)}"

# Mock Functions to verify age and documents. 
# This could be an interactive input of documents and extraction of information like age
def verify_age_and_documents(aadhaar, pan, dob):
    # Simulated age and document verification
    from datetime import datetime
    birth_year = int(dob.split('-')[0])
    age = datetime.now().year - birth_year
    
    if age < 21 or age > 58:
        return "Age not within eligible range (21-58 years)"
    
    # Mock Aadhaar number validation
    if len(aadhaar) != 12 or not aadhaar.isdigit():
        return "Invalid Aadhaar number"
        
    # Mock PAN number validation
    if not re.match("[A-Z]{5}[0-9]{4}[A-Z]{1}", pan):
        return "Invalid PAN format"
        
    return "Age and documents verified successfully"

# Mock Loan Eligibility Calculation. 
# This could be an integration with a loan calculator API
def calculate_loan_eligibility(monthly_income, existing_emis=0):
    # Mock Loan Eligibility Calculation. This could be an integration with a loan calculator API
    if monthly_income < 25000:
        return "Income below minimum requirement of ₹25,000"
        
    max_emi_capacity = monthly_income * 0.5 - existing_emis
    
    # Assuming 10.5% interest rate and 20-year tenure
    interest_rate = 0.105
    tenure_months = 240
    
    # EMI calculation formula
    r = interest_rate / 12
    max_loan = (max_emi_capacity * ((1 + r)**tenure_months - 1)) / (r * (1 + r)**tenure_months)
    
    return {
        "max_emi_allowed": round(max_emi_capacity, 2),
        "max_loan_amount": round(min(max_loan, 4000000), 2)  # Capped at 40 lakhs
    }

# Mock Employment History Check. 
# The data can be extracted from documents or integrations
def check_employment_history(pan_number):
    # Simulated employment history check
    employment_data = {
        "ABCDE1234F": {"status": "Salaried", "experience": 5, "current_tenure": 3},
        "PQRST5678G": {"status": "Self-Employed", "experience": 4, "business_vintage": 4},
        "LMNOP9012H": {"status": "Salaried", "experience": 1, "current_tenure": 1}
    }
    
    if pan_number not in employment_data:
        return "Employment history not found"
        
    data = employment_data[pan_number]
    if data["status"] == "Salaried" and data["experience"] < 2:
        return "Insufficient work experience (minimum 2 years required)"
    
    return f"Employment verified - {data['status']} with {data['experience']} years experience"

# Known Actions
known_actions = {
    "check_cibil_score": check_cibil_score,
    "verify_age_and_documents": verify_age_and_documents,
    "calculate_loan_eligibility": calculate_loan_eligibility,
    "check_employment_history": check_employment_history
}

# Loan Eligibility Agent
class LoanEligibilityAgent:
    def __init__(self):
        # System Prompt that sets the instruction to the agent of how to identify the actions
        self.system_prompt = """
        You are a loan eligibility checking agent for an Indian bank. 
        You run in a loop of Thought, Action, PAUSE, Observation.
        At the end of the loop you output a Final Decision.

        Available actions:
        1. check_cibil_score: Returns CIBIL score for a given PAN number
        2. verify_age_and_documents: Verifies age and document validity given Aadhaar, PAN, and DOB
        3. calculate_loan_eligibility: Calculates maximum loan amount given monthly income and existing EMIs
        4. check_employment_history: Verifies employment status and experience

        Requirements for approval:
        - CIBIL score above 750
        - Age between 21-58 years
        - Minimum monthly income of ₹25,000
        - Minimum 2 years work experience
        - Valid documentation
        - Total EMIs (including new loan) should not exceed 50% of income

        Example:
        Question: Check loan eligibility for a person with PAN ABCDE1234F, Aadhaar 123456789012, 
        DOB 1990-05-15, monthly income ₹60,000 with existing EMIs of ₹15,000
        Thought: Let me first check the CIBIL score
        Action: check_cibil_score: ABCDE1234F
        PAUSE
        """
        self.messages = [{"role": "system", "content": self.system_prompt}]

    # The __call__ method is the main method that runs the agent
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    # The execute method is the main method that runs the agent
    def execute(self):
        completion = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE")),
            messages=self.messages
        )
        return completion.choices[0].message.content

# The process_loan_application method is the main method that runs the agent
def process_loan_application(question, max_turns=10):
    agent = LoanEligibilityAgent()
    next_prompt = question
    
    action_re = re.compile(r"Action: (\w+): (.*)")
    
    for i in range(max_turns):
        print(f"\nStep {i + 1}:")
        result = agent(next_prompt)
        print(result)
        
        actions = [
            action_re.match(a) 
            for a in result.split('\n') 
            if action_re.match(a)
        ]
        
        if not actions:
            if "Final Decision:" in result:
                return result
            print("No action found or final decision reached")
            return
            
        action, action_input = actions[0].groups()
        if action not in known_actions:
            raise Exception(f"Unknown action: {action}: {action_input}")
            
        print(f"Executing: {action} with input: {action_input}")
        
        if action == "calculate_loan_eligibility":
            income, emis = map(float, action_input.split(","))
            observation = known_actions[action](income, emis)
        elif action == "verify_age_and_documents":
            # Parse the comma-separated input
            inputs = [x.strip() for x in action_input.split(",")]
            aadhaar = inputs[0].split()[-1]  # Get the last word after "Aadhaar"
            pan = inputs[1].split()[-1]      # Get the last word after "PAN"
            dob = inputs[2].split()[-1]      # Get the last word after "DOB"
            observation = known_actions[action](aadhaar, pan, dob)
        else:
            observation = known_actions[action](action_input)
            
        print(f"Observation: {observation}")
        next_prompt = f"Observation: {observation}"

# Example usage
question = """
Check loan eligibility for:
PAN: LMNOP9012H
Aadhaar: 123456789012
DOB: 1990-05-15
Monthly Income: ₹60,000
Existing EMIs: ₹15,000
"""

process_loan_application(question)