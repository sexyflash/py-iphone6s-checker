# Web Server Gateway Interface (WSGI)

from google.appengine.api import users
import webapp2
import json
import logging
from datetime import datetime
import time
import datetime
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from urllib import urlencode
import re
from urllib2 import unquote
from google.appengine.api import mail

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/437.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/437.78.2"
REFERRER_HK_ONLINE = "http://store.apple.com/hk/buy-iphone/iphone6"
REFERRER_HK_LOCAL = "https://reserve.cdn-apple.com/HK/en_HK/reserve/iPhone"

ONLINE_TAG = "Online"

PUBLIC_KEY_HKGOLDEN = "6LewtPoSAAAAAMTE4LeAjBa3JB7jUQRB_X422sIw"
PRIVATE_KEY_HKGOLDEN = "6LewtPoSAAAAAHTgjxbVMSjDk1XxKU4ut_DfWzH3"

PUBLIC_KEY_HKG = "6LedovoSAAAAAKFD_syd1EgMJrwGLC_GqOW8h7XV"
PRIVATE_KEY_HKG = "6LedovoSAAAAAHoFEfNTri-6L_NdPjbJC7zLgq2R"

PUBLIC_KEY_707 = "6LfTovoSAAAAAPAruvpcbAxuJgZ5SVYP9NW1mtgD"
PRIVATE_KEY_707 = "6LfTovoSAAAAAGhU4DkvAe-vNKHgA63RnZ9yhn0o"

# PUBLIC_KEY = PUBLIC_KEY_HKGOLDEN
# PRIVATE_KEY = PRIVATE_KEY_HKGOLDEN

# PUBLIC_KEY = PUBLIC_KEY_HKG
# PRIVATE_KEY = PRIVATE_KEY_HKG

PUBLIC_KEY = PUBLIC_KEY_707
PRIVATE_KEY = PRIVATE_KEY_707

#STORE_JSON_HK = "https://reserve.cdn-apple.com/HK/en_HK/reserve/iPhone/stores.json"
AVAILABILITY_JSON_HK = "https://reserve.cdn-apple.com/HK/en_HK/reserve/iPhone/availability.json"
STORE_JSON_HK = "https://www.dropbox.com/s/3x227l09qo49gwp/stores_hk.json?dl=1"
#AVAILABILITY_JSON_HK = "https://www.dropbox.com/s/1hg8gfc7awrmlbi/AVAILABILITY_HK.json?dl=1"


#STORE_JSON_FR = https://reserve.cdn-apple.com/FR/fr/reserve/iPhone/stores.json
#AVAILABILITY_JSON_FR = "https://reserve.cdn-apple.com/FR/fr/reserve/iPhone/availability.json"
# STORE_JSON_FR = "https://www.dropbox.com/s/e057xohvb15dwve/stores_fr.json?dl=1"
# AVAILABILITY_JSON_FR = "https://www.dropbox.com/s/zzs8xq3g4ilg0rh/availability_fr.json?dl=1"


URLs_HK =  ["http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=4_7inch&option.dimensionColor=silver&option.dimensionCapacity=16gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=4_7inch&option.dimensionColor=silver&option.dimensionCapacity=64gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=4_7inch&option.dimensionColor=silver&option.dimensionCapacity=128gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=4_7inch&option.dimensionColor=gold&option.dimensionCapacity=16gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=4_7inch&option.dimensionColor=gold&option.dimensionCapacity=64gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=4_7inch&option.dimensionColor=gold&option.dimensionCapacity=128gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=4_7inch&option.dimensionColor=space_gray&option.dimensionCapacity=16gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=4_7inch&option.dimensionColor=space_gray&option.dimensionCapacity=64gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=4_7inch&option.dimensionColor=space_gray&option.dimensionCapacity=128gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6P?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=5_5inch&option.dimensionColor=silver&option.dimensionCapacity=16gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6P?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=5_5inch&option.dimensionColor=silver&option.dimensionCapacity=64gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6P?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=5_5inch&option.dimensionColor=silver&option.dimensionCapacity=128gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6P?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=5_5inch&option.dimensionColor=gold&option.dimensionCapacity=16gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6P?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=5_5inch&option.dimensionColor=gold&option.dimensionCapacity=64gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6P?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=5_5inch&option.dimensionColor=gold&option.dimensionCapacity=128gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6P?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=5_5inch&option.dimensionColor=space_gray&option.dimensionCapacity=16gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6P?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=5_5inch&option.dimensionColor=space_gray&option.dimensionCapacity=64gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED",
"http://store.apple.com/hk/buyFlowSelectionSummary/IPHONE6P?node=home/shop_iphone/family/iphone6&step=select&option.dimensionScreensize=5_5inch&option.dimensionColor=space_gray&option.dimensionCapacity=128gb&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED"]


URL_APPLE_STORE = "http://store.apple.com/"
URL_REGION = "hk"
URL_IPHONE6R = "/buyFlowSelectionSummary/IPHONE6?node=home/shop_iphone/family/iphone6&step=select"
URL_IPHONE6P = "/buyFlowSelectionSummary/IPHONE6P?node=home/shop_iphone/family/iphone6&step=select"
URL_SIZE_47 = "&option.dimensionScreensize=4_7inch"
URL_SIZE_55 = "&option.dimensionScreensize=5_5inch"
URL_COLOR_SILVER = "&option.dimensionColor=silver"
URL_COLOR_GOLD = "&option.dimensionColor=gold"
URL_COLOR_SPACE = "&option.dimensionColor=space_gray"
URL_16GB = "&option.dimensionCapacity=16gb"
URL_64GB = "&option.dimensionCapacity=64gb"
URL_128GB = "&option.dimensionCapacity=128gb"
URL_UNLOCKED = "&option.carrierModel=UNLOCKED%2FWW&carrierPolicyType=UNLOCKED"
        #16         64          128
MAPs = ["MG482ZP/A","MG4H2ZP/A","MG4C2ZP/A", # 4.7 Silver
        "MG492ZP/A","MG4J2ZP/A","MG4E2ZP/A", # 4.7 Gold
        "MG472ZP/A","MG4F2ZP/A","MG4A2ZP/A", # 4.7 Space Grey
        "MGA92ZP/A","MGAJ2ZP/A","MGAE2ZP/A", # 5.5 Silver
        "MGAA2ZP/A","MGAK2ZP/A","MGAF2ZP/A", # 5.5 Gold
        "MGA82ZP/A","MGAH2ZP/A","MGAC2ZP/A"] # 5.5 Space Grey

model_map = {}
model_map['MG482ZP/A'] = "Silver 16GB 4.7"
model_map['MG4H2ZP/A'] = "Silver 64GB 4.7"
model_map['MG4C2ZP/A'] = "Silver 128GB 4.7"
model_map['MG492ZP/A'] = "Gold 16GB 4.7"
model_map['MG4J2ZP/A'] = "Gold 64GB 4.7"
model_map['MG4E2ZP/A'] = "Gold 128GB 4.7"
model_map['MG472ZP/A'] = "Space Grey 16GB 4.7"
model_map['MG4F2ZP/A'] = "Space Grey 64GB 4.7"
model_map['MG4A2ZP/A'] = "Space Grey 128GB 4.7"
model_map['MGA92ZP/A'] = "Silver 16GB 5.5"
model_map['MGAJ2ZP/A'] = "Silver 64GB 5.5"
model_map['MGAE2ZP/A'] = "Silver 128GB 5.5"
model_map['MGAA2ZP/A'] = "Gold 16GB 5.5"
model_map['MGAK2ZP/A'] = "Gold 64GB 5.5"
model_map['MGAF2ZP/A'] = "Gold 128GB 5.5"
model_map['MGA82ZP/A'] = "Space Grey 16GB 5.5"
model_map['MGAH2ZP/A'] = "Space Grey 64GB 5.5"
model_map['MGAC2ZP/A'] = "Space Grey 128GB 5.5"



loc_map = {}
loc_map['R409'] = "Causeway Bay iReserve"
loc_map['R428'] = "IFC Mall iReserve"
loc_map['R485'] = "Festival Walk iReserve"
loc_map['Online'] = "store.apple.com/hk"

class MailingList(ndb.Model):
    email = ndb.StringProperty()
    dateTimeCreated = ndb.DateTimeProperty(auto_now_add=True)
    active = ndb.BooleanProperty() # 1 active 0 inactive
    lastSent = ndb.DateTimeProperty(auto_now=True)

    def getAll(self):
        return self.query().fetch()

    def getLastSent(self):
        obj = ndb.Key(MailingList, "3dmouse@gmail.com").get()
        return obj.lastSent

    def writeLastSent(self):
        obj = ndb.Key(MailingList, "3dmouse@gmail.com").get()
        obj.put()


    def store(self, _email):
        if self.isExisting(_email):
            return False
        obj = MailingList(key=ndb.Key(MailingList, _email),
                          email=_email,
                          active=True)
        obj.put()
        return True

    def isExisting(self,_email):
        obj = ndb.Key(MailingList, _email).get()
        if obj is None:
            return False
        if obj.active is False:
            return False
        return True

    def inactive(self,_email, _key):
        obj = ndb.Key(MailingList, _email).get()
        if obj.dateTimeCreated == _key:
            obj.active = False
            obj.put()
            return True
        else:
            return False

    def issue(self):
        return self.dateTimeCreated




# Product (key = partNumber)
class Product(ndb.Model):
    partNumber = ndb.StringProperty()
    productName = ndb.StringProperty() # iPhone 6 Plus
    capacity = ndb.IntegerProperty()
    size = ndb.FloatProperty()
    color = ndb.StringProperty()
    unlocked = ndb.BooleanProperty() # 1 Unlocked, 0 locked
    country = ndb.StringProperty()

    def get(self):
        return self.query().fetch()

    def peek(self,_partNumber):
        return ndb.Key(Product, _partNumber).get()

    def store(self, _partNumber, _productName, _capacity, _color, _unlocked, _country):
        if _productName.find("Plus") > 0:
            _size = 5.5
        else:
            _size = 4.7
        obj = Product(key=ndb.Key(Product,_partNumber),
                      partNumber=_partNumber,
                      productName=_productName,
                      capacity=int(_capacity),
                      size=_size,
                      color=_color,
                      unlocked=_unlocked,
                      country=_country)
        obj.put()


# Location (key = storeId)
class Location(ndb.Model):
    storeId = ndb.StringProperty()
    storeName = ndb.StringProperty()
    isOpen = ndb.BooleanProperty()
    lastOpenDateTime = ndb.DateTimeProperty(auto_now=True)

    def get(self, _storeId):
        return self.query(Location.storeId == _storeId).get()

    def updateOpen(self, _storeId):
        obj = self.get(_storeId)
        obj.isOpen = True
        obj.put()

    def save(self, _storeId, _storeName):
        obj = Location(key=ndb.Key(Location, _storeId))
        obj.storeId = _storeId
        obj.storeName = _storeName
        obj.put()

# Product: iPhone6 Silver 16GB
# location:
# availability: "0" (Not Available) : "1" (Available) : "2" (Error)
# dateTimeUpdated: provided by Apple (may not be available)
# dateTimeCreated: Date and Time at
class Available(ndb.Model):
    partNumber = ndb.StringProperty()
    storeId = ndb.StringProperty()
    availability = ndb.IntegerProperty()
    dateTimeCreated = ndb.DateTimeProperty(auto_now_add=True)

    def get_latest_availability(self,_partNumber, _storeId):
        obj = Available()
        ret = obj.query(Available.partNumber == _partNumber, Available.storeId == _storeId).order(-Available.dateTimeCreated).get()
        if ret is None:
            return [3, None, ret]
        else:
            return [ret.availability, ret.dateTimeCreated, ret]

    def get(self, _storeId):
        return self.query(storeId=_storeId).order('-dateTimeCreated').fetch()

    def getLast(self, _storeId):
        return self.query(storeId=_storeId).order('-dateTimeCreated').get()

    def save(self, _partNumber, _storeId, _availability):
        obj = Available(partNumber=_partNumber,
                        storeId=_storeId,
                        availability=_availability)
        obj.put()


class CrawlingHandler(webapp2.RequestHandler):
    lastSent = None
    flag = False
    email_content = ""
    def online_store(self):
        for i in range(len(URLs_HK)):
            _url = URLs_HK[i]
            result = urlfetch.fetch(_url, headers = {'Referer': REFERRER_HK_ONLINE,'User-Agent': USER_AGENT })
            # print "header "+str(result.headers)
            # print "header msg "+str(result.header_msg)
            # print "final_url "+str(result.final_url)
            # print "status code "+str(result.status_code)
            # print result.
            if result.status_code == 200:
                content = json.loads(result.content)
                response_status =  content["head"]["status"] # 200 Apple OK
                logging.info("Fetching ... "+_url)
                try:
                    pageTitle = content["body"]["content"]["pageTitle"].decode('utf-8')

                    ### Country
                    _country = pageTitle[pageTitle.rfind('(')+1:pageTitle.rfind(')')]

                    ### Model Number
                    _partNumber = content["body"]["content"]["selected"]["partNumber"].decode('utf-8')
                    productTitle = content["body"]["content"]["selected"]["productTitle"].decode('utf-8').upper()
                    shippingLead = content["body"]["content"]["selected"]["purchaseOptions"]["shippingLead"].decode('utf-8')

                except ValueError:
                    logging.error("Receive empty json. "+_url)
                    continue
                except KeyError:
                    logging.error("Receive empty json. "+_url)
                    continue

                availability = shippingLead.find("Currently unavailable")

                ### iPhone6 or iPhone
                iphoneType = productTitle.find("PLUS") # -1 is a iPhone6, otherwise iPhone6 Plus
                if iphoneType < 0:
                    _productName = "iPhone 6"
                else:
                    _productName = "iPhone 6 Plus"

                ### Capacity
                gbList = ["16","64","128"]
                gbIndex = ""
                offset = 2
                for gb in gbList:
                    gbIndex = productTitle.find(gb)
                    offset = 3 if gb == "128" else 2
                    if gbIndex > 0:
                        break
                _capacity = productTitle[gbIndex:gbIndex+offset].strip()

                ### Color
                space_grey = productTitle.find("GREY")
                silver = productTitle.find("SILVER")
                gold = productTitle.find("GOLD")
                if space_grey > 0:
                    _color = "Space Grey"
                elif silver > 0:
                    _color = "Silver"
                elif gold > 0:
                    _color = "Gold"
                else:
                    _color = "Unknown Color"

                ### Policy
                unlocked = productTitle.find("UNLOCKED")
                _unlocked = True if unlocked > 0 else False
                if response_status == "200":
                    _availability = 0 if availability > 0 else 1
                else:
                    _availability = 2 # error from apple store

                # Do a search in case of new record in product like new part number
                availabilityObject = Available()
                # check the latest status if it has NOT been changed, then do not update.
                latest_availability = availabilityObject.get_latest_availability(_partNumber, ONLINE_TAG)
                if latest_availability[1] is None:
                    #logging.critical("online store Part Number: "+str(_partNumber) )
                    productObject = Product()
                    productObject.store(_partNumber,_productName, _capacity, _color, _unlocked, _country)
                    availabilityObject.save(_partNumber, ONLINE_TAG, _availability)
                else:
                    if latest_availability[0] != _availability:
                        availabilityObject.save(_partNumber, ONLINE_TAG, _availability)
                if _availability == 1:
                    self.email_content += "[Online] :"+str(_partNumber)+" now available. \n"
                    self.flag = True

                # self.response.headers['Content-type'] = 'application/json'
                # response = {'status': 'OK',
                #             'productTitle': productTitle,
                #             'partNumber': _partNumber,
                #             'availability': _availability
                #             }
                # response = json.dumps(response)
                logging.info('Online Store successfully fetched data')

            else:
                logging.error('Online Store is not working with status code '+result.status_code)
                # self.response.headers['Content-type'] = 'application/json'
                # response = {'status': 'Error'}
                # response = json.dumps(response)
                # self.response.write(response)


    def local_store(self):
        result = urlfetch.fetch(AVAILABILITY_JSON_HK, headers = {'Referer': REFERRER_HK_LOCAL,'User-Agent': USER_AGENT })
        if result.status_code == 200:
            content = json.loads(result.content)
            logging.info("local Store is reading ...."+result.content)
            #if iReserve Closes

            # Check if the store is closed within the minute, then update all items become unavailable.
            # Sign1: the content dictionary is empty. = store Closed
            # Sign2: Grab one of the item's last creation to see
            if len(content) == 0:
                location_object = Location()
                lastSeen = location_object.get("R409").lastOpenDateTime
                if lastSeen is not None and (datetime.datetime.now() - lastSeen).seconds < 300:
                    QuickFixHandler().get()
            else:
                #if iReserve Opens
                for _storeId in content:
                    #self.emailDistribute()
                    #logging.critical("iReserve Opens")
                    if _storeId != "updated":
                        for _partNumber in content[_storeId]:
                            _availability = 1 if content[_storeId][_partNumber] else 0
                            #productObject = Product()
                            #partNumber = productObject.peek(_partNumber)
                            #if partNumber is not None: # not a new product
                            availabilityObject = Available()
                            latest_availability = availabilityObject.get_latest_availability(_partNumber, _storeId)
                                ##########
                                #self.email_content += "[ON] "+str(model_map[_partNumber])+": at "+str(loc_map[_storeId])+" \n"
                                #self.flag = True
                                ##########
                            if latest_availability[1] is None:
                                logging.critical("local new product "+str(_partNumber)+"  at "+str(_storeId))
                            else:
                                if latest_availability[0] != _availability:
                                    availabilityObject.save(_partNumber, _storeId , _availability) # update available
                                    if _availability == 1:
                                        #logging.critical("[ON] "+str(model_map[_partNumber])+": at "+str(loc_map[_storeId]))
                                        self.email_content += "[ON] "+str(model_map[_partNumber])+": at "+str(loc_map[_storeId])+" \n"
                                        self.flag = True
                                logging.info("Successfully fetched - "+model_map[_partNumber]+" in local store at "+loc_map[_storeId])

        else:
            logging.error("Local Store Apple Server return an error "+result.status_code)

    def emailDistribute(self, _string):
        lastSentTime = None
        if self.lastSent is None:
            pass
            #logging.critical("lastSent is None")
            #logging.critical(datetime.datetime.now())
        if MailingList().getLastSent() is None:
            pass
            #logging.critical("Mailing List getLastSent is None")
        else:
            lastSentTime = MailingList().getLastSent()
            #logging.critical("Mailing List getLastSent is not None 4000 or 900 at version 012451")
            #logging.critical(str((datetime.datetime.now() - lastSentTime).seconds))

        lastSentDelta = (datetime.datetime.now() - lastSentTime).seconds
        if self.lastSent is None and (lastSentTime is None or lastSentDelta > 300 ):
            obj = MailingList()
            all = obj.getAll()
            for customer in all:
                _email = customer.email
                sender_address = "iPhone6 開賣 Alert <naivedevelopers@gmail.com>"
                subject = "[有貨] iPhone6 開賣 Alert 有Update."
                body = """
                    直入Login: https://reserve-hk.apple.com/HK/zh_HK/reserve/iPhone

                    Check邊度有貨: https://reserve.cdn-apple.com/HK/en_HK/reserve/iPhone/availability

                """
                body += _string
                logging.critical("["+str(datetime.datetime.now())+"]email writing to "+str(_email))
                mail.send_mail(sender_address,_email, subject, body)
            obj.writeLastSent()
        else:
            self.lastSent = "THINGS"


    def get(self):
        logging.info('CrawlingHandler: Starting Fetch data')
        self.online_store()
        self.local_store()
        if self.flag is True:
            self.emailDistribute(self.email_content)


class DisplayStatusHandler (webapp2.RequestHandler):
    def getJson(self):
        product_object = Product()
        result_product = product_object.query().fetch()
        dict_json_1 = {}
        for product in result_product:
            _partNumber = product.partNumber
            location_object = Location()
            result_location = location_object.query().fetch()
            _available_object = Available()
            _availability = _available_object.get_latest_availability(_partNumber,ONLINE_TAG)
            dict_json_2 = {}
            dict_json_2[ONLINE_TAG] = [_availability[0], _availability[1]]
            for location in result_location:
                _storeId = location.storeId
                _storeName = location.storeName
                _available_object = Available()
                _availability = _available_object.get_latest_availability(_partNumber,_storeId)
                dict_json_2[_storeId] = [_availability[0], _availability[1]]
            dict_json_1[_partNumber] = dict_json_2
        return dict_json_1

    def interpret(self,_available, _datetime):
        if _datetime is None:
            return "Unavailable"
        if _available == 0 or _available == 3:
            return "Unavailable ("+ u'最近一次開售'.encode('utf8') +str(datetime.timedelta(hours=+8) + _datetime)+")"
        return unquote(u"有得買 NOW".encode("latin1")).decode("utf8")

    def interpretAvailable(self,_available):
        if _available == 0 or _available == 3:
            return "Unavailable "
        return "Available NOW "

    def interpretDateTime(self,_datetime):
        if _datetime is None:
            return "Unavailable"
        return "( Last Release : "+str(datetime.timedelta(hours=+8) + _datetime)+")"

    def get(self):
        json = self.getJson()
        ret = "<table>"
        for partNumber in json:
            head = "<tr> <th id=\""+str(partNumber)+"\">"+model_map[partNumber]+"</th>"
            for loc in json[partNumber]:
                ret += head
                ret += "<th class=\""+str(partNumber)+str(loc)+"\">"+loc_map[loc]+"</th>"
                ret += "<th>"+self.interpretAvailable(json[partNumber][loc][0])+"</th>"
                ret += "<th>"+self.interpretDateTime(json[partNumber][loc][1])+"</th></tr>"
        ret += "</table>"
        self.response.headers['Content-type'] = 'text/html'
        self.response.write("<!DOCTYPE html><html>" \
            "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\
            <head><title> iPhone 6 Apple.com Status </title><body>"+ret +"</body></html>")



class GetStatusHandler(webapp2.RequestHandler):
    def get(self): # Loop through Product and get its key
        product_object = Product()
        result_product = product_object.query().fetch()
        dict_json_1 = {}
        for product in result_product:
            _partNumber = product.partNumber
            location_object = Location()
            result_location = location_object.query().fetch()
            _available_object = Available()
            _availability = _available_object.get_latest_availability(_partNumber,ONLINE_TAG)
            dict_json_2 = {}
            dict_json_2['"'+ONLINE_TAG+'"'] =  str(_availability)
            for location in result_location:
                _storeId = location.storeId
                _storeName = location.storeName
                _available_object = Available()
                _availability = _available_object.get_latest_availability(_partNumber,_storeId)
                dict_json_2['"'+_storeId+'"'] =  str(_availability)
            dict_json_1['"'+_partNumber+'"'] = dict_json_2
        ret_json = json.dumps(dict_json_1)
        self.response.headers['Content-type'] = 'application/json'
        self.response.write(ret_json)



class LandingHandler(webapp2.RequestHandler):
    def paragraph(self,_str):
        return "<p>"+_str+"</p>"

    def get(self):  # Get Request
        self.response.headers['Content-type'] = 'text/html'
        self.response.write("<!DOCTYPE html><html>" \
            "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\
            <head><title> iPhone 6 Apple.com Tracker </title><body> \
            <h1>登記 iPhone6 喺 Apple Store開售 同 iReserve預約 嘅 Mailing List </h1>\
            <p> <a href=\"http://iphone6-hkg.appspot.com/stat\">iphone6-hkg.appspot.com/stat</a>: 0759 - 0847 every 1 minute<br> \
            <p> <a href=\"http://iphone6-707.appspot.com/stat\">iphone6-707.appspot.com/stat</a>: 0847 - 2000 every 1 minute<br>\
            <p> <a href=\"http://iphone6-hkgolden.appspot.com/stat\">iphone6-hkgolden.appspot.com/stat</a> 2001 - 0758 every 2 minutes </p> \
            <form method=\"POST\" action=\"/getEmail\"><input type=\"email\" name=\"email\" id=\"email\"\
             placeholder=\"Email Address\" />\
            <input type=\"submit\" value=\"Sign Up\" /> \
            <script type=\"text/javascript\" \
            src=\"http://www.google.com/recaptcha/api/challenge?k="+PUBLIC_KEY+"\"> \
            </script><noscript> \
            <iframe src=\"http://www.google.com/recaptcha/api/noscript?k="+PUBLIC_KEY+"\" \
                height=\"300\" width=\"500\" frameborder=\"0\"></iframe><br> \
            <textarea name=\"recaptcha_challenge_field\" rows=\"3\" cols=\"40\"></textarea> \
            <input type=\"hidden\" name=\"recaptcha_response_field\" value=\"manual_challenge\"> </noscript></form> \
            <p> Created By 高登高仔 @ HKGolden.com </p>\
            </body></html>")
        #<iframe src=\"/display\" style=\"border: 0; position: absolute;  left:0; right:0;  width:100%; height:100%\"\">


class StorePushHandler(webapp2.RequestHandler):
    def get(self):
        logging.info('Fetch data from STORE_JSON_HK')
        result = urlfetch.fetch(STORE_JSON_HK)
        content = json.loads(result.content)
        stores = content["stores"]
        for s in stores:
            obj = Location()
            obj.save(s["storeNumber"], s["storeName"])

class SuccessRegistrationHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("<html><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\
        <body><h1>搞掂咗。你會收到一封Email架。<p> You will receive a confirmation email containing \
            information how to unsubscribe</p></body></html>")

class FailedRegistrationHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("<html><head><meta http-equiv=\"refresh\" content=\"3;url=/\" /> \
        <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" /></head><body>\
        <h1> 可能一) 錯Captcha呀。你係小學雞。啲字母都搞唔清。再嚟過啦。 </h1> \
        <h1> 可能二) 你咪入過囉. 做乜搞多次. </h1> \
        <p>Redirecting in 3 seconds... or <a href=\"/\" >Click here to the landing page. \
        </a></p></body></html>")





class ObtainEmailHandler(webapp2.RequestHandler):
    def validate(self, _email):
        return re.match(r'[^@]+@[^@]+\.[^@]+', _email)

    def get(self):
        password = self.request.get("password")
        if password == "dying":
            list = ["beauty235@gmail.com","bennylai@cen-1.com","cheukhinli@yahoo.com.hk","danielckn89@gmail.com",
                    "jonathanyth@gmail.com","michaelwong1231@gmail.com","oscarlai2383@gmail.com","s6f318484@hotmail.com",
                    "sailokto@yahoo.com.hk",
                    "wuwuyan1214@yahoo.com.hk",
                    "U3503819@GMAIL.COM",
                    "awdhoward@gmail.com",
                    "jonathanyth@gmail.com",
                    "laihiube@gmail.com",
                    "sailokto@yahoo.com.hk",
                    "wuwuyan1214@yahoo.com.hk",
                    "andrew030608@yahoo.com.hk",
                    "chanhok@live.hk",
                    "jonathanyth@gmail.com",
                    "kc343000@gmail.com",
                    "lcklrt1004@gmail.com",
                    "ryantck@gmail.com",
                    "sailokto@yahoo.com.hk",
                    "wuwuyan1214@yahoo.com.hk"]
            obj = MailingList()
            for _email in list:
                if mail.is_email_valid(_email):
                    if obj.store(_email) is True:
                        sender_address = "iPhone6 開賣 Alert <naivedevelopers@gmail.com>"
                        subject = "多謝登記 iPhone6 開賣 Alert 服務"
                        body = """

                             最終入口: http://iphone6-hkgolden.appspot.com/
                             Backup1: http://iphone6-hkg.appspot.com/
                             Backup2: http://iphone6-707.appspot.com/

                             直入Login: https://reserve-hk.apple.com/HK/zh_HK/reserve/iPhone

                            Check邊度有貨: https://reserve.cdn-apple.com/HK/en_HK/reserve/iPhone/availability

                        """
                        mail.send_mail(sender_address,_email, subject, body)
                        logging.info("Welcome letter sent to "+_email)
            self.redirect("/success")
        else:
            self.redirect("/failure#1")




    def post(self):
        VERIFY_URL = "http://www.google.com/recaptcha/api/verify"
        recaptcha_challenge_field = self.request.get("recaptcha_challenge_field")
        recaptcha_response_field = self.request.get("recaptcha_response_field")
        remoteIp = self.request.remote_addr
        data = {
            "privatekey": PRIVATE_KEY,
            "remoteip": remoteIp,
            "challenge": recaptcha_challenge_field,
            "response": recaptcha_response_field}

        response = urlfetch.fetch(url=VERIFY_URL,
                          payload=urlencode(data),
                          method="POST")
        captcha_ok = True if response.content.split("\n")[0] == "true" else False

        # logging.error("First line: %s " % response.content.split("\n")[0])
        # logging.error("Valid: %s" % captcha_ok)

        if captcha_ok:
            _email = self.request.get("email")
            obj = MailingList()
            if mail.is_email_valid(_email):
                if obj.store(_email) is True:

                    sender_address = "iPhone6 開賣 Alert <naivedevelopers@gmail.com>"
                    subject = "多謝登記 iPhone6 開賣 Alert 服務"
                    body = """

                         最終入口: http://iphone6-hkgolden.appspot.com/
                         Backup1: http://iphone6-hkg.appspot.com/
                         Backup2: http://iphone6-707.appspot.com/

                         直入Login: https://reserve-hk.apple.com/HK/zh_HK/reserve/iPhone

                        Check邊度有貨: https://reserve.cdn-apple.com/HK/en_HK/reserve/iPhone/availability

                    """
                    mail.send_mail(sender_address,_email, subject, body)
                    self.redirect("/success")
                else:
                    self.redirect("/failure#3")
            else:
                self.redirect("/failure#2")
        else:
            self.redirect("/failure#1")

# Mutate the availability value from 1 to 0
class QuickFixHandler(webapp2.RequestHandler):
    def get(self):
        obj = Product()
        products = obj.get()
        for each in products:
            _partNumber = each.partNumber
            available_obj = Available()
            for _storeId in loc_map:
                ret_list = available_obj.get_latest_availability(_partNumber, _storeId)
                if ret_list[0] != 0:
                    ret_list[2].availability = 0
                    ret_list[2].put()


getEmailApp = webapp2.WSGIApplication([
    ('/getEmail', ObtainEmailHandler)
], debug=True)

landingApp = webapp2.WSGIApplication([
    ('/', LandingHandler)
], debug=True)

# getStatusApp = webapp2.WSGIApplication([
#     ('/status', GetStatusHandler)
# ], debug=True)

pushStoreApp = webapp2.WSGIApplication([
    ('/push', StorePushHandler)
], debug=True)

crawlApp = webapp2.WSGIApplication([
    ('/crawl', CrawlingHandler)
], debug=True)

successRegistrationApp = webapp2.WSGIApplication([
    ('/success', SuccessRegistrationHandler)
 ], debug=True)

failedRegistrationApp = webapp2.WSGIApplication([
    ('/failure', FailedRegistrationHandler)
 ], debug=True)

displayStatusApp = webapp2.WSGIApplication([
    ('/stat', DisplayStatusHandler)
 ], debug=True)

quickFixApp = webapp2.WSGIApplication([
    ('/fix', QuickFixHandler)
 ], debug=True)

