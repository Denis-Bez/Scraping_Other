import requests, json, time
from config import CONFIG


# --- Class for Yandex APIconnection and create ads ---
class API_Requests:
 
    def __init__(self, ads_id):
        self.__token = CONFIG['ACCESS_TOKEN']
        self.__headers = {
                            'Authorization': 'Bearer ' + self.__token, 
                            'Accept-Language': 'ru'
                        }
        self.__serviceURL = {
                            'Ads': 'https://api.direct.yandex.com/json/v5/ads',
                            }    
        self.ads_id = ads_id


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
    

    def Start_ads(self):
        result = self.GetStatus_Ads()
        # Unarchived ads
        if result[0]:
            if result[1] == 'Архивно.':
                method = 'unarchive'
                params = {
                    "SelectionCriteria": {
                        "Ids": eval(self.ads_id)    
                    }
                }
                body = self.create_Body(method, params)
                result = self.Send_Request(body, self.__serviceURL['Ads'])
                try:
                    result['error']
                    return [False, f"Error! Don't can Start archive ads {result}"]
                except:
                    time.sleep(20)
            # Start ads
            method = 'resume'
            params = {
                "SelectionCriteria": {
                    "Ids": eval(self.ads_id)
                }
            }
            body = self.create_Body(method, params)
            result = self.Send_Request(body, self.__serviceURL['Ads'])
            try:
                result['error']
                return [False, f"Error! Don't can Start ads {result}"]
            except:
                return [True, result]
        else:
            return [False, f"Error! Couldn't get ad's Status {result}"]


    def Stop_ads(self):
        method = 'suspend'
        params = {
            "SelectionCriteria": {
                "Ids": eval(self.ads_id)
            }
        }
        body = self.create_Body(method, params)
        result = self.Send_Request(body, self.__serviceURL['Ads'])
        try:
            result['error']
            return [False, f"Error! Couldn't Stop ads {result}"]
        except:
            return [True, result]


# --- GETTING INFORMATION --- 

    def GetStatus_Ads(self):
        method = 'get'
        params = {
            "SelectionCriteria": {
                "Ids": eval(self.ads_id)
            },
            "FieldNames": ["StatusClarification"]
        }   
        body = self.create_Body(method, params)
        result = self.Send_Request(body, self.__serviceURL['Ads'])  
        try:
            result = result['result']['Ads'][0]['StatusClarification']
            return [True, result]
        except:
            return [False, f"Error! Don't got ad's Status {result}"]
    

    