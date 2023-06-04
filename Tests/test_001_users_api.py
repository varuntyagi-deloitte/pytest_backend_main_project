import json

import pytest

from Logs.log_file import log_class
from Utilities.readexcel import read_data_by_value as read
from Utilities.readexcel import update_data_to_sheet as write
from TestData.json_files import *

import requests


@pytest.mark.usefixtures("fixture")
class TestVarunUsersAPI(log_class):
    @pytest.mark.order(1)
    def test_001_get_api_health_check(self):
        log = self.test_log()
        log.info("get /health-check api testing started")
        response = requests.get(read("Data_Sheet", "base_url") + "/health-check")
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        log.info("Response data", parsed_data)
        assert parsed_data["message"] == read("Messages_Sheet", "health_check_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")
        assert parsed_data["success"] == True, "Failed Test"

    @pytest.mark.order(2)
    def test_002_get_api_health_check_negative(self):
        log = self.test_log()
        log.info("get /health-check api testing started for wrong api endpoint")
        response = requests.get(read("Data_Sheet", "base_url") + "/health_check")
        assert response.status_code == 404, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        assert parsed_data["message"] == read("Messages_Sheet", "health_check_negative_message"), "Failed Test"
        log.info("Success Message asserted successfully")

    @pytest.mark.order(3)
    def test_003_post_api_register_users(self):
        log = self.test_log()
        log.info("post /users/register api testing started")
        response = requests.post(read("Data_Sheet", "base_url") + "/users/register", data=register_payload())
        assert response.status_code == 201, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        assert parsed_data["message"] == read("Messages_Sheet", "register_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")
        write("Data_Sheet", "id", parsed_data["data"]["id"])
        assert parsed_data["data"]["name"] == read("Data_Sheet", "name"), "Failed Test"
        assert parsed_data["data"]["email"] == read("Data_Sheet", "email"), "Failed Test"
        log.info("Response data asserted successfully")

    @pytest.mark.order(4)
    def test_004_post_api_register_users_negative(self):
        log = self.test_log()
        log.info("post /users/register api testing started for registered user")
        response = requests.post(read("Data_Sheet", "base_url") + "/users/register",
                                 data=register_payload_with_registered_email())
        assert response.status_code == 409, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        assert parsed_data["message"] == read("Messages_Sheet", "register_negative_message"), "Failed Test"
        log.info("Success Message asserted successfully")

    @pytest.mark.order(5)
    def test_005_post_api_users_login(self):
        log = self.test_log()
        log.info("post /users/login api testing started")
        response = requests.post(read("Data_Sheet", "base_url") + "/users/login", data=login_payload())
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        write("Data_Sheet", "token", parsed_data["data"]["token"])
        assert parsed_data["message"] == read("Messages_Sheet", "login_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")
        assert parsed_data["data"]["id"] == read("Data_Sheet", "id"), "Failed Test"
        assert parsed_data["data"]["name"] == read("Data_Sheet", "name"), "Failed Test"
        assert parsed_data["data"]["email"] == read("Data_Sheet", "email"), "Failed Test"
        log.info("Response data asserted successfully")

    @pytest.mark.order(6)
    def test_006_post_api_users_login_negative(self):
        log = self.test_log()
        log.info("post /users/login api testing started for invalid email and password")
        response = requests.post(read("Data_Sheet", "base_url") + "/users/login",
                                 data=login_payload_with_wrong_email_password())
        assert response.status_code == 401, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        assert parsed_data["message"] == read("Messages_Sheet", "login_negative_message"), "Failed Test"
        log.info("Success Message asserted successfully")

    @pytest.mark.order(7)
    def test_007_get_api_users_profile(self):
        log = self.test_log()
        log.info("get /users/profile api testing started")
        response = requests.get(read("Data_Sheet", "base_url") + "/users/profile",
                                headers={'Content-Type': 'application/json',
                                         'x-auth-token': '{}'.format(read("Data_Sheet", "token"))})
        parsed_data = json.loads(json.dumps(response.json()))
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        assert parsed_data["message"] == read("Messages_Sheet", "get_profile_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")
        assert parsed_data["data"]["id"] == read("Data_Sheet", "id"), "Failed Test"
        assert parsed_data["data"]["name"] == read("Data_Sheet", "name"), "Failed Test"
        assert parsed_data["data"]["email"] == read("Data_Sheet", "email"), "Failed Test"
        log.info("Response data asserted successfully")

    @pytest.mark.order(8)
    def test_008_patch_api_users_profile(self):
        log = self.test_log()
        log.info("patch /users/profile api testing started")
        response = requests.patch(read("Data_Sheet", "base_url") + "/users/profile", data=profile_payload(),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'x-auth-token': '{}'.format(read("Data_Sheet", "token"))})
        parsed_data = json.loads(json.dumps(response.json()))
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        assert parsed_data["message"] == read("Messages_Sheet", "patch_profile_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")
        assert parsed_data["data"]["id"] == read("Data_Sheet", "id"), "Failed Test"
        assert parsed_data["data"]["name"] == read("Data_Sheet", "name"), "Failed Test"
        assert parsed_data["data"]["email"] == read("Data_Sheet", "email"), "Failed Test"
        assert parsed_data["data"]["phone"] == str(read("Data_Sheet", "phone")), "Failed Test"
        assert parsed_data["data"]["company"] == read("Data_Sheet", "company"), "Failed Test"
        log.info("Response data asserted successfully")

    @pytest.mark.order(9)
    def test_009_post_api_users_forgot_password(self):
        log = self.test_log()
        log.info("post /users/forgot-password api testing started")
        response = requests.post(read("Data_Sheet", "base_url") + "/users/forgot-password",
                                 data=forgot_password_payload())
        parsed_data = json.loads(json.dumps(response.json()))
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        assert parsed_data[
                   "message"] == "Password reset link successfully sent to " + read("Data_Sheet",
                                                                                    "email") + ". Please verify by clicking on the given link", "Failed Test"
        log.info("Success Message asserted successfully")

    @pytest.mark.order(10)
    def test_010_post_api_users(self):
        log = self.test_log()
        log.info("post /users/change-password api testing started")
        response = requests.post(read("Data_Sheet", "base_url") + "/users/change-password",
                                 data=change_password_payload(),
                                 headers={'Content-Type': 'application/x-www-form-urlencoded',
                                          'x-auth-token': '{}'.format(read("Data_Sheet", "token"))})
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        assert parsed_data["message"] == read("Messages_Sheet", "change_password_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")
