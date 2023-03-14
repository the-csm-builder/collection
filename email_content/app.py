import boto3
import pandas as pd
from datetime import date
from openpyxl import load_workbook


# Set up SES client
ses_client = boto3.client('ses', region_name='us-east-1')

# Load Excel file
df = pd.read_excel('sam-app\email_content\Customer-Drip-Poc.xlsx')

# Iterate through the rows of the DataFrame and send an email to each contact
for index, row in df.iterrows():
    # Check if Contact Information is not blank
    
    if pd.notna(row['Contact Information']):
        # Get email and URL from the row
        email = row['Contact Information']
        url = row['URL']
        subject = row['Title']

        # Construct email message
        subject = subject
        body_text = f'Hello,\n\nPlease visit this URL: {url}\n\nThank you!'
        sender = 'jklacyn@amazon.com'
        recipient = email

        # Send email using SES client
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=sender,
        )

        # Print response from SES client
        print(f"Email sent to {email} with response: {response}")