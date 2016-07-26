# Imports of various kinds
from Tkinter import *
import urllib2
import xml.etree.ElementTree as ET
import time as ostime

def Set_Agent():
# Sets user agent, grabbing from first text field
    global UAgent
    UAgent = UserEntry.get()
    print UAgent
# Setting my headers. Don't wanna be an illegal, yes~?
    global headers
    headers = {'User-Agent' : 'Update Monitor thing. Currently in use by' + UAgent + '. Devved by Panzer Vier> valkynora@gmail.com'}

def Check():
    global Nation
    global CurInfluence
    global UAgent
    global headers
    global Updated
    Nat = NatEntry.get().replace(' ', '_')
# Check if User Agent exists. If so, get rid of the setting prompt, if present.
    try:
        ThrowawayVar = UAgent
        print ThrowawayVar
        YouDidABad['text'] = ""
# Try to pull a request, to make sure the nation name is valid. If it works, all is well. If not, display NaN
        try:
# Quickly pausing for 1s, so I don't call too much API too quickly. More of a preventative measure, but oh wells.
            ostime.sleep(1)
            req = urllib2.Request("http://www.nationstates.net/cgi-bin/api.cgi?nation=" + Nat + "&q=influence", None, headers)
            html = urllib2.urlopen(req).read()
            print html
            trunk = ET.fromstring(html)
            for EVENT in trunk.iter('INFLUENCE'):
                CurInfluence = EVENT.text
            print CurInfluence
            Nation = Nat
            Updated = False
# Another sleep, 'cause I don't want an immediate jump from the one API call to the other. Just to be 100% safe.
            ostime.sleep(1)
            time.after(50, tick)
        except:
            print "Not a Nation"
            YouDidABad['text'] = 'Not a Nation!'
# Set your agent, or the Modfolk will eat you. For reals. I've seen it happen once!
# ...It was gruesome.
    except:
        YouDidABad['text'] = 'Enter User Agent'
def tick():
# Updating cycle. Pull the current influence level from API, match it to the influence initially drawn.
    global Updated
    if Updated == False:
        global CurInfluence
#1s is still within rate limits. Pls don't spank me, Violet D:
        ostime.sleep(1)
        req = urllib2.Request("http://www.nationstates.net/cgi-bin/api.cgi?nation=" + Nation + "&q=influence", None, headers)
        html = urllib2.urlopen(req).read()
        trunk = ET.fromstring(html)
        for EVENT in trunk.iter('INFLUENCE'):
            UpdInfluence = EVENT.text
# If they don't match, congratulations, it's a baby gi- update. Yes. That's what I meant.
        if UpdInfluence != CurInfluence:
            print 'Updated!'
            time['text'] = 'GO!'
            Updated = True
# In case of a match, display the same ol' waiting message. Gotta check if I can get some elevator music in here...
        else:
            print 'Waiting...'
            time['text'] = 'Waiting...'
        time.after(50, tick)

# Now for the actual window loop!
root = Tk()
# Initialising all them GUI elements. First the User Entry line...
Label(root, text="Username:").grid(row=0, column=0)

UserEntry = Entry(root, width=40)
UserEntry.grid(row=0, column=1)
# When pressed, calling back to set the User Agent!
Button(root, text='Okay', command=Set_Agent).grid(row=0, column=2, sticky=W, pady=4)

# Aaand Target entry
Label(root, text="Target Nation:").grid(row=2, column= 0)

NatEntry = Entry(root, width=40)
NatEntry.grid(row=2, column=1)
# Again, button does stuff. This time checking for validity and starting up my timers!
Button(root, text='Set', command=Check).grid(row=2, column=2, pady=4)
time = Label(root, text="")
time.grid(row=3, column=0)
YouDidABad = Label(root, text="")
YouDidABad.grid(row=4, column=1)

root.mainloop()