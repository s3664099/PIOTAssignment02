"""
.. module:: login

"""
import binascii
import hashlib
import os
import pymysql

# The following code for hashing, salting, and verifying a password was provided by
# https://www.vitoshacademy.com/hashing-passwords-in-python/
def hash_password(password):
    """
    Hash password

    """
    #The password is hashed, and salted, and the salt is added to the hash
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)

    #The encrypted password is then returned to the user
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """
    Verify password

    """
    #The stored, and entered passwords are provided.
    #The provided password is hashed, and salted with the salt from the stored password
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')

    #The two are then compared and a true or false is returned
    return pwdhash == stored_password


def new_user(user_name, first_name, last_name, email, password, db_connection):
    """
    New user insertion

    """
    cur = db_connection.cursor()
    password = hash_password(password)
    # SQL to insert new user into the database
    cur.execute(
        "INSERT INTO user VALUES ('" + user_name + "','" + first_name + "','" + last_name + "','" + password + "','" + email + "')")
    db_connection.commit()
    # Returns that the new user has been successfully created


def logon(email, user_password, db_connection):
    """
    User logging on

    """
    cur = db_connection.cursor()
    # SQL Query to search for the user and retrieves the password
    try:
        result = cur.execute("SELECT email, password FROM user WHERE email='" + email + "'")
    except pymysql.Error as e:
        print(e)
        return 1

    # Checks to see whether the user has been found
    if result:

        for email, password in cur.fetchall():

            # Verifies the password is correct
            new_key = verify_password(password, user_password)

            if (new_key == True):

                # Returns that the log in is successful
                return 2
            else:

                # Returns that the password is incorrect
                return 3
    else:

        # Returns that the user has not been found
        return 1

def verify_register(email,username,db_connection):
    """
    Verify registration

    """
    cur=db_connection.cursor()
    try:
        result=cur.execute("SELECT email from user where email='"+email+"' or username='"+username+"'")
    except pymysql.Error as e:
        print(e)
        return 1

    if result:
        return 1
    else:
        return 2


# ADDED BELOW MODIFIED CODE FOR LOGIN, PLEASE INCORPORATE IN TESTS 

#writing a new function to test API call for hashing the input password
def hashing_password(email,password,db_connection):
    """
    Hashing the password

    """
    cur = db_connection.cursor()
    # SQL Query to search for the user and retrieves the password
    try:
        result = cur.execute("SELECT email, password FROM user WHERE email='" + email + "'")
    except pymysql.Error as e:
        print(e)
        return 1

    # Checks to see whether the user has been found
    if result:

        for email, stored_password in cur.fetchall():
            salt = stored_password[:64]
            stored_password = stored_password[64:]
            encryptedPassword = hashlib.pbkdf2_hmac('sha512',
                                  password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    encryptedPass = binascii.hexlify(encryptedPassword).decode('ascii')
    return encryptedPass

#new Function to verify hashed password input against the password stored in the database
def verify_password_new(stored_password,provided_password):
    """
    Verification of the new password

    """
    stored_password = stored_password[64:]
    return stored_password == provided_password

#modified function to login when encrypted password is passed
def login(email, user_password, db_connection):
    """
    User login

    """
    cur = db_connection.cursor()
    # SQL Query to search for the user and retrieves the password
    try:
        result = cur.execute("SELECT u.email, password FROM user u , user_role ur WHERE u.email='" + email + "' and u.email=ur.email and ur.is_active='1'")
    except pymysql.Error as e:
        print(e)
        return 1

    # Checks to see whether the user has been found
    if result:

        for email, password in cur.fetchall():

            # Verifies the password is correct
            new_key = verify_password_new(password, user_password)

            if (new_key == True):

                # Returns that the log in is successful
                return 2
            else:

                # Returns that the password is incorrect
                return 3
    else:

        # Returns that the user has not been found
        return 1