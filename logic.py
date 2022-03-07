import hashlib,os,binascii
import mysql.connector
from store_database import db # imports database
from datetime import date, datetime
import re # using regex to validate userNames. I do not currently know regex but I am aware of the use cases of it
from password_strength import PasswordPolicy # package that analyses password stregnth 
from hashinglibs import hashingalgo,verify_password


'''will contain logic to:

a) Add users with nessecary checks such as users with the same username cannot be added and username must be greater than 6 charecters
b) ensure passwords are greater than 6 charecters and hashed correctly before being inserted in to the userdatabase against the correct userId which is a foreign key
c) allow user to change its password by using the relationship between the parent and child table
d) parse products from a txt file into the database
e) allow user to choose the products they want
f) allow user to return a list of all products their basket (slighly flawed as in reality each user will have their own basket table)

'''
ADD_USER_COMMAND = "INSERT INTO myUsers(name,userName,address,creation_date) VALUES(%s,%s,%s,%s)"
ADD_PASSWORD = "INSERT INTO userPassword(userID,passwd) VALUES(%s,%s)"
# c = db.cursor() # creates cursor towards database

date_now = datetime.now().strftime("%y-%m-%d")

policy = PasswordPolicy.from_names( # password policy that sets password criteria
    length=6,  # min length: 8
    uppercase=1,  # need min. 2 uppercase letters
    numbers=1,  # need min. 2 digits
    special=1  # need min. 2 special characters
)



def add_users(name = ' ',userName = ' ',address = '',password = ''):
    '''logic behind adding users'''
    try:
        c = db.cursor()
        list_of_usernames = c.execute("SELECT userName FROM myUsers") # returns userNames within myUsers table. Will be used to check if new userName is available to be used or is already taken
        list_of_usernames = c.fetchall() # returns all userNames in myUsers table
        length_of_userName  = len(userName) # returns length of username
        passwordtest  = policy.test(password) # returns empty list if all conditions of the password are met
        if(length_of_userName>=6 and (userName not in list_of_usernames) and name.isalpha() and len(passwordtest) == 0):
            '''triggerered if all above of the conditions are met'''
            c.execute(ADD_USER_COMMAND,(name,userName,address,date_now))
            lastrowid = c.lastrowid # returns primary key of user added and is used to store againstt password allowing a link between parent and child
            hashed_password = hashingalgo(password) 
            c.execute(ADD_PASSWORD,(lastrowid,hashed_password))
            db.commit() #commits insetions into the database
            print("Succesfully added")

        else:
            print("TRIGGERED")
    except Exception as err:
        print("Cannot add user:",err)

    
def hashingalgo(string):
    '''takes in string that is confirmed to be a valid length password and is hashed'''
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', string.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
    

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user
       Takes in hashed and salted string/password,decodes hashed string and compares to entered password. Returns booleans 
    """
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'),100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

add_users("Matt","MattysAccount","Road 1,Ledge street,Lincoln,L1 2PR","Test123")
add_users("Callum","MattysAccount","Road 1,Ledge street,Lincoln,L1 2PR","Test123")
add_users("James","MattysAccount","Road 1,Ledge street,Lincoln,L1 2PR","Test123")
add_users("Kimani","MattysAccount","Road 1,Ledge street,Lincoln,L1 2PR","Test123")
add_users("Kelly","MattysAccount","Road 1,Ledge street,Lincoln,L1 2PR","Test123")


