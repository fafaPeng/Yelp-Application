#Mady by Ziying(301417046) Peng
#2023-04-01

import pyodbc
import uuid

conn = pyodbc.connect('driver={SQL Server};Server=cypress.csil.sfu.ca;Trusted_Connection=yes;')
cur = conn.cursor()

# to validate the connection, there is no need to change the following line
cur.execute('SELECT username,passphrase from dbo.helpdesk')
row = cur.fetchone()
while row:
    print ('SQL Server standard login name = ' + row[0])
    print ('The password for this login name = ' + row[1])
    row = cur.fetchone()

global curr_user 

# function1: login 
def login():
    global curr_user
    while True:
        user = input('Please provide your user ID: ')
        query = "SELECT user_id FROM user_yelp WHERE user_id=?"
        cur.execute(query, (user,))
        all_user = cur.fetchone()

        if all_user:
            curr_user = all_user[0]
            print(f'Successfully logged in as user {curr_user}.')
            return True
        else:
            print('Invalid user ID. Please try again.')


#function2: Search Business
def searchBussiness():
    while True:
        min_star = input('Please provide the minimum stars, or hit enter to skip: ')
        if not min_star:
            min_star = 0
            break
        try:
            min_star = int(min_star)
            break
        except ValueError:
            print("Please enter a valid integer or hit enter to skip.")

    while True:
        max_star = input('Please provide the maximum stars, or hit enter to skip: ')
        if not max_star:
            max_star = 5
            break
        try:
            max_star = int(max_star)
            break
        except ValueError:
            print("Please enter a valid integer or hit enter to skip.")

    city = input('Please provide the name of the city, or hit enter to skip: ')
    name = input('Please provide the name of the business, or hit enter to skip: ')

    if not city:
        city = "%"
    else:
        city = '%'+city+'%'
    
    if not name: 
        name = '%'
    else:
        name = '%' + name +'%'
    print(f'The minimum number of stars you entered is: {min_star}')
    print(f'The maximum number of stars you entered is: {max_star}')
    print(f'The city you entered is: {city.strip("%")}')
    print(f'The business name you entered is: {name.strip("%")}')
    print('Here is the search result: ')

    query = """
    select business_id, name, address, city, stars from business where city like ? and name like ? and stars<=? and stars >=? order by name;
    """
    cur.execute(query, [city.strip().lower(), name.strip().lower(), max_star, min_star])
    all_bus = cur.fetchall()
    if len(all_bus)==0:
        return '----------Sorry, the search result is empty.----------'

    else:
        print(f"{'ID':<25} {'Name':<30} {'Address':<60} {'City':<20} {'Stars':<5}")
        print('-' * 150)
        for row in all_bus:
            business_id, name, address, city, stars = row
            formatted_output = f"{business_id if business_id else '':<15} {name if name else '':<30} {address if address else '':<60} {city if city else '':<20} {stars if stars else '':<5}"
            print(formatted_output)
        return '----------End of the list----------'

# function3: Search Users
def get_attribute_input(attribute_name):
    while True:
        attr_value = input(f"Please provide if the user is {attribute_name} or not, any number larger than 0.0 for {attribute_name}, otherwise not: ")
        try:
            attr_value = float(attr_value)
            if attr_value > 0.0:
                return f"{attribute_name} > 0"
            else:
                return f"{attribute_name} = 0"
        except ValueError:
            if not attr_value:
                return f"{attribute_name} = 0"
            print(f"Please enter a valid number or hit enter to skip.")

def searchUser():
    name = input('Please provide the user name key word:').strip()

    useful = get_attribute_input('useful')
    funny = get_attribute_input('funny')
    cool = get_attribute_input('cool')

    name = f"%{name.lower()}%" if name else '%'

    query = f"""select user_id, name, useful, funny, cool, yelping_since from user_yelp where name like ? and {useful} 
    and {funny} and {cool} order by name"""
    cur.execute(query, [name,])
    all_user = cur.fetchall()

    if len(all_user) == 0:
        return '----------Sorry, the search result is empty.----------'

    else:
        print(f"{'ID':<25} {'Name':<16} {'Useful':<10} {'Funny':<10} {'Cool':<15} {'Date of register'}")
        print('-' * 150)
        for row in all_user:
            user_id, name, useful, funny, cool, yelping_since = row
            # useful = 'yes' if useful > 0 else 'no'
            # funny = 'yes' if funny > 0 else 'no'
            # cool = 'yes' if cool > 0 else 'no'
            print(f"{user_id:<20} {name:<20} {useful:<10} {funny:<10} {cool:<10} {yelping_since}")

        return '----------End of the list----------'

def makeFriend():
    print(searchUser())
    while True:
        friend = input('Which user above you want to make friend with? Please provide their user ID: ')
        if not friend:
            print('----------Empty input. Please enter a valid user ID.----------')
            continue
        
        query_check_user = "SELECT user_id FROM user_yelp WHERE user_id=?"
        cur.execute(query_check_user, (friend,))
        if not cur.fetchone():
            print(f'----------Invalid user ID: {friend}. Please enter a valid user ID.----------')
            continue

        query = "INSERT INTO friendship VALUES (?, (SELECT user_id FROM user_yelp WHERE user_id=?))"
        
        try:
            cur.execute(query, (curr_user, friend))
            conn.commit()
            return f'----------User with id: {friend} have become friend with you.----------'
        except Exception as e:
            #print(e)  
            return '----------You guys already have friendship.----------'

# funciton5: Write Review
def writeReview():
    while True:
        business_id = input('Please provide the business_id that you want to review for: ')
        if business_id:
            # Check if business_id is valid
            query = "SELECT COUNT(*) FROM business WHERE business_id = ?"
            cur.execute(query, [business_id])
            count = cur.fetchone()[0]
            if count == 0:
                print('----------Invalid business_id. Please try again.----------')
            else:
                break
        else:
            print('----------Must have a valid business_id. Please try again.----------')

    while True:
        stars = input('Please give a star rating, must range from 1 to 5: ')
        try:
            stars = float(stars)
            if 0 < stars <= 5:
                break
            else:
                print('----------Star rating must be between 1 and 5. Please try again.----------')
        except ValueError:
            print('----------Invalid input. Please enter a number between 1 and 5.----------')

    review_id = ''
    while len(review_id) == 0:
        temp =  str(uuid.uuid4())[:22]
        query = "select review_id from review where review_id=?"
        cur.execute(query, [temp])
        old_review_id = cur.fetchone()
        if not old_review_id:
            review_id = temp
            break
    
    query = "insert into review (review_id, business_id, user_id, stars) values ('{0}', '{1}', '{2}', {3})".format(review_id,business_id,curr_user,stars)
    cur.execute(query)
    conn.commit()
    return '----------Successfully insert the review----------'

def main():
    if login()==False:
        return
    running = True
    while running:
        print('Welcomt! Please make a selection from following function: ')
        print('Press 0 to exit/terminate the program')
        print('Press 1 to search busniess')
        print('Press 2 to search user')
        print('Press 3 to make friend')
        print('Press 4 to write a reivew')

        user_input = input('please select from 0 to 4: ')
       
        #print('you select function: '+user_input)
        if int(user_input)==0:
            running=False
            print('----------Exit the program----------')
        elif int(user_input) == 1:
            print('----------Jumping to search busniess function----------')
            print (searchBussiness())
        elif int(user_input) ==2:
            print('----------Jumping to search users function----------')
            print (searchUser())
        elif int(user_input)==3:
            print('----------Jumping to make friend function----------')
            print(makeFriend())
        elif int(user_input) == 4:
            print('----------Jumping to write a reivew for busnises function----------')
            print(writeReview())
        else:
            print('----------This is an invalid input, please select from 0-4.----------')

main()
conn.close()

