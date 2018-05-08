import web
import subprocess
import checkacpower


#Site Setup
urls = (
  '/trigger', 'trigger','/aircon', 'aircon', "/killapp", "killapp"
)
app = web.application(urls, globals())
render = web.template.render('templates/')

#IR Setup
def irsend(button):
    subprocess.call("irsend SEND_ONCE aircon %s" % button, shell=True)
    return None

#Webpages

class trigger(object):
    def GET(self):
        form = web.input(scriptname=None)
        if form.scriptname:
            scriptname = str(form.scriptname)
            subprocess.call("scripts/%s.sh" % form.scriptname) 
            return render.trigger(scriptname = scriptname)
        else:
            return render.trigger(scriptname = None)

class aircon(object):
    def GET(self):
        form = web.input(power=None,mode=None,fan=None,temp=None,abstemp=None)
        varcount = 1
        power = form.power
        if form.power:
            varcount = None
            if form.power == "toggle":
                irsend("KEY_POWER")
            elif form.power == "on":
                if checkacpower.getpowerstatus() == 0:
                    irsend("KEY_POWER")
                else:
                    power = power + " (AC unit was already on. No IR trigger sent.)"
            elif form.power == "off":
                if checkacpower.getpowerstatus() == 1:
                    irsend("KEY_POWER")
                else:
                    power = power + " (AC unit was already off. No IR trigger sent.)"
            elif form.power == "status":
                powerstatus = checkacpower.getpowerstatus()
                if powerstatus == 1:
                    powerstatus = "ON"
                elif powerstatus == 0:
                    powerstatus = "OFF"
                else:
                    powerstatus = "Error Reading Power Status"
                power = "The Air Conditioner is Currently %s" % powerstatus
            else:
                power = 'INVALID VARIABLE GIVEN (%s).  Please use: "toggle", "on", "off", "status."' % power
        if form.mode:
            varcount = None
            mode = int(form.mode)
            for _ in range(mode):
                irsend("KEY_MODE")
        if form.fan:
            varcount = None
            fan = int(form.fan)
            for _ in range(fan):
                irsend("KEY_F")
        if form.temp:
            varcount = None
            temp = int(form.temp)
            if temp < 0:
                for _ in range(abs(temp) + 1):
                    irsend("KEY_DOWN")
            if temp > 0:
                for _ in range(temp + 1):
                    irsend("KEY_UP")
        if form.abstemp:
            varcount = None
            for _ in range(16):
                irsend("KEY_DOWN")
            for _ in range(int(form.abstemp) - 64):
                irsend("KEY_UP")                
        return render.aircon(power=power,mode=form.mode,fan=form.fan,temp=form.temp,abstemp=form.abstemp,error=varcount)

class killapp(object):
    def GET(self):
        raise SystemExit
        return "If you are seeing this the Kill Trigger did not work!  Try manually killing the python proccess from SSH."


if __name__ == "__main__":
    app.run()




#Negitive accepting fan and mode code (Does Not work)
'''
            if mode < 0:
                #print mode
                negmode = abs(mode) + 1
                #print negmode
                for _ in range(negmode):
                    subprocess.call("irsend Send_Once aircon KEY_MODE", shell=True)
            if mode > 0:
                for _ in range(mode):
                    subprocess.call("irsend Send_Once aircon KEY_MODE", shell=True)
        if form.fan:
            fan = int(form.fan)
            if fan < 0:
                #print fan
                negfan = abs(fan) + 2
                #print negfan
                for _ in range(negfan):
                    subprocess.call("irsend Send_Once aircon KEY_F", shell=True)
            if fan > 0:
                for _ in range(fan):
                    subprocess.call("irsend Send_Once aircon KEY_F", shell=True)
        return render.aircon()
'''
