# ---------------------------------------
#	Import Libraries
# ---------------------------------------
import os
import codecs
import json
import time

# ---------------------------------------
#	[Required]	Script Information
# ---------------------------------------
ScriptName = "Money Transfer Script"
Website = "https://github.com/kemtalis/TransferCurrencyScript"
Creator = "Kemtalis"
Version = "1.0.1"
Description = "Allows users to transfer currency"

# ---------------------------------------
#	Set Variables
# ---------------------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "MTSSettings.json")


# ---------------------------------------
# Classes
# ---------------------------------------
class Settings(object):
    #Load in saved settings file if available or else set default values.

    def __init__(self, settingsfile=None):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        except:
            self.desired_command = "!give"
            self.currency_name = "points"
            self.minimum_permissions = "everyone"
            self.successful_transfer_message = "{0} has successfully transfered {1} {2} to {3}"
            self.not_enough_funds_message = "Sorry {0}, you do not have enough {1}"
            self.invalid_amount_message = "Sorry {0}, {1} is not a valid amount"
            self.no_target_message = "Sorry {0}, but you didn't say who to send the {1} to!"
            self.invalid_target_message = "Sorry {0}, but {1} doesn't exist."

    def reload(self, jsondata):
        #Reload settings from Chatbot user interface by given json data.
        self.__dict__ = json.loads(jsondata, encoding="utf-8")
        return

    def save(self, settingsfile):
        #Save settings contained within to .json and .js settings files.
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            Parent.Log(ScriptName, "Failed to save settings to file.")
        return


# ---------------------------------------
#	Functions
# ---------------------------------------
def transfermoney(user, target, cname, amount):
    if target in Parent.GetViewerList():

        if amount.isalpha() or amount == "":
            Parent.SendTwitchMessage(str(ScriptSettings.invalid_amount_message).format(user, amount))
        elif int(amount) <= Parent.GetPoints(user):
            Parent.RemovePoints(user, int(amount))
            Parent.AddPoints(target, int(amount))
            Parent.SendTwitchMessage(str(ScriptSettings.successful_transfer_message).format(user, amount, cname, target))
        else:
            if amount.isdigit():
                Parent.SendTwitchMessage(str(ScriptSettings.not_enough_funds_message).format(user, cname))
    else:
        if target == "":
            Parent.SendTwitchMessage(str(ScriptSettings.no_target_message).format(user, cname))
        else:
            Parent.SendTwitchMessage("Sorry " + user + ", but " + target + " doesn't exist.")

# ---------------------------------------
#	[Required] Intialize Data
# ---------------------------------------
def Init():
    #Initialize

    # Globals
    global ScriptSettings
    global LastRunTime

    # Load in saved settings
    ScriptSettings = Settings(SettingsFile)
    # Set LastRunTime to now
    LastRunTime = time.time()

    # End of Init
    return


# ---------------------------------------
# Reload Settings on Save
# ---------------------------------------
def ReloadSettings(jsondata):
    #Reloads settings

    # Globals
    global ScriptSettings

    # Reload newly saved settings
    ScriptSettings.reload(jsondata)

    # End of ReloadSettings
    return


# ---------------------------------------
#	[Required] Execute Data / Process Messages
# ---------------------------------------
def Execute(data):
    #Check for command execution

    if data.IsChatMessage():
        if data.GetParam(0).lower() == ScriptSettings.desired_command:
            transfermoney(data.User, data.GetParam(1), ScriptSettings.currency_name, data.GetParam(2))
    return


# ---------------------------------------
#	[Required] Tick Function
# ---------------------------------------
def Tick():
    return