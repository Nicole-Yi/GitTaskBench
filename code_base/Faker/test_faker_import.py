
from faker import Faker

# Create a Faker instance
fake = Faker()

# Generate fake data
company_name = fake.company()
address = fake.address()
phone = fake.phone_number()

print("Company Name:", company_name)
print("Address:", address)
print("Phone:", phone)