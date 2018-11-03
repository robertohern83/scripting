How to configure selenium-server as a service on linux - RedHat: 

Copy selenium-server.jar to /opt/selenium/
Create a new user with selenium as it's id
Copy selenium file to /etc/init.d/
Register selenium at boottime: 
	sudo ln -s opt/selenium/selenium.sh /usr/bin/selenium
	sudo chmod 755 /etc/init.d/selenium
	sudo chkconfig --add selenium
