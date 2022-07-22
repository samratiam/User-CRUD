import os
import csv
import smtplib
from tempfile import NamedTemporaryFile
import shutil
import re
from dotenv import load_dotenv, find_dotenv 

# Using SMTP to send mail from my gmail account 'pudaemperor@gmail.com' to newly registered user
import smtplib

def send_email(receiver_mail,firstname):
    # Create SMTP session
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # Start TLS for security
    server.starttls()

    # Authentication
    # Loading environment variables
    load_dotenv()
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    PASSWORD = os.getenv('PASSWORD')
    server.login(SENDER_EMAIL, PASSWORD)

    # Message to be sent
    SUBJECT = "Confirmation Mail"
    TEXT = f'Hi,{firstname}, \nThis is a confirmation email about your registration for IW Bootcamp.'

    message = f'Subject: {SUBJECT}\n\n{TEXT}'

    # Sending the mail
    RECEIVER_EMAIL = receiver_mail
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)

    # Terminate the session
    server.quit()
    

# Create User class to perform CRUD operations
class User:
    # Register user, insert it into file 
    def create(self, firstname, lastname, contact, address, course, email):
        with open('data.csv', 'a+', newline='') as csvfile:
            user_header = ['firstname', 'lastname', 'contact', 'address', 'course', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=user_header)

            # If file is empty create header for each column
            if os.stat('data.csv').st_size == 0:
                writer.writeheader()
            writer.writerow({'firstname': firstname, 'lastname': lastname, 'contact': contact,
                             'address': address, 'course': course, 'email': email})

            print("User registered successfully. Check mail inbox for confirmation mail.")

    # Display information of the user based on their email
    def read(self, email):
        # Check if file exists
        if os.path.exists('data.csv'):
            with open('data.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)  
                for row in reader:  
                    if row['email'] == email:
                        print("--Your detail information---")
                        print(row)
                    else:
                        raise Exception("No records found")

    # Update information of the user based on their email
    def update(self, email):
        # Create a temporary file to store update value and then move it into original file
        tempfile = NamedTemporaryFile(mode='w', delete=False)

        fields = ['firstname', 'lastname', 'contact', 'address', 'course', 'email']

        # Check if file exists
        if os.path.exists('data.csv'):
            with open('data.csv', 'r') as csvfile, tempfile:
                reader = csv.DictReader(csvfile, fieldnames=fields)
                writer = csv.DictWriter(tempfile, fieldnames=fields)
                for row in reader:
                    # Check existing email to update the data
                    if row['email'] == email:
                        print('Updating your data\n')
                        new_firstname = str(input("Enter your updated firstname:"))
                        new_lastname = str(input("Enter your updated lastname:"))
                        new_email = str(input("Enter your updated email:"))
                        new_contact = int(input("Enter your updated contact number:"))
                        new_address = str(input("Enter your updated address:"))
                        new_course = str(input("Enter your updated preferred course:"))
                        
                        row['firstname'], row['lastname'], row['contact'], row['address'],row['course'],row['email'] = new_firstname,new_lastname,new_contact,new_address,new_course,new_email
                    else:
                        raise Exception("No records found")
                    
                    
                    row = {'firstname': row['firstname'], 'lastname': row['lastname'], 'contact': row['contact'], 'address': row['address'],'course':row['course'],'email':row['email']}
                    writer.writerow(row)
                print("Your data is updated")

            shutil.move(tempfile.name, 'data.csv')

    # Delete information of the user based on their email
    def delete(self, email):
        # Create a temporary file to remove the value and then move it into original file
        tempfile = NamedTemporaryFile(mode='w', delete=False)

        fields = ['firstname', 'lastname', 'contact', 'address', 'course', 'email']

        # Check if file exists
        if os.path.exists('data.csv'):
            with open('data.csv', 'r') as csvfile, tempfile:
                reader = csv.DictReader(csvfile, fieldnames=fields)
                writer = csv.DictWriter(tempfile, fieldnames=fields)
                for row in reader:
                    # Check existing email to delete the data
                    if row['email'] == email:
                        print('Deleting your data\n')     
                        row = {'firstname': None, 'lastname': None, 'contact': None, 'address': None,'course':None,'email':None}
                            
                        # row['firstname'], row['lastname'], row['contact'], row['address'],row['course'],row['email'] = '','','','','',''
                    else:
                        raise Exception("No record found")
                    # row = {'firstname': row['firstname'], 'lastname': row['lastname'], 'contact': row['contact'], 'address': row['address'],'course':row['course'],'email':row['email']}
                    writer.writerow(row)
                print("Your data is deleted")

            shutil.move(tempfile.name, 'data.csv')
        
    # Check whether email already exist or not  
    def check_email(self, email):
        # Check if the data.csv file exists or not
        if os.path.exists('data.csv'):
            with open('data.csv', 'r') as csvfile:
                    reader = csv.DictReader(csvfile)  
                    for row in reader:  
                        if row['email'] == email:
                            raise Exception("Email already exists.")

if __name__ == "__main__":
    while True:
        choice = int(input("""\n\nChoose one of the options:
              1. Register (Create)
              2. Read
              3. Update
              4. Delete
              5. Exit \n"""))

        # Create object of a User class
        user = User()

        # Create a user object and insert into a file and send confirmation mail
        if choice == 1:
            email = str(input("Enter your email:"))
            
            # Validating email address
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            while(re.fullmatch(regex,email) is None):
                email = str(input("Invalid email. Please enter your valid email:"))
                
            # Checking mail whether it already exists or not    
            user.check_email(email)
            
            firstname = str(input("Enter your firstname:"))
            lastname = str(input("Enter your lastname:"))
            contact = int(input("Enter your mobile number:"))
            
            # Validating contact number
            while len(str(contact))!=10:
                contact = int(input("Invalid mobile number. Please Enter valid mobile number:"))
                
            address = str(input("Enter your address:"))
            course = str(input("Enter your preferred course:"))
            
            user.create(firstname, lastname, contact, address, course, email)
            
            # After registration of user, send confirmation mail to the user
            send_email(email,firstname)
            
        # Read user data after entering email 
        elif choice == 2:
            email = str(input("Enter your email to view your data:"))
            
            user.read(email)

        # Update user data after entering email 
        elif choice == 3:
            email = str(input("Enter your email to update your data:"))
            
            user.update(email)

        # Delete user data after entering email 
        elif choice == 4:
            email = str(input("Enter your email to delete your data:"))
            option = int(input("Are you sure you want to delete your data?\nType 1 to Yes and 0 to No:\n"))
            
            if option == 1:
                user.delete(email)
        
        elif choice == 5:
            exit()

        else:
            print("Invalid choice")
        
      
