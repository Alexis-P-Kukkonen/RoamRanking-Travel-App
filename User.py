import json
import os
users = []
class User:
    def __init__(self, username, password, security, lists = None):
        self._username = username
        self._password = password
        self._security = security
        self._lists = lists if lists is not None else []

    def to_dict(self):
        return{
            "username" : self.username,
            "password": self.password,
            "security": self.security,
            "lists" : self.lists
        }
    @staticmethod
    def save_users(user_list):
        data = []
        for u in user_list:
            data.append({
                "username": u.username,
                "password": u.password,
                "security": u.security,
                "lists" : u.lists
            })
        with open("users.json", "w") as file:
            json.dump(data, file, indent = 5)
    @staticmethod
    def load_users():
        try:
            with open("users.json", "r") as file:
                data = json.load(file)
                temp_list = []
                for user_data in data:
                    newuser=User(user_data["username"], user_data["password"], user_data["security"])
                    newuser.lists= user_data.get("lists", [])
                    temp_list.append(newuser)
                return temp_list
        except (FileNotFoundError, json.JSONDecodeError):
            print("User was not saved")
            return []

    @property
    def username(self):
        return self._username
    @username.setter
    def username(self, name):
        self._username = name
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, password):
        trys = 0
        confirmed = False
        while trys<3 and not confirmed:
            gold = input("Old password: ")
            if gold == self._password:
                self._password = password
                confirmed = True
            trys+=1
        sec= input("What city did your parents meet?")
        if sec == self._security:
            self._password = password
            confirmed = True
        if not confirmed:
            print("Too many failed attempts. Couldn't change password")
    @property
    def security(self):
        return self._security

    @security.setter
    def security(self, security):
        trys = 0
        confirmed = False
        old = self._password
        while trys<3 and not confirmed:
            gold = input("Old password: ")
            if gold == self._password:
                self._security = security
                confirmed = True
            trys+=1
        sec= input("What city did your parents meet?")
        if sec == self._security:
            self._security = security
            confirmed = True
        if not confirmed:
            print("Too many failed attempts. Couldn't change security question answer.")

    @property
    def lists(self):
        return self._lists
    @lists.setter
    def lists(self, value):
        if isinstance(value,list):
            self._lists= value
        else:
            self._lists.append(value)
