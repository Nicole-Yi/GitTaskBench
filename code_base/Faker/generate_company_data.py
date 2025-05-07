
import csv
from faker import Faker

# Create a Faker instance
fake = Faker()

# Define the output CSV file path
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Faker_02/output.csv'

# Define the header for the CSV file
fieldnames = ['Company Name', 'Address', 'Phone']

# Generate fake company data
with open(output_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for _ in range(5):
        # Create a fake company entry
        writer.writerow({
            'Company Name': fake.company(),
            'Address': fake.address(),
            'Phone': fake.phone_number()
        })
print(f"Data has been written to {output_path}")