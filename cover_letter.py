import shutil
from datetime import datetime


class CoverLetter:
    #  Cover Letter templates.
    web_template_source = "cover_letter_templates/cover_letter_template_web.txt"
    template_destination = "cover_letter_output"

    def __init__(self, version):
        # Attributes
        self._version = version
        self._date = ""
        self._cover_letter = ""
        self._company = ""
        self._role = ""

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
            self._cover_letter = CoverLetter.template_destination + "/" + str(datetime.now())
            shutil.copy(CoverLetter.web_template_source, self._cover_letter)

    def insert_data(self):
        pass

    def generate_word_doc(self):
        pass

    def clean_up(self):
        pass
