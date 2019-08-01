# HomeAccessCenter
A python script which goes to HomeAccessCenter website, takes screenshots of grades, and emails them to the user.
The script uses the selenium chrome driver to automatically open an instance of chrome, load the HomeAccessCenter website, enter the username and password, and get the grades. 

To use the program, run hac.py. Before doing so, make sure to set the username and password for HAC in the config.py file. Additionally, in EmailAlert.py, the sender's username and password need to be entered as well. To ensure security, it is best to save such information in environment variables.
