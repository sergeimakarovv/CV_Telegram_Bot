import os
import subprocess
from bs4 import BeautifulSoup
from typing import List


HtmlStr  = str




class UserProfilePDFHandler:
    def __init__(self, usersall: dict):
        self.usersall = usersall

    from bs4 import BeautifulSoup

    def add_html_element(self, data_list) -> HtmlStr:
        try:
            pdf_folder = 'module'
            os.makedirs(pdf_folder, exist_ok=True)
            filename = os.path.join(pdf_folder, "without_custom.html")
            with open(filename) as tmp_file:
                main_html = tmp_file.read()
            soup = BeautifulSoup(main_html, 'html.parser')
            insert_to_div = {
                "header": soup.find(class_="header-info"),
                "about_me": soup.find(class_="about-me"),
                "expt": soup.find(class_="experience-box"),
                "edu": soup.find(class_="content-box-edu"),
                "skill_hr": soup.find(class_="group-of-skills-hr"),
            }
            for class_name, add_html in zip(insert_to_div.keys(), data_list):
                content_div = insert_to_div[class_name]
                if content_div:
                    new_content = BeautifulSoup(add_html, 'html.parser')
                    insert_position = len(content_div.contents)
                    content_div.insert(insert_position, new_content)
            return soup.prettify()
        except FileNotFoundError:
            print("The HTML template file was not found.")
        except Exception as e:
            print(f"An error occurred in add_html_element: {e}")

    def format_user_data(self) -> None:
        tmpl_data = {
                "header": """
                            <div class="naming">{0}</div>
                            <div class="sub-header">
                            <div class="main-info">
                            <div class="role-name">{1}</div>
                            <div class="city">{2}</div>
                            </div>
                            <div class="fast-link-section">
                            <div class="link">
                            <a class="fast_link_content" href="{3}" target="_blank">{4}</a>
                            </div>
                            <div class="link"><a>{5}</a></div>
                            """,
                "about_me": """
                            <div class="content">
                            {0}
                            </div>""",
                "exp_tmpl": """
                            <div class="job">
                            <div class="header-section">
                            <div class="mini-header">
                            <div class="mini-header-1">
                            <a class="foreigh_link" id="company_name_1" target="_blank">{0}</a>
                            </div>
                            <div class="mini-header-2" id="position_1">{1}</div>
                            </div>
                            <div class="date" id="date_1">{2}</div>
                            </div>
                            <div class="content" id="content_1">
                            {3}
                            </div>
                            </div>""",
                "edu_tmpl": """
                            <div class="header-section">
                            <div class="mini-header">
                            <div class="mini-header-1">
                            <a class="foreigh_link" id="university_name1" target="_blank">{0}</a>
                            </div>
                            <div class="mini-header-2" id="university_loc1">{1}</div>
                            </div>
                            <div class="date" id="university_date1">{2}</div>
                            </div>""",
                "skills_hr": """<div class="skill">{0}</div>""",
                "skills_sf": """<div class="skill">{0}</div> """
            }
        try:
            _id = list(self.usersall.keys())[0]
            work_data = "".join(
                [
                    tmpl_data["exp_tmpl"].format(
                        self.usersall[_id]["work_exp"][work_exp]["work_name"],
                        self.usersall[_id]["work_exp"][work_exp]["pos_work"],
                        self.usersall[_id]["work_exp"][work_exp]["start_end_work"],
                        self.usersall[_id]["work_exp"][work_exp]["desc_work"],
                    )
                    for work_exp in self.usersall[_id]["work_exp"].keys()
                ]
            )

            edu_data = "".join(
                [
                    tmpl_data["edu_tmpl"].format(
                        self.usersall[_id]["edu_exp"][edu_exp]["educate_name"],
                        self.usersall[_id]["edu_exp"][edu_exp]["educate_place"],
                        self.usersall[_id]["edu_exp"][edu_exp]["start_end_study"],
                    )
                    for edu_exp in self.usersall[_id]["edu_exp"].keys()
                ]
            )

            skills_data = " ".join(
                [tmpl_data["skills_hr"].format(self.usersall[_id]["skills"][skill]) for skill in self.usersall[_id]["skills"].keys()]
            )

            header = tmpl_data["header"].format(self.usersall[_id]["full_name"],
                                       self.usersall[_id]["position"],
                                       self.usersall[_id]["residence"],
                                       self.usersall[_id]["portfolio"],
                                       self.usersall[_id]["portfolio"],
                                       self.usersall[_id]["email"])

            about_me = tmpl_data["about_me"].format(self.usersall[_id]["about_me"])


            final_html = self.add_html_element(data_list = [header, about_me, work_data, edu_data, skills_data])
            pdf_folder = 'module'
            os.makedirs(pdf_folder, exist_ok=True)
            filename = os.path.join(pdf_folder, "tmp_resume_file.html")
            with open(filename, "w") as tmp_file:
                tmp_file.write(final_html)
            # print(final_html)
        except KeyError as e:
            print(f"Key missing in user data: {e}")
            return None
        except Exception as e:
            print(f"An error occurred in format_user_data: {e}")
            return None

    def create_pdf(self) -> None:
        # try:
        user_id = list(self.usersall.keys())[0]
        pdf_folder = 'pdf_files'
        os.makedirs(pdf_folder, exist_ok=True)
        filename = os.path.join(pdf_folder, f"{user_id}.pdf")

        js_folder = 'module'
        os.makedirs(js_folder, exist_ok=True)
        js_route = os.path.join(js_folder, "convertToPDF2.js")

        output = subprocess.check_output(["node", js_route, filename], text=True)

        returned_filename = output.strip()
        print(f"JavaScript returned: {returned_filename}")
        # except subprocess.CalledProcessError as e:
        #     print(f"Failed to create PDF: {e.output}")
        # except Exception as e:
        #     print(f"Unexpected error in create_pdf: {e}")

    def delete_file(self) -> None:
        user_id = list(self.usersall.keys())[0]
        pdf_folder = 'pdf_files'
        os.makedirs(pdf_folder, exist_ok=True)
        file_path = os.path.join(pdf_folder, f"{user_id}.pdf")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"File '{user_id}' in directory '{file_path}' has been deleted.")
            except OSError as e:
                print(f"Error deleting '{user_id}': {e}")
        else:
            print(f"File '{user_id}' in directory '{file_path}' does not exist.")
