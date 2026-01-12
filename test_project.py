import project
from user import User
import pytest
import os
from unittest.mock import patch, MagicMock
import responses


def test_login():
    us = User("grace", "password", "paris")
    assert us.username == "grace"
    assert us.security == "paris"
    assert us.lists ==[]
@patch("os.system")
def test_clear_screen(mock_system):
   project.clear_screen()
   ter = "cls" if os.name == "nt" else "clear"
   mock_system.assert_called_once_with(ter)

def test_new_list():

    us = User("grace", "password", "paris")
    us.lists =[]
    project.current_user = us

    with patch("builtins.input", return_value="vacation"),\
        patch("user.User.save_users"):
       project.new_list()
    assert len(us.lists)==1
    assert us.lists[0]=="vacation.csv"
    if os.path.exists("vacation.csv"):
        os.remove("vacation.csv")


@patch("project.requests.get")
@patch("project.webbrowser.open")
@patch("builtins.input", side_effect=["no"])
def test_search_image_api_access(mock_browser, mock_get,mock_input):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value ={
        "items": [{"link": "https://example.com/photo.jpg"}]
    }
    query = "Paris"
    result = project.search_image(query)
    assert mock_get.called
