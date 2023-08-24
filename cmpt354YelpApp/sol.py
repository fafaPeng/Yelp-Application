import pypyodbc
import uuid

conn = pypyodbc.connect('')  
cur = conn.commit()

global curr_user

def login():
    username=input('please give me your username: ')
    query="select user_id from user_yelp where name='{0}'".format(username)
    cur.execute(query)
    all_user = cur.fetchone()
    if all_user:
        curr_user = all_user[0]
        return True
    return False

def searchBus():
    min_star = input('please give me the mininal stars, or keyboard enter to skip: ')
    max_star = input('please give me the max stars, or keyboard enter to skip: ')
    city = input('please give me the city name, or keyboard enter to skip: ')
    name = input('please give me the business, or keyboard enter to skip: ')

    if not min_star:
        min_star=0
    else:
        min_star = int(min_star)
    
    if not max_star:
        max_star=5
    else:
        max_star = int(max_star)
    
    if not city:
        city = "%"
    else:
        city = '%'+city+'%'
    
    if not name:
        name = '%'
    else:
        name = '%' + name +'%'

    print(min_star, max_star, city, name)

    query = """
    select name, address, city, stars from business where city like ? and name like ? and stars<=? and stars >=? order by name;
    """
    cur.execute(query, [city.strip().lower(), name.strip().lower(), max_star, min_star])
    all_bus = cur.fetchall()
    if len(all_bus)==0:
        return 'There is no business for those critria'

    else:
        for row in all_bus:
            print(row[0], row[1], row[2], row[3])
        return 'done'


def searchUser():
    name = input('Please give me the user name key word:')
    funny = input('please give me if the user is funny or not, 1 for funny, 0 for not:')
    cool = input('please give me if the user is cool or not, 1 for cool, 0 for not:')
    useful = input('please give me if the user is useful or not, 1 for useful, 0 for not:')

    if name:
        name='%'+name.strip().lower()+'%'
    else:
        name = '%'
    
    if int(funny) == 1:
        funny='funny > 0'
    else:
        funny = 'funny = 0'

    if int(cool) == 1:
        cool='cool > 0'
    else:
        cool = 'cool = 0'

    if int(useful) == 1:
        useful='useful > 0'
    else:
        useful = 'useful = 0'

    query ="""select user_id, name, funny, cool, useful, yelping_since from user_yelp where name like ? and {0} 
    and {1} and {2}
    """.format(funny, useful, cool)
    cur.execute(query, [name,])
    all_user = cur.fetchall()
    if len(all_user)==0:
        return 'There is no user for those critria'

    else:
        for row in all_user:
            if int(row[2]) == 0:
                row[2] = 'no'
            else:
                row[2] = 'yes'
            
            if int(row[3]) == 0:
                row[3] = 'no'
            else:
                row[3] = 'yes'

            if int(row[4]) == 0:
                row[4] = 'no'
            else:
                row[4] = 'yes'

            print(row[0], row[1], row[2], row[3])
        return 'done'

def makeFriend():
    print(searchUser())
    friend = input('Which user above you want to make friend with? please give me she/he user id: ')
    if not friend:
        return 'empty friend, please enter a valid user'
    
    query = "insert into friendship values (?, (select user_id from yelp_user where user_id=?))"
    try:
        cur.execute(query, [curr_user, friend])
        cur.commit()
        return '{0} because friend with you, {1}'.format(friend, curr_user)
    except:
        return 'cannot make friend with this user, please double check the user_id'

def writeReview():
    buss_id = input('please give the bussnisess_id you want to reivew for')
    stars = input('please give a star, must range from 1 to 5')


    if not buss_id:
        return 'must have an valid buss_id'

    if not stars or float(stars) > 5 or float(stars) < 0:
        return 'must have a valid star'

    
    # generate a new review id
    review_id = ''
    while len(review_id) == 0:
        temp =  uuid.uuid4()[:22]
        query = "select review_id from review where review_id=?"
        cur.execute(query, [temp])
        temp = cur.fetchone()
        if len(temp) == 0:
            review_id = temp
            break
    
    query = "insert into review (review_id, business_id, user_id, date) values (?, ?, ?, now())"
    
    try:
        cur.execute(query)
        conn.commit()
        return 'succussfully insert the review'
    except:
        return 'cannot insert the review, check your query.'    


def main():
    if not login():
        print('you are not a valid user, please give a valid username')
        return


    running = True
    while running:
        print('please select from following function')
        print('0, exit')
        print('1, search busniess')
        print('2, search user')
        print('3, make friend')
        print('4, write a reivew')
        user_input = input('please select from 0 to 4: ')
        print('you select function: '+user_input)
        if int(user_input)==0:
            running=False
        elif int(user_input) == 1:
            print('going to search busniess function')
            print (searchBus())
        elif int(user_input) ==2:
            print('going to search users function')
            print (searchUser())
        elif int(user_input)==3:
            print('going to make friend function')
            print(makeFriend())

        elif int(user_input) == 4:
            print('going to write a reivew for busnises')
            print(writeReview())
        
        else:
            print('it is an invalid input, please select from 0-4')



main()





# # function3: Search Users
# def searchUser():
#     name = input('Please provide the user name key word:')

#     while True:
#         useful = input('Please provide if the user is useful or not, any number larger than 0.0 for useful, otherwise not: ')
#         try:
#             useful = float(useful)
#             if useful > 0.0:
#                 useful = 'useful > 0'
#             else:
#                 useful = 'useful = 0'
#             break
#         except ValueError:
#             print("Please enter a valid number or hit enter to skip.")
#             if not useful:
#                 useful = 'useful = 0'
#                 break

#     while True:
#         funny = input('Please provide if the user is funny or not, any number larger than 0.0 for funny, otherwise not: ')
#         try:
#             funny = float(funny)
#             if funny > 0.0:
#                 funny = 'funny > 0'
#             else:
#                 funny = 'funny = 0'
#             break
#         except ValueError:
#             print("Please enter a valid number or hit enter to skip.")
#             if not funny:
#                 funny = 'funny = 0'
#                 break

#     while True:
#         cool = input('Please provide if the user is cool or not, any number larger than 0.0 for cool, otherwise not: ')
#         try:
#             cool = float(cool)
#             if cool > 0.0:
#                 cool = 'cool > 0'
#             else:
#                 cool = 'cool = 0'
#             break
#         except ValueError:
#             print("Please enter a valid number or hit enter to skip.")
#             if not cool:
#                 cool = 'cool = 0'
#                 break

#     if name:
#         name = '%' + name.strip().lower() + '%'
#     else:
#         name = '%'

#     query ="""select user_id, name, useful, funny, cool, yelping_since from user_yelp where name like ? and {0} 
#     and {1} and {2} order by name
#     """.format(useful, funny, cool)
#     cur.execute(query, [name,])
#     all_user = cur.fetchall()
#     if len(all_user)==0:
#         return '----------Sorry, the search result is empty.----------'

#     else:
#         print(f"{'ID':<25} {'Name':<16} {'Useful':<10} {'Funny':<10} {'Cool':<15} {'Date of register'}")
#         print('-' * 150)
#         for row in all_user:
#             if int(row[2]) == 0:
#                 row[2] = 'no'
#             else:
#                 row[2] = 'yes'
            
#             if int(row[3]) == 0:
#                 row[3] = 'no'
#             else:
#                 row[3] = 'yes'

#             if int(row[4]) == 0:
#                 row[4] = 'no'
#             else:
#                 row[4] = 'yes'
            
#             print(f"{row[0]:<20} {row[1]:<20} {row[2]:<10} {row[3]:<10} {row[4]:<10} {row[5]}")
#         return '----------End of the list----------'

# function4: Make Friend
# def makeFriend():
#     #print('print current usere here: ',curr_user)
#     #global curr_user 
#     print(searchUser())

#     friend = None
#     while not friend:
#         friend = input('Which user above you want to make friend with? Please provide their user ID: ')
#         if not friend:
#             print('----------Empty input. Please enter a valid user ID.----------')
    
#     query = "insert into friendship values ('{0}', (select user_id from user_yelp where user_id='{1}'))".format(curr_user,friend)
#     try:
#         cur.execute(query)
#         conn.commit()
#         return '----------User with id: {0} have become friend with you.----------'.format(friend)
#     except:
#         return '----------Cannot make friend with this user, this situation may cause by invalid userID input or these two users already have friendship.----------'
