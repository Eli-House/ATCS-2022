from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:

    def __init__(self, current_user=None):
        self.current_user = current_user
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):

        registration = False
        taken = False
        users = db_session.query(User.username)

        while registration == False:
            uname = input("Create your twitter handle:\n")
            passOne = input("Create your password:\n")
            passTwo = input("Verify your password:\n")

            for usernames in users:
                if uname == usernames:
                    print("Username is taken, try again.")
                    taken = True
                    break

            if taken == False:
                if passOne == passTwo:
                    newUser = User(uname, passOne)
                    db_session.add(newUser)
                    db_session.commit()
                    print("Welcome " + uname)
                    registration = True
                    self.current_user = uname
                else: 
                    print("Passwords dont match, try agian.")
        
    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        users = db_session.query(User.username, User.password)

        username = input("Enter your username:\n")
        password = input("Enter your password:\n")

        login = False
        for usernames, passwords in users:
            if username == usernames and password == passwords:
                print("Welcome " + usernames)
                login = True
                self.current_user = username
                break
        if login == False:
            print("Invalid username or password")

    
    def logout(self):
        self.current_user = None
        self.startup()

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):

        print("Select a menu option")
        print("1. Log in")
        print("2. Sign up")
        print("3. Exit")

        option = int(input(""))

        if option == 1:
            self.login()
        elif option == 2:
            self.register_user()
        elif option == 3:
            self.end()

    def follow(self):
        follow = input("Enter the username of the person you want to follow:\n")
        users = db_session.query(User.username)
        following = db_session.query(Follower.following_id).where(self.current_user == Follower.follower_id)
        real_user = True
        already_following = False

        for user in following:
            user = str(user)[2:]
            user = user[:len(user)-3]
            if follow == user:
                print("You already follow " + follow)
                already_following = True
                break
            
        if already_following == False:
            for users.username in users:
                user = str(users.username)[2:]
                user = user[:len(user)-3]
                if follow == user:
                    print("you are now folling " + follow)
                    new_follower = Follower(self.current_user, follow)
                    db_session.add(new_follower)
                    db_session.commit()
                    real_user = True
                    break

        if real_user == False:
            print("This user does not exits")

    def unfollow(self):
        unfollow = input("Enter the username of the person you want to unfollow:\n")
        user = db_session.query(User).where(User.username==unfollow).first()
        following = db_session.query(Follower).where(Follower.follower_id==self.current_user).all()
        follow = False
        for follower in following:
            if user.username == follower.following_id:
                print("You are longer following " + user)
                db_session.delete(follower)
                db_session.commit()
                follow = True
                break

        if follow == False:
            print("You dont follow " + user)

    def tweet(self):
        content = input("Enter the message you want to tweet: ")
        tags = input("Enter tags (seperate by spaces): ")
        timestamp = datetime.now()
        new_tweet = Tweet(content, timestamp, self.current_user)
        tag = db_session.query(Tag).all()

        for hashtag in tags.split():
            new_tag = True
            for made_tag in tag:
                if hashtag == made_tag.content:
                    new_tweet.tags.append(made_tag)
                    new_tag = False
            if new_tag == True:
                create_tag = Tag(hashtag) 
                new_tweet.tags.append(create_tag)

        db_session.add(new_tweet)
        db_session.commit()
     
    def view_my_tweets(self):
        tweets = db_session.query(Tweet).where(Tweet.username == self.current_user)
        self.print_tweets(tweets)
            
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        pass

    def search_by_user(self):
        users = db_session.query(User.username)
        uname = input("Enter a username: \n")
        real_user = False
        
        for users.username in users:
            user = str(users.username)[2:]
            user = user[:len(user)-3]
            if uname == user:
                real_user = True
                tweets = db_session.query(Tweet).where(Tweet.username == uname)
                break
        if real_user == True:
            self.print_tweets(tweets)
        if real_user == False:
            print("No user has that name")

    def search_by_tag(self):
        pass

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        while self.current_user == None:
            self.startup()
            active = True

        while active == True:
            self.print_menu()
            option = int(input(""))

            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
                active = False
        
        self.end()

