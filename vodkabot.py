# -*- coding: utf-8 -*-

from LineAlpha import LineClient

from LineAlpha.LineApi import LineTracer

from LineAlpha.LineThrift.ttypes import Message

from LineAlpha.LineThrift.TalkService import Client

import time, datetime, random ,sys, re, string, os, json

reload(sys)

sys.setdefaultencoding('utf-8')

client = LineClient()

client._qrLogin("line://au/q/")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)

offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

wait = {

'readPoint':{},

'readMember':{},

'setTime':{},

'ROM':{}

}

setTime = {}

setTime = wait["setTime"]

def sendMessage(to, text, contentMetadata={}, contentType=0):

mes = Message()

mes.to, mes.from_ = to, profile.mid

mes.text = text

mes.contentType, mes.contentMetadata = contentType, contentMetadata

if to not in messageReq:

messageReq[to] = -1

messageReq[to] += 1

client._client.sendMessage(messageReq[to], mes)

def NOTIFIED_ADD_CONTACT(op):

try:

sendMessage(op.param1, client.getContact(op.param1).displayName + "安安(*´･ω･*)")

except Exception as e:

print e

print ("\n\nFriendAdd\n\n")

return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):

#print op

try:

sendMessage(op.param1, client.getContact(op.param2).displayName + "歡迎加入" + group.name)

except Exception as e:

print e

print ("\n\nGroupEnter\n\n")

return

tracer.addOpInterrupt(17,NOTIFIED_ACCEPT_GROUP_INVITATION)

def NOTIFIED_KICKOUT_FROM_GROUP(op):

try:

sendMessage(op.param1, client.getContact(op.param3).displayName + " 被踢了\n可憐(*´･ω･*)")

except Exception as e:

print e

print ("\n\nGroupKick\n\n")

return

tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def NOTIFIED_LEAVE_GROUP(op):

try:

sendMessage(op.param1, client.getContact(op.param2).displayName + " 離開了\n可憐(*´･ω･*)")

except Exception as e:

print e

print ("\n\nGroupLeave\n\n")

return

tracer.addOpInterrupt(15,NOTIFIED_LEAVE_GROUP)

def NOTIFIED_READ_MESSAGE(op):

#print op

try:

if op.param1 in wait['readPoint']:

Name = client.getContact(op.param2).displayName

if Name in wait['readMember'][op.param1]:

pass

else:

wait['readMember'][op.param1] += "\n・" + Name

wait['ROM'][op.param1][op.param2] = "・" + Name

else:

pass

except:

pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def RECEIVE_MESSAGE(op):

msg = op.message

try:

if msg.contentType == 0:

try:

if msg.to in wait['readPoint']:

if msg.from_ in wait["ROM"][msg.to]:

del wait["ROM"][msg.to][msg.from_]

else:

pass

except:

pass

else:

pass

except KeyboardInterrupt:

	 sys.exit(0)

except Exception as error:

print error

print ("\n\nMessageReceive\n\n")

return

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def SEND_MESSAGE(op):

msg = op.message

try:

if msg.toType == 0:

if msg.contentType == 0:

if msg.text == "我的友資":

sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)

if msg.text == "禮物":

sendMessage(msg.to, text="gift sent", contentMetadata={'PRDID': '3cc08ba6-5d04-4c52-ab76-651231ead8ef','PRDTYPE': 'THEME','MSGTPL': '6'}, contentType=9)

if msg.text == "時間":

sendMessage(msg.to, "現在時間:" + datetime.datetime.today().strftime('%Y年%m月%d日 %H點%M分%S秒'))

else:

pass

else:

pass

if msg.toType == 2:

if msg.contentType == 0:

if msg.text == "我的密碼":

sendMessage(msg.to, msg.from_)

if msg.text == "群組密碼":

sendMessage(msg.to, msg.to)

if msg.text == "群組資訊":

group = client.getGroup(msg.to)

md = "查詢完成(*´･ω･*)\n[群組名稱]\n" + group.name + "\n[群組密碼]\n" + group.id + "\n[群組封面]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus

if group.preventJoinByTicket is False: md += "\n群組網址:開放中\n"

else: md += "\n群組網址:關閉中\n"

if group.invitee is None: md += "已加入:" + str(len(group.members)) + "人\n邀請中:0人"

else: md += "已加入:" + str(len(group.members)) + "人\n邀請中:" + str(len(group.invitee)) + "人"

sendMessage(msg.to,md)

if "群組名稱:" in msg.text:

key = msg.text[22:]

group = client.getGroup(msg.to)

group.name = key

client.updateGroup(group)

sendMessage(msg.to,"群組名稱已經變更為:"+key+"(*´･ω･*)")

if msg.text == "群組網址":

sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))

if msg.text == "開放網址":

group = client.getGroup(msg.to)

if group.preventJoinByTicket == False:

sendMessage(msg.to, "開放中喔(*´･ω･*)")

else:

group.preventJoinByTicket = False

client.updateGroup(group)

sendMessage(msg.to, "開放成功(*´･ω･*)")

if msg.text == "關閉網址":

group = client.getGroup(msg.to)

if group.preventJoinByTicket == True:

sendMessage(msg.to, "關閉中喔(*´･ω･*)")

else:

group.preventJoinByTicket = True

client.updateGroup(group)

sendMessage(msg.to, "關閉成功(*´･ω･*)")

if msg.text == "取消所有邀請":

group = client.getGroup(msg.to)

if group.invitee is None:

sendMessage(op.message.to, "咦? 沒有人被邀請喔(*´･ω･*)")

else:

gInviMids = [contact.mid for contact in group.invitee]

client.cancelGroupInvitation(msg.to, gInviMids)

sendMessage(msg.to, str(len(group.invitee)) + "取消了所有邀請(*´･ω･*)")

if "邀請:" in msg.text:

key = msg.text[-33:]

client.findAndAddContactsByMid(key)

client.inviteIntoGroup(msg.to, [key])

contact = client.getContact(key)

sendMessage(msg.to, "邀請了"+contact.displayName+"(*´･ω･*)")

if msg.text == "我的友資":

M = Message()

M.to = msg.to

M.contentType = 13

M.contentMetadata = {'mid': msg.from_}

client.sendMessage(M)

if "發送友資:" in msg.text:

key = msg.text[-33:]

sendMessage(msg.to, text=None, contentMetadata={'mid': key}, contentType=13)

contact = client.getContact(key)

sendMessage(msg.to, ""+contact.displayName+"的友資發送成功(*´･ω･*)")

if msg.text == "時間":

sendMessage(msg.to, "現在時間:" + datetime.datetime.today().strftime('%Y年%m月%d日 %H點%M分%S秒'))

if msg.text == "禮物":

sendMessage(msg.to, text="gift sent", contentMetadata={'PRDID': '3cc08ba6-5d04-4c52-ab76-651231ead8ef','PRDTYPE': 'THEME','MSGTPL': '6'}, contentType=9)

if msg.text == "開始抓已讀":

sendMessage(msg.to, "狩獵開始")

try:

del wait['readPoint'][msg.to]

del wait['readMember'][msg.to]

except:

pass

wait['readPoint'][msg.to] = msg.id

wait['readMember'][msg.to] = ""

wait['setTime'][msg.to] = datetime.datetime.today().strftime('%Y年%m月%d日 %H點%M分%S秒')

wait['ROM'][msg.to] = {}

print wait

if msg.text == "抓已讀":

if msg.to in wait['readPoint']:

if wait["ROM"][msg.to].items() == []:

chiya = ""

else:

chiya = ""

for rom in wait["ROM"][msg.to].items():

print rom

chiya += rom[1] + "\n"

sendMessage(msg.to, "抓到了(*´･ω･*)\n已讀過的人: %s\n\n已讀不回的傢伙們:\n%s\n狩獵開始的時間:[%s]" % (wait['readMember'][msg.to],chiya,setTime[msg.to]))

else:

sendMessage(msg.to, "還沒開始抓已讀(*´･ω･*)")

else:

pass

else:

pass

except Exception as e:

print e

print ("\n\nMessageSand\n\n")

return

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:

tracer.execute()

