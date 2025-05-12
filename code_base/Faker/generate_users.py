import sys
import csv
sys.path.append('/data/data/agent_test_codebase/GitTaskBench/code_base/Faker')
from faker import Faker

fake = Faker()
output_file = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Faker_01/users.csv'

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Username', 'Email'])
    
    for _ in range(100):
        username = fake.user_name()
        email = fake.email()
        writer.writerow([username, email])

print(f"Generated 100 fake user records at {output_file}")