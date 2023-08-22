import os
import re
import shutil
from datetime import datetime


class CoverLetter:
    #  Cover Letter templates.
    web_template_source = "./cover_letter_templates/cover_letter_template_web.txt"
    template_destination = "./cover_letter_temp_files/"

    def __init__(self, version):
        # Attributes
        self._version = version
        self._date = None
        self._cover_letter = None
        self._company = None
        self._role = None

        self.create_template()

    # Setters
    def set_company(self, company_name):
        self._company = company_name

    def set_job_role(self, job_name):
        self._role = job_name

    def set_date(self, date):
        self._date = date

    # Getters
    def get_company(self):
        return self._company

    def get_job_role(self):
        return self._role

    def get_date(self):
        return self._date

    # Class Actions
    def create_template(self):
        if self._version == "web":
            self._cover_letter = (CoverLetter.template_destination + self._version +
                                  "_cover_letter " + str(datetime.now()))
            shutil.copy(CoverLetter.web_template_source, self._cover_letter)

    def insert_data(self):
        # Check if data is present
        if self._date is None or self._role is None or self._company is None:
            missing_data = []
            if self._date is None:
                missing_data.append("Date")
            if self._role is None:
                missing_data.append("Role")
            if self._company is None:
                missing_data.append("Company")

            missing_data_as_string = ""
            while len(missing_data) > 0:
                if len(missing_data) == 1:
                    missing_data_as_string += missing_data.pop()
                else:
                    missing_data_as_string += missing_data.pop() + ", "
            raise Exception(missing_data_as_string + " is missing.")

        with open(self._cover_letter, "r") as f:
            contents = f.read()

        re.sub("___DATE___", self._date, contents)
        re.sub("___JOBTITLE___", self._role, contents)
        re.sub("___COMPANYNAME___", self._company, contents)

        with open(self._cover_letter, "w") as f:
            f.write(contents)

    def generate_word_doc(self):
        pass

    def clean_up(self):
        # clean up temp files
        for file in os.listdir(CoverLetter.template_destination):
            os.remove(os.path.join(CoverLetter.template_destination, file))
