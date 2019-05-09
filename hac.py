from selenium import webdriver
import config
import os
from EmailAlert import EmailAlert
import img2pdf
from datetime import date
from PIL import Image


class HAC(object):
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('disable-infobars')
        # self.options.add_argument('--kiosk-printing')
        # self.options.add_argument('--headless')
        self.options.add_experimental_option("prefs", config.chrome_profile)
        self.driver = webdriver.Chrome('../chromedriver', options=self.options)
        self.driver.maximize_window()
        self.driver.get(config.login_info.get('url'))
        self.driver.implicitly_wait(15)
        Image.init()

    def getGrades(self):
        username = self.driver.find_element_by_xpath(
            '//*[@id="LogOnDetails_UserName"]')
        password = self.driver.find_element_by_xpath(
            '//*[@id="LogOnDetails_Password"]')
        login_button = self.driver.find_element_by_xpath(
            '//*[@id="SignInSectionContainer"]/div[2]/button')
        username.send_keys(config.login_info.get('username'))
        password.send_keys(config.login_info.get('password'))
        login_button.click()
        # Classes Header
        classes = self.driver.find_element_by_xpath('//*[@id="hac-Classes"]')
        classes.click()
        # Swtich to the encompassing iframe
        frame = self.driver.find_element_by_xpath(
            '//*[@id="sg-legacy-iframe"]')
        self.driver.switch_to.frame(frame)
        # # click dropdown for runs to make the elements in the dropdown visible
        # dropdown_btn = self.driver.find_element_by_xpath(
        #     '//*[@id="combobox_plnMain_ddlReportCardRuns"]/a')
        # dropdown_btn.click()

        # # Gets a list of elements with class as 'ui-menu-item'. Since we want
        # # fourth quarter, it corresponds to index 3.
        # all_runs = self.driver.find_elements_by_xpath(
        #     '//*[@class="ui-menu-item"]/a')
        # for index, runs in enumerate(all_runs):
        #     print(index, runs.text)
        # fourth_quarter = all_runs[0]
        # fourth_quarter.click()

        # refresh_view = self.driver.find_element_by_xpath(
        #     '//*[@id="plnMain_btnRefreshView"]')
        # refresh_view.click()

        ### Continue button if need to select quarter 4
        # continue_btn = self.driver.find_element_by_xpath(
        #     '//*[@id="plnMain_btnContinue"]')
        # continue_btn.click()

        full_view = self.driver.find_element_by_xpath('//*[@id="btnView"]')
        full_view.click()

        # Loop through all the assignments and take screenshots
        assignments = self.driver.find_elements_by_class_name('AssignmentClass')
        file_names = []
        for index, assignment in enumerate(assignments):
            name = assignment.find_element_by_class_name(
                'sg-header-heading').text
            #The math class has '/' which causes an error in saving the image
            name = name.replace('/','_')

            #If physical science, then zoom out
            if 'Physical Science' in name:
                self.driver.execute_script("document.body.style.zoom='94%'")
            else:
                self.driver.execute_script("document.body.style.zoom='100%'")
            file_names.insert(index, name)
            file_names[index] += '.png'
            assignment.screenshot(file_names[index])

        # Combine the grade pngs in a single pdf
        pdf_name = 'grades_%s.pdf' % str(date.today())
        # with open(pdf_name, 'wb') as grades:
        #     grades.write(img2pdf.convert(file_names))
        # self.convert_img_to_pdf(pdf_name)
        image_list = [self.open_image(img) for img in file_names]
        image_list[1].save(pdf_name, "PDF", resolution=100.0, save_all=True,
                           append_images=image_list)




        self.driver.switch_to.default_content()
        # self.driver.quit()

    def open_image(self, img_to_open):
        img = Image.open(img_to_open)
        if (img.mode == "RGBA"):
            rgb = Image.new('RGB', img.size, (255, 255, 255))
            rgb.paste(img, mask=img.split()[3])
            return rgb
        else:
            return Image.open(img_to_open)

    def path_of_grades(self):
        download_dir = '.'
        for file in os.listdir(download_dir):
            if "grades" in file:
                return os.path.join(download_dir, file)

    def send_grades(self):
        # receiver = input("Who do you want to email to?\n")
        # receiver = receiver.strip()
        # subject = input("What is the subject?\n")
        # message = input("What is the message\n")
        subject = "HAC Grades"
        message = "Gungun"
        email_sender = EmailAlert("netraamin13@gmail.com", subject, message)
        return email_sender.send_email(self.path_of_grades())

    def delete_file(self):
        [os.remove(file) for file in os.listdir(".") if file.endswith('.png') or file.endswith('.pdf')]


if __name__ == '__main__':
    hac = HAC()
    hac.getGrades()
    success = hac.send_grades()
    hac.delete_file() if success else None
