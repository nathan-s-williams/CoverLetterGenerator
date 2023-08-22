from cover_letter import CoverLetter

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cover_letter = CoverLetter("web")
    try:
        cover_letter.set_date("August 21, 2023")
        cover_letter.set_job_role("Software Engineer")
        cover_letter.set_company("abc company")
        cover_letter.insert_data()
        cover_letter.generate_word_doc()
        # cover_letter.clean_up()
    except Exception as e:
        print(e)

