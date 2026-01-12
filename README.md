# RoamRanking: Share, Rank, and Travel
## Video Demo:[https://youtu.be/MXUyraqYb-M]
## Description:

RoamRanking is a travel app that allows you to share your travel plans with friends. You both can add, search, and rank these places so you don't miss out on mutually important places.

I built this app because I plan to travel after finishing high school. I this trip for a long time but find it agonizing to manual count and remember all the important places. Adding another person just jumbled up my organized chaos. This app is made to help keep plans organized while making sure I prioritize my and my friends wants.

### File Description

**project.py**: This is the bulk of my project. It has my main function as well as the imported libraries, csv files, and my own personal User class. It directs users to a menu where they can view to share, list, rank, or view places they would like to go and saves their preferences on a csv file. This csv file is named what ever the person wants, and with a new list of places and collaborators, a new csv file is created every time.
**test_project.py** :This file is used to check some of my functions within project.py. It uses pytest to check if functions have carried out the purpose or in some cases partially carried out. This is because I am using ai within my project and cannot get the same answer everytime.
**user.py**:This file is a class file that creates and saves new users to a json file where their information can be saved even when users exit the program. It also allows for changes to the password and security questions.
**requirements.txt**: This file just lists the external libraries that I needed to create and run this program

### Design Choices:

For this project I wanted to learn the best way to save my list information. I remembered our lesson on csv files, which is why I saved the places in the lists to the csvfiles. But, when I was trying to save user data such as login information, I was having difficulty parsing through the specific pieces of information as each users required informations kept changing throughout the process of making this program. That is why I opted to use **JSON** instead, as it made my life easier due to its nesting nature. The list were still kept in a **Csv** because they could then be exported to sheets or another table more easily.
Another big design choice I made was to use an API for google gemini instead of using one for a google custom search engine. Originally I used a custom search engine api to go through all of the prices of an attractions by using an re. expression that had the symbols for a lot of exceptable currencies. The problem was that there were so many answers and if something was free I couldn't convey that. To be more particular I used gemini to give me the price of the adult ticket to one of these attractions.
### Future Features
In the future I want to add different circumstances for people to gain a more accurate ticket price. When Users sign in they would be asked their name, age, any disabilities, military service, height and citizenship as it can be used to get discounted tickets.
I also want to create a function where I can get rid of places or lists from a person's account
