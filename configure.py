import pickle
import os
import getpass
import rwuserdata

def makeConfig():
    key = input("Please input a Key to Encrypt your Infos with (Remember it) - ")
    configAccepted = False
    while not configAccepted:
        os.system("cls")
        config = {}
        email_sms = input("Please input SMS Email - ")
        pwd_sms = getpass.getpass("Please input SMS Password - ")
        config["SMS"] = {
            "usr":email_sms,
            "pwd":pwd_sms
        }

        useGoogleCal = getYN("Use Google Calendar? (Y/N) - ")
        if useGoogleCal:
            email_google = input("Please input Google Mail - ")
            pwd_google = getpass.getpass("Please input Google Password - ")
        config["GOOGLE"] = {
            "usr":email_google if useGoogleCal == True else "-",
            "pwd":pwd_google if useGoogleCal == True else "-"
        }

        useOutlookCal = getYN("Use Outlook Calendar? (Y/N) - ")
        if useOutlookCal:
            email_outlook = input("Please input Outlook Mail - ")
            pwd_outlook = getpass.getpass("Please input Outlook Password - ")
        config["OUTLOOK"] = {
            "usr":email_outlook if useOutlookCal == True else "-",
            "pwd":pwd_outlook if useOutlookCal == True else "-"
        }
        os.system("cls")
        print("SMS Email :", config["SMS"]["usr"])
        print("SMS Password :", config["SMS"]["pwd"])
        print("GOOGLE Email :", config["GOOGLE"]["usr"])
        print("GOOGLE Password :", config["GOOGLE"]["pwd"])
        print("OUTLOOK Email :", config["OUTLOOK"]["usr"])
        print("OUTLOOK Password :", config["OUTLOOK"]["pwd"])
        configAccepted = getYN("Do you wish continue with the Options selected above? (Y/N) - ")
    rwuserdata.encryptObj(key.encode(), config, "config.aes")
    return config

# Returns True if the Answer is 'Y' or 'y' and False if the Answer is 'N' or 'n'
def getYN(prompt):
    noAnswer = True
    while noAnswer:
        try:
            inp = input(prompt)
            answer = True if inp == "Y" or inp == "y" else False if inp=="N" or inp=="n" else Exception("Answer is not Valid")
            if str(answer) != "True" and str(answer) != "False":
                raise answer
            noAnswer = False
        except:
            print("Option", inp, "is not an option.")
    return answer

def loadconfiguration(key):
    if os.path.exists("config.aes"):
        config = rwuserdata.decryptObj(key, "config.aes")
    else:
        config = makeConfig()
    return config
