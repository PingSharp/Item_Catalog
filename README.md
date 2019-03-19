# Item_Catalog
## Getting Started

### for Mac or Linux 
regular terminal program on your computer
### for Windows
you need to use Git Bash terminal for this Project,if you don't have ,[click here to install](https://git-scm.com/downloads)
### next steps for all
1. install VirtualBox ,[You can download it from here.](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.
2. download Vagrant from [here](https://www.vagrantup.com/downloads.html). Install the version for your operating system.
3. download this Item_Catalog project as zip file from github or use git clone. Inside this project is the VM configuration. In case you download it as zip file, Unzip the file. This will give you a directory called Item_Catalog. Also if you git cloned it. 
4. Open a terminal or git bash. Under the Item_Catalog directory find the vagrant directory and change to this location. After run the command
```
vagrant up
```
This will cause Vagrant to download a Linux operating system image and install it. This may take quite a while.when vagrant up is finished running,you can run 
```
vagrant ssh
```
to log in to your newly installed linux VM.

5. To execute the Item_Catalog application first we need to fill the data into the local database, so first
```
cd /vagrant/catalog
```
to change into the vagrant directory and use the command 
```
python database_setup.py
```
this will create a empty menuitems.db file ,then run the command to fill data to the data base 
```
python alotofdatas.py
```
the 2 commands above will create a new database , tables and fill them with data.

6. For use of  the authentication and authorization of this application you have to obtain OAuth 2.0 credentials from the Google API Console. Visit the Google API Console to obtain OAuth 2.0 credentials such as a client ID and client secret that are known to both Google and your application. 
7. After you got the the client ID and the Client secret,you have to copy paste the client ID to home.html under templates directory file replace YourclientID with your client ID (line 4), replace the APPLICATION_NAME in application file with YourApplicationName. Download the client secret JSON file and rename it to client_secret and move this JSON file to catalog directory.

8. run the python programm with this command
```
 python application.py
```
this will start a server on your virtual machine ,you can access it with your broswer (on your normal physical machine).Access and test your application by visiting http://localhost:8000 locally
