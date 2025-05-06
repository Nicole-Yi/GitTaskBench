
import sys
import os
sys.path.append('/data/data/agent_test_codebase/GitTaskBench/code_base/Faker')

from faker import Faker
import csv

# Initialize Faker
fake = Faker()

# Create output directory if it doesn't exist
output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Faker_01'
os.makedirs(output_dir, exist_ok=True)

# Generate 100 fake users
users = []
for _ in range(100):
    users.append({
        'Username': fake.user_name(),
        'Email': fake.email()
    })

# Save to CSV
output_file = os.path.join(output_dir, 'output.csv')
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['Username', 'Email']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for user in users:
        writer.writerow(user)

print(f"Generated 100 fake users and saved to {output_file}")