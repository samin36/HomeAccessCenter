#!/usr/bin/env python3
from selenium import webdriver
import config
import os
import sys
from EmailAlert import EmailAlert
import img2pdf
from datetime import date
from PIL import Image


class HAC():
    def __init__(self):
        """
        initalizes the webdriver
        """
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--start-fullscreen')
        self.options.add_argument('disable-infobars')
        self.options.add_argument('--window-size=2560,1440')
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(config.login_info.get('url'))
        self.driver.implicitly_wait(15)
        Image.init()

    def get_grades(self):
        """
        function which gets the grades using selenium driver
        """
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

        full_view = self.driver.find_element_by_xpath('//*[@id="btnView"]')
        full_view.click()

        # Loop through all the assignments and take screenshots
        assignments = self.driver.find_elements_by_class_name(
            'AssignmentClass')
        file_names = []
        for index, assignment in enumerate(assignments):
            name = assignment.find_element_by_class_name(
                'sg-header-heading').text
            # The math class has '/' which causes an error in saving the image
            name = name.replace('/', '_')

            # If physical science, then zoom out
            if 'Physical Science' in name:
                self.driver.execute_script("document.body.style.zoom='98%'")
            else:
                self.driver.execute_script("document.body.style.zoom='100%'")

            file_names.insert(index, name)
            file_names[index] += '.png'
            assignment.screenshot(file_names[index])

        # Combine the grade pngs in a single pdf
        pdf_name = 'grades_%s.pdf' % str(date.today())
        image_list = [self.open_image(img) for img in file_names]
        image_list[1].save(pdf_name, "PDF", resolution=100.0, save_all=True,
                           append_images=image_list)

        self.driver.switch_to.default_content()
        self.driver.quit()

    def open_image(self, img_to_open):
        img = Image.open(img_to_open)
        if (img.mode == "RGBA"):
            # Since the PIL Image library only accepts RBG images, must make a
            # blank image and copy over the old image to the new one with RGB
            # mode
            rgb = Image.new('RGB', img.size, (255, 255, 255))
            rgb.paste(img, mask=img.split()[3])
            return rgb
        else:
            return Image.open(img_to_open)

    def path_of_grades_pdf(self):
        """
        function to return the path of the grades pdf file
        """
        download_dir = '.'
        for file in os.listdir(download_dir):
            if "grades" in file:
                return os.path.join(download_dir, file)

    def list_of_images_png(self):
        """
        function to return a list of the names of the pngs
        """
        download_dir = '.'
        return [file for file in os.listdir(download_dir) if ".png" in file]

    def send_grades(self):
        """
        function which handles sending the grades. it uses the EmailAlert.py
        file
        """
        receiver = input("Who do you want to email to?\n")
        receiver = receiver.strip()
        subject = "HAC Grades"
        message = f"HAC Grades for {str(date.today())}"
        email_sender = EmailAlert(receiver, subject, message)
        # send_what = input("PDF or PNGS?\n")
        send_what = "PDF"
        if "PDF" in send_what:
            return email_sender.send_email(self.path_of_grades_pdf())
        elif "PNGS" in send_what:
            return email_sender.send_email(self.list_of_images_png())

    def delete_file(self):
        """
        function which deletes the screenshot images and grades pdf after email
        is sent
        """
        [os.remove(file) for file in os.listdir(".")
         if file.endswith('.png') or file.endswith('.pdf')]


if __name__ == '__main__':
    hac = HAC()
    hac.get_grades()
    success = hac.send_grades()
    hac.delete_file() if success else None
