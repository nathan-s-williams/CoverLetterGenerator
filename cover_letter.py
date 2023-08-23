import os
import re
import shutil
import string
from datetime import datetime
from docx import Document


class CoverLetter:
    #  Cover Letter templates.
    web_template_source = "./cover_letter_templates/cover_letter_template_web.txt"
    template_destination = "./cover_letter_temp_files/"

    def __init__(self, version: string):
        # Attributes
        self._version = version
        self._date = None
        self._cover_letter = None
        self._company = None
        self._role = None
        self._cover_letter_content = None
        self._template_populated = False
        # Initialize template
        self.create_template()

    # Setters
    def set_company(self, company_name: string):
        self._company = company_name

    def set_job_role(self, job_name: string):
        self._role = job_name

    def set_date(self, date: string):
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
            list_of_missing_data = []
            if self._date is None:
                list_of_missing_data.append("Date")
            if self._role is None:
                list_of_missing_data.append("Role")
            if self._company is None:
                list_of_missing_data.append("Company")

            missing_data = ""
            while len(list_of_missing_data) > 0:
                if len(list_of_missing_data) == 1:
                    missing_data += list_of_missing_data.pop()
                else:
                    missing_data += list_of_missing_data.pop() + ", "
            raise Exception(missing_data + " is missing.")

        with open(self._cover_letter, "r") as f:
            self._cover_letter_content = f.read()

        self._cover_letter_content = re.sub("___DATE___", self._date, self._cover_letter_content)
        self._cover_letter_content = re.sub("___JOBTITLE___", self._role, self._cover_letter_content)
        self._cover_letter_content = re.sub("___COMPANYNAME___", self._company, self._cover_letter_content)

        with open(self._cover_letter, "w") as f:
            f.write(self._cover_letter_content)

        # Checkpoint reached: template populated
        self._template_populated = True

    def generate_word_doc(self, file_destination: string = "./"):
        if not self._template_populated:
            raise Exception("Template has not been created yet.")

        document = Document()
        document.add_paragraph(self._cover_letter_content)
        document.save(os.path.join(file_destination, "Cover_Letter_Nathan_Williams.docx"))

    def generate_text_doc(self, file_destination: string = "./"):
        if not self._template_populated:
            raise Exception("Template has not been created yet.")
        shutil.copy(self._cover_letter, os.path.join(file_destination, "Cover_Letter_Nathan_Williams.docx"))

    @staticmethod
    def clean_up():
        # clean up temp files and any other artifacts
        for file in os.listdir(CoverLetter.template_destination):
            os.remove(os.path.join(CoverLetter.template_destination, file))
