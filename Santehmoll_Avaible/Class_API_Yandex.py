import requests, json, re, time
from .config import CONFIG
from datetime import date
from .Dictionary_TextForAPIYandex import NegativeKeywords, SitelinkSetId, AdExtensionIds


# --- Class for Yandex APIconnection and create ads ---
class API_Requests:
 
    def __init__(self, adTexts):
        self.__token = CONFIG['ACCESS_TOKEN']
        self.__headers = {
                            'Authorization': 'Bearer ' + self.__token, 
                            'Accept-Language': 'ru'
                        }
        self.__serviceURL = {
                            'campaignsURL': 'https://api.direct.yandex.com/json/v5/campaigns/',
                            'adgroupsURL':  'https://api.direct.yandex.com/json/v5/adgroups',
                            'dictionaries': 'https://api.direct.yandex.com/json/v5/dictionaries',
                            'vcard': 'https://api.direct.yandex.com/json/v5/vcards',
                            'adimages': 'https://api.direct.yandex.com/json/v5/adimages',
                            'sitelinks': 'https://api.direct.yandex.com/json/v5/sitelinks',
                            'adextensions': 'https://api.direct.yandex.com/json/v5/adextensions',
                            'keywords': 'https://api.direct.yandex.com/json/v5/keywords',
                            'Ads': 'https://api.direct.yandex.com/json/v5/ads',
                            }
        
        self.adTexts = adTexts


    def Send_Request(self, body, serviceURL):
        jsonBody = json.dumps(body, ensure_ascii=False).encode('utf8')
        result = requests.post(serviceURL, jsonBody, headers=self.__headers)

        return result.json()
    

    def create_Body(self, method, params):
        body = {
                'method': method,
                'params': params
                }   

        return body


    def delete_if_error(self, id, service):
        #TODO Mega-crutch. Detecting type of input 'id' (list or int?)
        if type(id) == type(1):
            ID = []
            ID.append(id)
            id = ID
        
        method = 'delete'
        params = {
            "SelectionCriteria": {
                "Ids": id
            }
        }

        body = self.create_Body(method, params)
        self.Send_Request(body, self.__serviceURL[service])
    

    def Moderation_Send(self, Ads_Ids):
        method = 'moderate'
        params = {
            "SelectionCriteria": {
                "Ids": Ads_Ids
            }
        }

        body = self.create_Body(method, params)
        self.Send_Request(body, self.__serviceURL['Ads'])
    

    def Start_ads(self):
        result = self.GetStatus_Ads()
        if result['result']['Ads'][0]['StatusClarification'] == 'Архивно.':
            method = 'unarchive'
            params = {
                "SelectionCriteria": {
                    "Ids": eval(self.adTexts)    
                }
            }
            body = self.create_Body(method, params)
            self.Send_Request(body, self.__serviceURL['Ads'])
            time.sleep(10)

        method = 'resume'
        params = {
            "SelectionCriteria": {
                "Ids": eval(self.adTexts)
            }
        }

        body = self.create_Body(method, params)
        return self.Send_Request(body, self.__serviceURL['Ads'])


    def Stop_ads(self):
        method = 'suspend'
        params = {
            "SelectionCriteria": {
                "Ids": eval(self.adTexts)
            }
        }

        body = self.create_Body(method, params)
        return self.Send_Request(body, self.__serviceURL['Ads'])
    

    def Update_Price(self, new_Price):
        Price_Update = []
        for i in eval(self.adTexts):
            diction = {}
            diction['Id'] = i
            diction['TextAd'] = {'PriceExtension': {'Price': int(new_Price)*1000000}}
            Price_Update.append(diction)

        method = 'update'
        params = {
            "Ads": Price_Update
        }

        body = self.create_Body(method, params)
        return self.Send_Request(body, self.__serviceURL['Ads'])


    def Update_OldPrice(self, new_oldPrice):
        if re.search(r"Don't", new_oldPrice):
            new_oldPrice = 0
         
        OldPrice_Update = []
        for i in eval(self.adTexts):
            diction = {}
            diction['Id'] = i
            diction['TextAd'] = {'PriceExtension': {'OldPrice': int(new_oldPrice)*1000000}}
            OldPrice_Update.append(diction)

        method = 'update'
        params = {
            "Ads": OldPrice_Update
        }

        body = self.create_Body(method, params)
        return self.Send_Request(body, self.__serviceURL['Ads'])


# --- CREATE ADS ---
 
    # Create new Compaign. It's main method for create ads
    def add_Compaign(self, last_ad):
        
        # Get last ad's id from database
        compaign_number = int(last_ad.compaign_number)
        CampaignId = last_ad.CampaignId
        vCardId = last_ad.vCardId

        # If current company already has 1000 Grours create new company
        if self.GroupsCount(CampaignId) >= 1000:
            startdate = date.today().isoformat()
            method = 'add'
            params = {
                        "Campaigns": [{
                            "Name": "SantehmollAPP_" + str(compaign_number + 1),
                            "StartDate": startdate,
                            "DailyBudget":{
                                "Amount": "300000000",
                                "Mode":"STANDARD",
                            },
                            "NegativeKeywords": {
                                "Items": NegativeKeywords,
                            },
                            "TextCampaign": {
                                "BiddingStrategy": {
                                    "Search": {"BiddingStrategyType": "HIGHEST_POSITION",},
                                    "Network": {"BiddingStrategyType": "SERVING_OFF",},
                                },
                            }
                        }]
                    }
        
            body = self.create_Body(method, params)
            try:
                CampaignId = self.Send_Request(body, self.__serviceURL['campaignsURL'])
                CampaignId = CampaignId['result']['AddResults'][0]['Id']
                compaign_number += 1
                # Creating 'vCard'
                resultVCard = self.add_vCard(CampaignId)
                if resultVCard:
                    vCardId = resultVCard['AddResults'][0]['Id']
                else:
                    print("Error creating 'vCard'. Deleting new company")
                    self.delete_if_error(CampaignId, 'campaignsURL')
                    return [False, "Error! Fail to create vCard"]
            except:
                return [False, f"Error! Fail to create new company: {CampaignId}"]
        
        # Create Ad's Group
        try:
            AdGroupId = self.add_adGroup(CampaignId)
            AdGroupId = AdGroupId['result']['AddResults'][0]['Id']
        except:
            # Checking If company has 0 groups
            try:
                self.GroupsCount(CampaignId)
            except:
                print('Ошибка создания группы. Удаляем компанию')
                self.delete_if_error(CampaignId, 'campaignsURL')
            return [False, "Error! Fail to create new Ad's group"]

        # Create Keywords
        result = self.add_Keywords(AdGroupId)['result']['AddResults']
        KeywordsId = []
        check_errors = False
        # Translate dictionsry of the Keyword Ids to list of Keyword Ids
        for i in result:
            if list(i)[0] == 'Id':
                KeywordsId.append(i['Id'])
            else:
                check_errors = True
        if check_errors:
            print('Error creating keywords. Deleting group, keywords (if exist) and company (if new)')
            self.delete_if_error(KeywordsId, 'keywords')
            self.delete_if_error(AdGroupId, 'adgroupsURL')
            # Checking If company has 0 groups
            try:
                self.GroupsCount(CampaignId)
            except:
                self.delete_if_error(CampaignId, 'campaignsURL')
            
            return [False, f"Error! Fail to create new Ad's group {result}"]
        
        # Create Ad
        result = self.add_Ads(AdGroupId, vCardId)
        ads_Id = result
        if not result[0]:
            print(f'Error creating ads: {result[1]}. Deleting Keywords, group and compaign (if it new)')
            self.delete_if_error(KeywordsId, 'keywords')
            self.delete_if_error(AdGroupId, 'adgroupsURL')
            # Checking If company has 0 groups
            try:
                self.GroupsCount(CampaignId)
            except:
                self.delete_if_error(CampaignId, 'campaignsURL')
            return [False, f"Error! Fail to create new Ads: {result[1]}"]

        
        return [CampaignId, vCardId, ads_Id, compaign_number]


    # Create new ad Group and ads in Group
    def add_adGroup(self, CampaignId):
        method = 'add'
        params = {
                "AdGroups": [{
                    "Name": self.adTexts['groupName'],
                    "CampaignId": CampaignId,
                    "RegionIds": ["225", "977"],
                }]
        }

        body = self.create_Body(method, params)
        
        return self.Send_Request(body, self.__serviceURL['adgroupsURL'])
        

    # Create new 3 ads (input: id adgroup)
    def add_Ads(self, groupId, vCardId):
        add_created_id = []
        method = 'add'
        for i in range(0, 2):
            params = {
                "Ads": [{
                    "AdGroupId": groupId,
                    "TextAd": {
                        "Title": self.adTexts['mainTitle'][i],
                        "Title2": self.adTexts['subTitle'][i],
                        "Text": self.adTexts['text'][i],
                        "Href": self.adTexts['url'],
                        "Mobile": "NO",
                        "DisplayUrlPath":self.adTexts['suburl'],
                        "VCardId": vCardId,
                        "SitelinkSetId": SitelinkSetId,
                        "AdExtensionIds": AdExtensionIds,
                        "PriceExtension": {
                            "Price": int(self.adTexts['price'])*1000000,
                            "PriceQualifier": "NONE",
                            "PriceCurrency": "RUB",
                        },
                    },
                }]
            }
            # Invite 'old price' if it exist
            if not re.search(r"Don't", self.adTexts['oldprice']):
                params["Ads"][0]["TextAd"]["PriceExtension"]["OldPrice"] = int(self.adTexts['oldprice'])*1000000
            
            body = self.create_Body(method, params)
            result = self.Send_Request(body, self.__serviceURL['Ads'])
            try:
                add_created_id.append(result['result']['AddResults'][0]['Id'])
            except:
                # Deleted ads if error
                for id in add_created_id:
                    self.delete_if_error(id, 'Ads')
                return [False, result]

        # Creating mobile ad the some as second ad
        params["Ads"][0]["TextAd"]["Mobile"] = "YES"
        body = self.create_Body(method, params)
        result = self.Send_Request(body, self.__serviceURL['Ads'])
        try:
            add_created_id.append(result['result']['AddResults'][0]['Id'])
        except:
            # Deleted ads if error
            for id in add_created_id:
                self.delete_if_error(id, 'Ads')
            return [False, result]
        
        # Return list of Ads Ids
        return add_created_id


    # Invite Keywords in ad's group (input: id adgroup)
    def add_Keywords(self, adGroupId):
        method = 'add'

        params = {"Keywords": []}
        
        for key in self.adTexts['keyPhrases']:
            params["Keywords"].append({"Keyword": key, "AdGroupId": adGroupId, "Bid": "10000000",})
        
        body = self.create_Body(method, params)

        return self.Send_Request(body, self.__serviceURL['keywords'])


    # Create vCard. Start to get vCard id and save it in
    def add_vCard(self, CampaignId):
        method = 'add'

        params = {
            "VCards": [{
                "CampaignId": CampaignId, 
                "Country": "Россия",
                "City": "Москва",
                "CompanyName": "Магазин сантехники СантехМолл",
                "WorkTime": "0;6;09;0;22;0",
                "Phone": {
                    "CountryCode": "8",
                    "CityCode": "800",
                    "PhoneNumber": "333-00-48",
                },
                "Street": "Рязанский пр-т",
                "House": "2",
                "Building": "3",
                "ExtraMessage": "У нас в магазине можно купить сантехнику отечественного и зарубежного производства по доступным ценам. Мы сотрудничаем с 60 брендами из Италии, Франциии, России, Испании и других стран.",
                "ContactEmail": "zakaz@santehmoll.ru",
                "Ogrn": "1167746096484",
            }]
        }

        body = self.create_Body(method, params)
        result =  self.Send_Request(body, self.__serviceURL['vcard'])

        return result.get('result', False)
    

    # Create set extension for ads (return: 'AdExtensionIds' for add_Ads()). Once for all company. Handly saved in 'Dictionary_TextForAPIYandex'
    def adExtension(self):
        method = 'add'

        params = {
            "AdExtensions": [{
                "Callout": {"CalloutText": "Кредит, Рассрочка"},
                "Callout": {"CalloutText": "В Наличии"},
                "Callout": {"CalloutText": "Бережная доставка"},
                "Callout": {"CalloutText": "Поддержка 9:00-22:00"},
            }]
        }

        body = self.create_Body(method, params)
        return self.Send_Request(body, self.__serviceURL['adextensions'])
    

    # Create set fast links for ads (return: 'SitelinkSetId' for add_Ads()). Once for all company. Handly save in 'Dictionary_TextForAPIYandex'
    def adSitelinks(self):
        method = 'add'

        params = {
            "SitelinksSets": [{
                "Sitelinks": [
                    {"Title": "Каталог сантехники", "Href": "https://ad.admitad.com/g/dra8qamlvk037e654884d22e56a5b7/?ulp=https%3A%2F%2Fsantehmoll.ru%2Fcategory%2Fsantekhnika%2F", "Description": "Большой выбор сантехники. Скидки и подарки. Доставка по РФ",},
                    {"Title": "Мебель для ванной", "Href": "https://ad.admitad.com/g/dra8qamlvk037e654884d22e56a5b7/?ulp=https%3A%2F%2Fsantehmoll.ru%2Fcategory%2Fmebel-dlya-vannoy%2F", "Description": "Каталог мебели для ванной комнаты. Скидки, уцененные товары",},
                    {"Title": "Инженерная сантехника", "Href": "https://ad.admitad.com/g/dra8qamlvk037e654884d22e56a5b7/?ulp=https%3A%2F%2Fsantehmoll.ru%2Fcategory%2Finzhenernaja-santehnika%2F", "Description": "Широкий выбор труб, арматуры, фасонных частей",},
                    {"Title": "Каталог скидок", "Href": "https://ad.admitad.com/g/dra8qamlvk037e654884d22e56a5b7/?ulp=https%3A%2F%2Fsantehmoll.ru%2Fdiscounts%2F", "Description": "Купить сантехнику со скидкой. Работаем с 2014 года",},
                    {"Title": "Доставка", "Href": "https://ad.admitad.com/g/dra8qamlvk037e654884d22e56a5b7/?subid=3&ulp=https%3A%2F%2Fsantehmoll.ru%2Fdostavka-i-oplata%2F%3Fshipping%3Ddostavka", "Description": "Аккуратная доставка по России и Москве",},
                    {"Title": "Сантехника в кредит", "Href": "https://ad.admitad.com/g/dra8qamlvk037e654884d22e56a5b7/?subid=3&ulp=https%3A%2F%2Fsantehmoll.ru%2Fsantekhnika-v-kredit%2F", "Description": "Купить сантехнику в кредит или рассрочку",},
                    {"Title": "Гарантия", "Href": "https://ad.admitad.com/g/dra8qamlvk037e654884d22e56a5b7/?subid=3&ulp=https%3A%2F%2Fsantehmoll.ru%2Fpriem-i-vozvrat-tovara%2F", "Description": "Получения и возврат товара, гарантия, сервис",},
                    {"Title": "Контакты", "Href": "https://ad.admitad.com/g/dra8qamlvk037e654884d22e56a5b7/?subid=3&ulp=https%3A%2F%2Fsantehmoll.ru%2Fkontakty%2F", "Description": "Организуем доставку заказа в любую точку России",},
                    ]
            }]
        }

        body = self.create_Body(method, params)
        return self.Send_Request(body, self.__serviceURL['sitelinks'])


# --- GETTING INFORMATION ---

    # Getting list of region's codes (input: region that you want to find)
    def dictionry_regions(self, searchRegion):
        method = 'get'
        params = {
                    "DictionaryNames": ["GeoRegions"],
                 }
        
        body = self.create_Body(method, params)
        regions = self.Send_Request(body, self.__serviceURL['dictionaries'])
        regions = regions['result']['GeoRegions']

        for i in regions:
            if i["GeoRegionName"] == searchRegion:
                return i
        
        return "Region isn't found"
    

    # TODO Error "Not enough points" (https://yandex.ru/dev/direct/doc/examples-v5/python3-requests-points.html)
    def balance_Points(self):
        pass


    # Count the groups in the campaign. All groups including archived groups (input: compaign id, return: count groups)
    def GroupsCount(self, CampaignId):
        method = 'get'
        params = {
                    'SelectionCriteria': { 'CampaignIds': [CampaignId] },
                    'FieldNames': ['Id']
                 }
        
        body = self.create_Body(method, params)
        result = self.Send_Request(body, self.__serviceURL['adgroupsURL'])

        return len(result['result']['AdGroups'])
    

    def GetStatus_Ads(self):
        method = 'get'
        params = {
            "SelectionCriteria": {
                "Ids": eval(self.adTexts)
            },
            "FieldNames": ["StatusClarification"]
        }
        
        body = self.create_Body(method, params)
        result = self.Send_Request(body, self.__serviceURL['Ads'])
        return result
    

    # Getting information about all company
    def getCampaigns(self):
        method = 'get'
        params = {
                    'SelectionCriteria': {"States":["ON"]},
                    'FieldNames': ['Id', 'Name', 'Status'],
                 }
        
        body = self.create_Body(method, params)
        return self.Send_Request(body, self.__serviceURL['campaignsURL'])
    

    # Gettig all extensions in accaunt (Id and Text)
    def getExtensions(self):
        method = 'get'
        params = {
            "SelectionCriteria": {},
            "FieldNames": [("Id")],
            "CalloutFieldNames": [( "CalloutText" )],
        }

        body = self.create_Body(method, params)
        return self.Send_Request(body, self.__serviceURL['adextensions'])