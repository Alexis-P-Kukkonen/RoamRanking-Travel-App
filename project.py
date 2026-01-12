import webbrowser
import os
import sys
import csv
import requests
from user import User
from google import genai
from google.genai import types
from google.genai import errors
import smtplib
from email.message import EmailMessage


users=User.load_users()
API_KEY = "add"
CSEID = "add"
GAPI_KEY = "add"
current_user= None
try:
        client = genai.Client(api_key=GAPI_KEY)
except Exception:
        client = None
def clear_screen():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _= os.system("clear")
def login():
    global current_user
    have = input("Do you have an account? if yes type yes ")


    if have =="yes":
        un = input("Username: ")
        fm = False
        for user in users:
            if user.username.strip().lower() == un.strip().lower():
                fm = True
                pw= input("Password: ")
                if pw == user.password:
                    current_user = user
                else:
                    forgot = input("Did you forget your password? If yes type yes ")
                    if forgot == "yes":
                        seq = input("What city did your parents meet? ")
                        if seq == user.security:
                            current_user = user
                            change = input("Would you like to change your password? If yes type yes ")
                            if change == "yes":
                                user.password = input("New Password: ")
                                User.save_users(users)
                break
        if not fm:
            print("No user found with that username.")
    else:
        create= input("would you like to create one? if yes type yes ")
        if create =="yes":
            us = input("Username: ")
            name_taken = False
            for user in users:
                if user.username.lower()== us.lower():
                    name_taken = True
                    break
            if name_taken:
                print("That username is taken")
                return
            pa = input("Password: ")

            clear = False
            tries =0
            while not clear and tries<3:
                check = input("Retype Password: ")
                if check ==pa:
                    clear= True
                else:
                    tries +=1
            if clear:
                seq = input("What city did your parents meet? ")
                new_user = User(us,pa,seq)
                users.append(new_user)
                current_user = new_user

                User.save_users(users)


def search_image(query):
    google = f"https://www.googleapis.com/customsearch/v1?key=add&q={query}&searchType=image"

    try:  # change to google
        response = requests.get(google)
        response.raise_for_status()
        results = response.json()
        next = True
        n = 0
        while next == True:
            image_results = results.get("items", [{}])[n]
            imaurl = image_results.get("link")
            if imaurl:
                webbrowser.open(imaurl)
            else:
                print("couldn't find photo")
            qu = input(
                "would you like to see the next photo? If so type next: ")
            if qu != "next":
                next = False
            n += 1

        return imaurl

    except requests.exceptions.ConnectionError as pop:
        sys.exit(
            f"Couldn't connect to the google Images website. \nError: {pop}")
    except requests.exceptions.Timeout as pop:
        sys.exit(f"google websited timed out. \nError: {pop}")
    except requests.exceptions.HTTPError as pop:
        sys.exit(
            f"There was an error with the link to the google Images website.\nError: {pop}")
    except requests.exceptions.RequestException as pop:
        sys.exit(
            f"Request to use the google Images website was denied. \nError: {pop}")


def add_place(place):
    add = False
    with open("travel.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for r in reader[1:]:
            if r["place"] == place:
                again = input(
                    f"{place} is already on your. Would you like to add it again? If yes type yes")
                if again == "yes":
                    add = True

    if add:
        with open("travel.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile)
            currency, cost = cost(place)
            writer.writerow(
                {"place": place, "currency": currency, "cost": cost})


def cost(place):
    if not client:
        return "Unknown"
    search_tool = types.Tool(google_search=types.GoogleSearch())
    config = types.GenerateContentConfig(tools =[search_tool])
    prompt = f"cost of {place} return only the currency and the price and nothing else if free return $0 I don't want any other words just price of an adult ticket do not give me more information return format currency price"
    try:
        gresponse = client.models.generate_content(model= "gemini-2.5-flash", contents = prompt,config = config)
        return gresponse.text
    except Exception:
        return "Error with Gemini"





def new_list():
    global current_user
    name = input("What is the name of the new list: ")

    fieldnames = ["place","score","votes","cost","description","open hours","image url","personal note","scored"]

    with open(f"{name}.csv", mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
    current_user.lists.append(f"{name}.csv")

    User.save_users(users)







def hours(place):
    if not client:
        return "Unknown"
    search_tool = types.Tool(google_search=types.GoogleSearch())
    config = types.GenerateContentConfig(tools =[search_tool])
    prompt = f"for the place {place} Summarize the standard daily hours, specific days or date ranges (e.g., 'Mon-Fri'), and any seasonal changes or temporary closures in 2 sentences or less"
    try:
        gresponse = client.models.generate_content(model= "gemini-2.5-flash", contents = prompt,config = config)
        return gresponse.text
    except Exception:
        return "Error with Gemini"

def description(place):
    if not client:
        return "Unknown"
    search_tool = types.Tool(google_search=types.GoogleSearch())
    config = types.GenerateContentConfig(tools =[search_tool])
    prompt = f"give me a brief description of {place} like what and where it is, interesting history, and what to do there within a paragraph"
    try:
        gresponse = client.models.generate_content(model= "gemini-2.5-flash", contents = prompt,config = config)
        return gresponse.text
    except errors.ClientError:
        return "to many requests with Gemini"





def display_lists():
    if len(current_user.lists)==0:
        create = input("You have no Travel Docs would you like to create one? If yes type yes ")
        if create == "yes":
            new_list()
        return False
    else:
        print(f"\n=---{current_user.username}'s Saved lists---")
        for filename in current_user.lists:
            print(filename[:-4])
        return True

def menu():
    con = True
    while con:
        clear_screen()
        options = ["Add new place", "Start a list", "Score unscored places","Invite a friend","Share list with friend","View list","Exit"]
        for i, opt in enumerate(options, start=1):
            print(f"{i}. {opt}")
        choice = 0
        while not (1<= choice <= len(options)):
            try:
                choice = int(input("Number: "))
            except ValueError:
                print("Please enter a valid number.")
        if choice == 1:
            still = True
            while still == True:
                place = input("where would you like to go? ")
                desc = description(place)
                print(desc)
                print()
                cos = cost(place)
                print(cos)
                url =search_image(place)
                print()
                hour = hours(place)
                print(hour)
                print()
                add = input(f"would you like to add {place} to one of your lists? If yes type yes: ")
                if add == "yes":
                    clear_screen()
                    add_to_list(place, cos, desc, hour, url)
                    st = input("Would you like to add another place? If yes type yes? ")
                    if st== "yes":
                        still = True
                    else:
                        still = False
                else:
                    look = input("Would you like to look up another place? If yes type yes: ")
                    if look == "yes":
                        still = True
                    else:
                        still = False
        if choice == 2:
            new_list()
        if choice == 3:
            unscored()
        if choice ==4:
            add_friend()
        if choice == 5:
            collaborate()
        if choice == 6:
            rank()
            input("press enter to return to menu")
        if choice == 7:
            con =False

def collaborate():
    global current_user
    display_lists()
    li = input("Which list would you like to share? ")
    if f"{li}.csv" not in current_user.lists:
        cre = input(f"{li} is not part of your lists. Would you like to create a new one? (yes/no) ")
        if cre=="yes":
            new_list()
        else:
            return

    friend = input("Friends Username: ")
    fm = False
    for user in users:
        if user.username.strip().lower() == friend.strip().lower():
            fm = True
            fr = user

    if fm:
        real = current_user
        current_user = fr
        join_list(f"{li}.csv")
        current_user =real
    else:
        no = input("Your friend is not a RoamRanking user. Would you like to invite them? (yes/no) ")
        if no == "yes":
            add_friend()
        else:
            print(f"{friend} was not added to ")
def join_list(filename):
    global current_user
    if filename not in current_user.lists:
        current_user.lists.append(filename)
        User.save_users(users)

    else:
        print(f"You have already sent (filename[:-4]) to (current_user.username)")
def add_to_list(place, cost, description, time, url):
    has_lists = display_lists()
    li = input("Which list would you like to add to? ")
    fieldnames = ["place","score","votes","cost","description","open hours","image url","personal note","scored"]

    if f"{li}.csv" in current_user.lists:
        with open(f"{li}.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for r in reader:
                if r.get("place") == place.lower():
                    sti = input(f"{place} is already in {li}. Would you still like to add to {li}? If yes type yes: ")
                    if not sti == "yes":
                        return

        with open(f"{li}.csv", mode = "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames = fieldnames)
            per = input("Personal note: ")
            sc = input(f"how would you rate on a scale from 1 to 5 your interest in {place}? ")
            writer.writerow({
            "place": place,
                "score": sc,
                "votes": sc,
                "cost": cost,
                "description": description,
                "open hours": time,
                "image url": url,
                "personal note": per,
                "scored": " ("+current_user.username+")"
            })
    else:
            cre =input(f"{li} is no in your lists. Would you like to create a new list? (yes/no)")
            if cre == "yes":
                new_list()
                return add_to_list(place,cost,description,time,url)

def add_friend():
    user = input("What is the name that this person would know you by? ")
    user_email = input("Your email: ")
    app_password = input("What is your 16-digit App password?\n1. Go to your Google Account: Visit myaccount.google.com.\n2. Security Tab: Click on 'Security' in the left-hand menu.\n3. 2-Step Verification: Scroll down to the 'How you sign in to Google' section. Click on '2-Step Verification' (make sure it says 'On').\n4. App Passwords: Scroll to the very bottom of the 2-Step Verification page. You will see a section called 'App passwords'.\n    Note: If you don't see it, search for 'App passwords' in the search bar at the top of the account page.\n5. Create Name: Give it a name you'll remember, like Python Travel Project.\n6. Copy the Code: Click Create. A yellow box will appear with a 16-character code (e.g., abcd efgh ijkl mnop).\n    Important: Do not close the box but simply transfer the code over to the program. You will never see it again once you close the window.\n\nPIN: ")
    msg=EmailMessage()
    msg["Subject"] = "Invite to RoamRanking"
    msg["From"]= user_email
    target = input("What is the recipients name? ")
    target_email = input("What is their email address: ")
    msg["To"]= target_email
    msg.set_content(f"Hi {target}, \n\n    You have been invited by {user} to RoamRanking. Save, share, and rank travel spots with friends. RoamRanking helps you prioritize your itinerary so you never miss a must-see destination. Welcome!\n\nLinks: https://prod.liveshare.vsengsaas.visualstudio.com/join?871D4DE263A6F4D4CE74193748D6297B3703")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
            smtp.login(user_email, app_password)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception:
        print("Error sending email")



def unscored():
    display_lists()
    li = input("Which list would you like to score? ")
    all_rows=[]
    if f"{li}.csv" in current_user.lists:
        with open(f"{li}.csv") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if not row.get("place"):
                    continue
                row["scored"]= row.get("scored") or ""
                if f"({current_user.username.strip()})" not in row["scored"]:
                    try:
                        sc = input(f"how would you rate on a scale from 1 to 5 your interest in {row.get("place")}? ")
                        if not sc: sc = "0"
                        row["scored"] += " ("+current_user.username+")"


                        votes = int(row["votes"] or 0)
                        votes += int(sc)
                        row["votes"]=str(votes)

                        sco = votes / row["scored"].count(")")
                        row["score"] = str(round(sco,2))
                    except ValueError:
                        print("Invalid input. Skipping place")
                all_rows.append(row)
        with open(f"{li}.csv", mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)
def rank():
    display_lists()
    li = input("which list would you like to see: ")
    filename = f"{li}.csv"
    if filename in current_user.lists:
        places=[]
        try:
            with open(filename, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row["score"]= float(row.get("score", 0)or 0)
                    places.append(row)
            ranked = sorted(places, key = lambda x :x["score"], reverse =True)
            print(f"\n------{li}-------")
            for i, p in enumerate(ranked, start=1):
                print(f"{i}. {p["place"]}")
        except FileNotFoundError:
            print(f"{li} could not be found")



def main():
    clear_screen()
    login()
    if current_user == None:
        sys.exit("You have not given your login information. Try rerunning the program")
    clear_screen()
    menu()


if __name__ == "__main__":
    main()
