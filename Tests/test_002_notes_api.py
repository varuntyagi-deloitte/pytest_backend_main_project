import json

import pytest

from Logs.log_file import log_class
from Utilities.readexcel import read_data_by_value as read
from Utilities.readexcel import update_data_to_sheet as write
from TestData.json_files import *

import requests


@pytest.mark.usefixtures("fixture")
class TestVarunNotesAPI(log_class):
    note_id = []

    @pytest.mark.order(11)
    @pytest.mark.parametrize("category", ["Home", "Work", "Personal"])
    def test_003_post_api_create_notes(self, category):
        log = self.test_log()
        log.info("post /notes api testing started")
        response = requests.post(read("Data_Sheet", "base_url") + "/notes", data=create_notes_payload(category),
                                 headers={'Content-Type': 'application/x-www-form-urlencoded',
                                          'x-auth-token': '{}'.format(read("Data_Sheet", "token"))})
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        assert parsed_data["message"] == read("Messages_Sheet", "post_notes_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")
        assert parsed_data["data"]["title"] == read("Data_Sheet", "title"), "Failed Test"
        assert parsed_data["data"]["description"] == read("Data_Sheet", "description"), "Failed Test"
        assert parsed_data["data"]["category"] == category, "Failed Test"
        log.info("Response data asserted successfully for " + "'" + category + "'" + " Category")

    @pytest.mark.order(12)
    def test_004_get_api_get_notes(self):
        log = self.test_log()
        log.info("get /notes api testing started to get all the notes")
        response = requests.get(read("Data_Sheet", "base_url") + "/notes",
                                headers={'x-auth-token': '{}'.format(read("Data_Sheet", "token"))})
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        for i in range(len(parsed_data["data"])):
            self.note_id.append(parsed_data["data"][i]["id"])
            if read("Data_Sheet", "id") == parsed_data["data"][i]["user_id"]:
                assert True
            else:
                assert False
            assert parsed_data["data"][i]["title"] == read("Data_Sheet", "title"), "Failed Test"
            assert parsed_data["data"][i]["description"] == read("Data_Sheet", "description"), "Failed Test"
        log.info("Response data asserted successfully")
        assert parsed_data["message"] == read("Messages_Sheet", "get_notes_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")
        assert len(parsed_data["data"]) == 3, "Failed Test"

    @pytest.mark.order(13)
    def test_005_get_api_get_note_by_id(self):
        log = self.test_log()
        log.info("get /notes/id api testing started to get a note by id")
        response = requests.get(read("Data_Sheet", "base_url") + "/notes/" + self.note_id[0],
                                data=get_note_by_id_payload(self.note_id[0]),
                                headers={'x-auth-token': '{}'.format(read("Data_Sheet", "token"))})
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        assert parsed_data["message"] == read("Messages_Sheet", "get_notes_by_id_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")
        assert parsed_data["data"]["title"] == read("Data_Sheet", "title"), "Failed Test"
        assert parsed_data["data"]["description"] == read("Data_Sheet", "description"), "Failed Test"
        log.info("Response data asserted successfully")

    @pytest.mark.order(14)
    def test_006_put_api_edit_notes(self):
        log = self.test_log()
        log.info("put /notes/id api testing started to update a note by id")
        response = requests.put(read("Data_Sheet", "base_url") + "/notes/" + self.note_id[0],
                                data=edit_note_payload(self.note_id[0]),
                                headers={'x-auth-token': '{}'.format(read("Data_Sheet", "token"))})
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        assert parsed_data["message"] == read("Messages_Sheet", "put_notes_by_id_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")
        assert parsed_data["data"]["title"] == read("Data_Sheet", "title"), "Failed Test"
        assert parsed_data["data"]["description"] == read("Data_Sheet", "description"), "Failed Test"
        assert parsed_data["data"]["completed"] == False, "Failed Test"
        assert parsed_data["data"]["category"] == read("Data_Sheet", "category"), "Failed Test"
        log.info("Response data asserted successfully")

    @pytest.mark.order(15)
    def test_007_patch_api_users(self):
        log = self.test_log()
        log.info("patch /notes/id api testing started to update the completed status of a note")
        response = requests.patch(read("Data_Sheet", "base_url") + "/notes/" + self.note_id[0],
                                  data=update_note_as_completed_payload(self.note_id[0]),
                                  headers={'x-auth-token': '{}'.format(read("Data_Sheet", "token"))})
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        assert parsed_data["message"] == read("Messages_Sheet", "patch_notes_by_id_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")
        assert parsed_data["data"]["completed"] == True, "Failed Test"
        log.info("Response data asserted successfully")

    @pytest.mark.order(16)
    def test_008_delete_api_users(self):
        log = self.test_log()
        log.info("delete /notes/id api testing started to delete a note by id")
        response = requests.delete(read("Data_Sheet", "base_url") + "/notes/" + self.note_id[0],
                                   data=get_note_by_id_payload(self.note_id[0]),
                                   headers={'x-auth-token': '{}'.format(read("Data_Sheet", "token"))})
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        assert parsed_data["message"] == read("Messages_Sheet", "delete_notes_by_id_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")

    @pytest.mark.order(17)
    def test_009_delete_api_logout_user_account(self):
        log = self.test_log()
        log.info("delete /users/logout api testing started to logout a user")
        response = requests.delete(read("Data_Sheet", "base_url") + "/users/logout",
                                   headers={'Content-Type': 'application/json',
                                            'x-auth-token': '{}'.format(read("Data_Sheet", "token"))})
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        assert parsed_data["message"] == read("Messages_Sheet", "logout_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")

    @pytest.mark.order(18)
    def test_010_post_api_user_login(self):
        response = requests.post(read("Data_Sheet", "base_url") + "/users/login", data=new_login_payload())
        assert response.status_code == 200, "Failed Test"
        parsed_data = json.loads(json.dumps(response.json()))
        write("Data_Sheet", "new_token", parsed_data["data"]["token"])

    @pytest.mark.order(19)
    def test_011_delete_api_delete_user_account(self):
        log = self.test_log()
        log.info("delete /users/delete-account api testing started to delete a user")
        response = requests.delete(read("Data_Sheet", "base_url") + "/users/delete-account",
                                   headers={'x-auth-token': '{}'.format(read("Data_Sheet", "new_token"))})
        assert response.status_code == 200, "Failed Test"
        log.info("Status Code asserted successfully")
        parsed_data = json.loads(json.dumps(response.json()))
        assert parsed_data["message"] == read("Messages_Sheet", "delete_account_success_message"), "Failed Test"
        log.info("Success Message asserted successfully")
