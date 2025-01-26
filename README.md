# Loan Eligibility Agent

An intelligent loan eligibility checking system that uses OpenAI's API to process loan applications with multiple verification steps. The agent performs various checks including CIBIL score verification, document validation, and employment history verification to determine loan eligibility.

## Features

- CIBIL score verification
- Age and document validation
- Loan eligibility calculation based on income and EMIs
- Employment history verification
- Automated decision-making process
- Configurable through environment variables

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Basic understanding of loan processing

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration:
   ```env
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-4o
   OPENAI_TEMPERATURE=0
   ```
It is best to keep the temperature 0

## Usage

### Basic Example

```python
from loan_agent import process_loan_application

question = """
Check loan eligibility for:
PAN: ABCDE1234F
Aadhaar: 123456789012
DOB: 1990-05-15
Monthly Income: ₹60,000
Existing EMIs: ₹15,000
"""

result = process_loan_application(question)
print(result)
```

## Loan Eligibility Criteria

The system checks the following criteria:
- CIBIL score must be above 750
- Age must be between 21-58 years
- Minimum monthly income of ₹25,000
- Minimum 2 years work experience
- Valid documentation (PAN and Aadhaar)
- Total EMIs (including new loan) should not exceed 50% of income

## System Components

### Mock Functions
The system includes mock functions for:
- CIBIL score checking
- Age and document verification
- Loan eligibility calculation
- Employment history verification

These can be replaced with actual API integrations in a production environment.

### LoanEligibilityAgent Class

The main agent class that:
- Maintains conversation context
- Processes loan applications step by step
- Makes decisions based on multiple criteria
- Uses OpenAI's API for intelligent processing

## Error Handling

The system includes basic error handling for:
- Invalid document formats
- Missing information
- Age restrictions
- Income requirements

## Development

To modify the mock functions or integrate with real APIs:
1. Locate the relevant mock function in `loan_agent.py`
2. Replace the mock implementation with your API integration
3. Update the error handling as needed

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: The GPT model to use (default: gpt-3.5-turbo)
- `OPENAI_TEMPERATURE`: Controls response randomness (0.0 to 1.0)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
