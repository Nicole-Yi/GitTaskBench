
import sys
import os
sys.path.append('/data/data/agent_test_codebase/GitTaskBench/code_base/Faker')

from faker import Faker
import csv

# Initialize Faker
fake = Faker()

# Create output directory if it doesn't exist
output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Faker_02'
os.makedirs(output_dir, exist_ok=True)

# Generate 5 company records
companies = []
for _ in range(5):
    company = {
        'Company Name': fake.company(),
        'Address': fake.address().replace('\n', ' '),  # Replace newlines with spaces
        'Phone': fake.phone_number()
    }
    companies.append(company)

# Write to CSV
output_file = os.path.join(output_dir, 'output.csv')
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Company Name', 'Address', 'Phone'])
    writer.writeheader()
    writer.writerows(companies)

print(f"Generated company data has been saved to {output_file}")