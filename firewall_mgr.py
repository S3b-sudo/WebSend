import os

os.system("clear")
print("WebSend Firewall Survace:")
print("=========================")
print("Pick your Firewall Provider: ")
print("1. Firewalled (Default on Fedora)")
print("2. UFW (Default on Ubuntu)")
print("3. Other")
print("=========================")

while True:
    choice1 = input("Pick a nomber:")

    if choice1 == "1":
        while True:
            print("What would you like to do?")
            print("1. Add firewall rule to allowe port 8501/tcp")
            print("2. Remove firewall rule to allow port 8501/tcp")

            choice2 = input("Pick a Nomber: ")

            if choice2 == "1":
                os.system("sudo firewall-cmd --permanent --add-port=8501/tcp")
                os.system("sudo firewall-cmd --reload")
                print("=====================================================")
                input("Executed opporation. Press 'Return' to quit.")
                quit()
            
            if choice2 == "2":
                os.system("sudo firewall-cmd --permanent --remove-port=8501/tcp")
                os.system("sudo firewall-cmd --reload")
                print("=====================================================")
                input("Executed opporation. Press 'Return' to quit.")
                quit()

    if choice1 == "2":
        while True:
            print("What would you like to do?")
            print("1. Add firewall rule to allowe port 8501/tcp")
            print("2. Remove firewall rule to allow port 8501/tcp")

            choice2 = input("Pick a nomber: ")

            if choice2 == "1":
                os.system("sudo ufw allow 8501")
                print("=====================================================")
                input("Executed opporation. Press 'Return' to quit.")
                quit()
            
            if choice2 == "2":
                os.system("sudo ufw deny 8501")
                print("=====================================================")
                input("Executed opporation. Press 'Return' to quit.")
                quit()

    
    if choice1 == "3":
        print("I Dont know: You need to find out what firewall survace you are using.")           
        print(" ")
        print("My firewall provider is not listed: Find a way to allow port 8501/tcp through your firewall.")
        print(" ")
        input("Press 'Return' to quit: ")
        quit()