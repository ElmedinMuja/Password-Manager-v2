import json
import random
import os.path
import sys
import time
#from myFunctions import *
# from PW_Generator_functions import passwordgenerator

'''
GOAL: 
    CREATE A PASSWORD MANAGER THAT STORE AND ENCRYPTS PASSWORDS IN AN 'ACCOUNT' 
STATUS: 
    COMPLETE    



   
ADDITIONS:
1 - add a forgot password section [see under new_user_check()] using twilio and the generate password functions to generate a uniqe 6 character + digit key
2 - nested data to hold things like date created, date last accessed, date last changed, etc. see chapter 16 in python crash course
    a. this will add alot of work and refactoring with the current functions
3 - Alt method of encrypt:
     - create a list of all binary codes. use this as a 2nd layer of encryption
     - when encoded from key1 to key2, get the binary code, then with the int passed, move x indexs and get 
        the binary code and translate it back to a character and use that as the return 
     - return 
     
     
STEP BY STEP:

1 - SCRIPT WILL ASK FOR FILENAME AKA 'ACCOUNT'
2 - IF USER HAS AN ACCOUNT, THEN IT WILL REQ ITS PASSWORD
  - IF USER DOES NOT HAVE AN ACCOUNT, IT WILL CREATE ONE WITH A PASSWORD 
3 - USER CAN DO ANY OF THE FOLLOWING:
    a - ADD ACCOUNT/PASSWORD COMBO
    b - GET THE PASSWORD TO AN ACCOUNT
    c - UPDATE AN EXISTING ACCOUNTS PASSWORD
    d - LIST OUT ALL THE ACCOUNTS THAT HAVE SAVED PASSWORDS IN THE FILE   
4 - IF USER ADDS A PASSWORD, IT WILL BE ENCRYPTED WITH AN ENIGMA LIKE METHOD


POSSIBLE ADDITIONS:
1 - RECOVER PASSWORD TO ACCESS FILE USING TWILIO [NEED NEW TOKEN]
2 - ENCRYPTION KEY CHANGES EVERYTIME DATA IS ACCESSED 
'''

### function for adding dummy data to file; testing #####
def add_dummy_data():
    fn = 'PWMGR.json'
    # data to add
    PWinfo = {'hotmail':'qwerty',
              'gmail':'qazwsx',
              'runescape':'q1w2e3r4t5',
              'google':'fdlkasdf'}

    # add data to json file
    with open(fn,'w') as jsonobj:
        json.dump(PWinfo,jsonobj)
    # load data to confirm it was added
    with open(fn) as fileobj:
        contents = json.load(fileobj)


def add_data_to_json(fn,key,value):
    info = {key:value}
    # add data to json file
    with open(fn,'w') as jsonobj:
        json.dump(info,jsonobj)
    # load data to confirm it was added





## loads json file and returns json object
def open_load_json(fn):
    with open(fn) as f:
        contents = json.load(f)
    return contents


## generate original key, for whatever reason i might need this again
## static, will always remain the same
def originalKey():

    allchar = string.ascii_lowercase,string.ascii_uppercase,string.digits,string.punctuation

    ## make them into a list
    onestring = ''
    for items in allchar:
        for i in items:
            onestring += i

    ## create an all characters list
    newkey1 = list(onestring)
    return newkey1


## create new randmoized key; ***************** HAVE THIS ADD NEW KEY TO JSON FILE 'key2.json'
def generate_new_encryption():

    ogkey = originalKey()


    newkey2 = []
    for items in range(len(ogkey)):
        random_char = random.choice(ogkey)
        newkey2 += random_char
        charindex = ogkey.index(random_char)  ## returns a number
        ogkey.pop(charindex)

    return newkey2


## convert char(string) to binary
def convert_to_binary(text):
    to_convert = text.encode()
    binary_codes = int.from_bytes(to_convert,byteorder='little')
    binary_string = bin(binary_codes)
    print(binary_string)
    return binary_string


## encrypt the string and return the character
def encrypt_password(password_to_encrypt):
    jsonkey1 = 'key1.json'
    jsonkey2 = 'key2.json'
    encrypted_string = ''
    # password_to_encrypt = 'aaaa'
    key1 = open_load_json(jsonkey1)
    key2 = open_load_json(jsonkey2)

    for character in password_to_encrypt:
        index = key1.index(character)  ## get index of character in key1
        encrypting = key2[index]  ## return char in same index of key2
        encrypted_string += encrypting  ## add to string
    return encrypted_string



## decrypt the password string
def decryptor(password_to_decrypt):
    ## create variables for key.json files and get json objs with open_load_json
    jsonkey1 = 'key1.json'
    jsonkey2 = 'key2.json'
    key1 = open_load_json(jsonkey1)
    key2 = open_load_json(jsonkey2)

    ## set variable for empty string
    decrypted_string = ''

    ## decrypt each character in strig and append to blank string
    for character in password_to_decrypt:
        index = key2.index(character)  ## get index of character in key1
        decrypting = key1[index]  ## return char in same index of key2
        decrypted_string += decrypting  ## add to string

    ## return string
    return decrypted_string



## add account and password to opened file; works if data already exists
def add_to_file(fn, account,password):
    # fn = 'PWMGR.json'

    ## open json file with r+ permissions; view, append, edit, etc
    with open(fn, 'r+') as f:
        ## load json
        contents = json.load(f)
        ## add k,v
        contents[account] = encrypt_password(password)

    ## add to json file with json.dumps()
    with open(fn, 'w') as f:
        f.write(json.dumps(contents))


## pass the account/site you want the password from
def get_password(fn, account):
    # fn = 'PWMGR.json'

    # load data to confirm it was added
    with open(fn) as f:
        contents = json.load(f)

    if contents[account] == 'fileaccess':
        print('cannot give out the password')
    else:
        password = contents[account]
        password = decryptor(password)

    return password
    #print(f"your decrypted password is: {password}")



## list out the site/account names
def list_acconts(fn):
    #fn = 'PWMGR.json'

    # load data to confirm it was added
    with open(fn) as f:
        contents = json.load(f)
        for k,v in contents.items():
            print(k.title())


## check if the user has an existing file and if not, create one for them using the name given
def new_user_check():
    user_file = input(
        'what is the name of your file? \n'
        'If you do not already have one, give me a filename and i can create one for you\n'.title())

    fn = str(user_file + '.json')

    ## check if user_file exists


    ## if file already exists, skip to ask what user wants to do step
    if os.path.exists(fn) is True:

        ## ask for password to access the file
        pass_to_access = input('What is access password to get into the account?')


    ## if the user input != the password ['fileaccess'] then ask again
        if pass_to_access != get_password(fn,'filepass'):
            print('incorrect password'.title())
            sys.exit()

    ## password recovery with text
            # print('incorrect password \nWould you like to reset your password? Y/N'.title())
            # if input('').lower() == 'y':
            #     secret_code = Textmeresetcode(passwordgenerator(8),13473236866)
            #     customTextme(str(secret_code)),print('code has been sent to your phone, input code for new temp password:\n')
            #     code_input = input('')
            #     if code_input == secret_code:
            ## if password is correct, grant access

        ## if the userinput != password
        if pass_to_access == get_password(fn,'filepass'):
            time.sleep(1)
            print('\nPassword correct, \npulling up existing encrypted file:'.title())
            time.sleep(1)
            pass



        else:
            sys.exit()


    ## if user file doesnt exist, create one and add password to access it in the future
    else:
        open(fn, 'w')
        print('no file detected under that name,\n creating your new file: '.title() + "'" + fn + "'")

        ## creates a password to access file; encrypts and stores it into the file itself
        user_file_password = input('set a password to access your password file'.title()) # ask for a password
        user_file_password = encrypt_password(user_file_password) # encrypts the password
        new_user_info = {'filepass':str(user_file_password)} # stores both profile and password into a var

        ## add password to access the file into the file
        add_data_to_json(fn,'filepass',user_file_password)
        print(f"file and password have been created".title())


    return fn


## add new key list/independant string/char to a json file
def add_key_to_json(fn,keylist):
    import json
    ## add to json file with json.dumps()
    with open(fn, 'w') as f:
        f.write(json.dumps(keylist))


## update key1.json
def update_key1():
    add_key_to_json('key1.json', originalKey())


## update key2.json
def update_key2():
    add_key_to_json('key2.json', generate_new_encryption())


fn = new_user_check()

## running it
try:
    while True:
        # user_file = input('what is the name of your file? \nIf you do not already have one, give me a filename and i can create one for you\n'.title())
        #
        # ## check if user_file exists
        # fn = str(user_file + '.json')
        #
        # ## if file already exists, skip to ask what user wants to do step
        # if os.path.exists(fn) is True:
        #     print('pulling up existing encrypted file'.title())
        #     time.sleep(1)
        #     pass
        # else:
        #     open(fn,'w')
        #     print('creating your new file: '.title() + "'"+fn+"'")
        #
        # # asks user what they want to do
        userInput = input('\nWhat would you like to do? Here are your options'
                          '\n Type "q" to quit'
                          '\n Add: to add account and passwordd'
                          '\n Get: tells you password of the account'
                          '\n Update: update password for existing account'
                          '\n List: list out all stored accounts\n')


        userInput = userInput.lower()
        ## quit option
        if userInput == 'q' or userInput.lower() == 'quit':
            print('=== EXISTING PROGRAM ====')
            break

        ## add new account and password pair
        elif userInput == 'add':
            accounta = str(input('\nwhat is the account/site\n'.title()))
            passworda = str(input('what is the password\n'.title()))
            add_to_file(fn,accounta,passworda)

            print('\n details have been encrypted and saved'.title())
            time.sleep(1)

        ## retrieve password of an account
        elif userInput == 'get':
            account_to_get = input('\nwhat is the account whos password you want to get; i.e hotmail/gmail\n'.title())
            heres_your_password = get_password(fn,account_to_get)

            print(f"\nyour password for ".title() + account_to_get + f" is: " + heres_your_password)
            time.sleep(1)

        ## update a password to an existing account; uses the add_to_file function
        elif userInput == 'update':
            account_name = input('\nwhat accounts password do you want to update?\n'.title())
            new_password = input('what is the new password \n'.title())
            add_to_file(fn,account_name,new_password)

            print('\n details have been encrypted and saved'.title())
            time.sleep(1)
        ## list out all accounts stored in the PasswordManager
        elif userInput == 'list':
            print('\n')
            print(f"here are the avaliable accounts: ".title())
            list_acconts(fn)
            time.sleep(1)


except KeyboardInterrupt:
    print('\n === ENDING PROGRAM ===')
except KeyError:
    print('\nALERT: That account does not exist!'.upper())
except ValueError:
    print('\n***There seems to have been an error, please restart the manager***')
    sys.exit()

