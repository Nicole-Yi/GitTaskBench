
import csv
from faker import Faker

# Initialize Faker generator
fake = Faker()

# Path for the output CSV
output_csv = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Faker_01/fake_users.csv'

# Generate 100 fake users data
fake_users = [{'Username': fake.user_name(), 'Email': fake.email()} for _ in range(100)]

# Write to CSV
with open(output_csv, mode='w', newline='') as csv_file:
    fieldnames = ['Username', 'Email']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(fake_users)

print(f"Generated 100 fake users and saved to {output_csv}")