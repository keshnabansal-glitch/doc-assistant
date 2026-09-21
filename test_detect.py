from modules.doc_reader import detect_blank_fields

sample_text = """
RENTAL AGREEMENT

This agreement is made between (Landlord's Name) and
___________ (Tenant's Name) on [Date].

Monthly Rent: {{monthly_rent}}
Security Deposit Paid: Yes / No

Signature: ____________________
Date:
"""

fields = detect_blank_fields(sample_text)

for field in fields:
    print(field)