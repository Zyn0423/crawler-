import requests
import re,json,os
import jsonpath



class MeiTuan(object):

    def __init__(self,offset):

        self.url = 'http://meishi.meituan.com/i/api/channel/deal/list'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36',
            'Referer':'http://meishi.meituan.com/i/?ci=1&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1',
            'Cookie':'_hc.v=b47511c8-71e5-0f49-1c04-d1998f649802.1532833240; _lxsdk_cuid=164e3fb12eec8-0f752eb988fff3-277d274d-419ce-164e3fb12efc8; IJSESSIONID=mmxgjm853l8w1wwihq4r8x1fo; iuuid=5C12E7FBB462CF18D5933EBF713043BFBA88C58BDA4238CB67770967AD7772D7; ci=1; cityname=%E5%8C%97%E4%BA%AC; webp=1; __utmc=74597006; _lxsdk=5C12E7FBB462CF18D5933EBF713043BFBA88C58BDA4238CB67770967AD7772D7; client-id=226a53b8-02cf-40c6-8bdc-fa84d585aefa; uuid=0ad63b1c-1ad4-4f82-b24d-2a49e8c2ca69; __utma=74597006.323140895.1532932034.1532932034.1532936072.2; __utmz=74597006.1532936072.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ci3=1; latlng=39.90469,116.40717,1532936429101; __utmb=74597006.6.9.1532936430327; i_extend=C_b1Gimthomepagecategory11H__a; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=152416774.1532833239919.1532936836035.1532936871347.17; _lxsdk_s=164ea1a61db-388-76a-8d7%7C%7C93',
            'Host': 'meishi.meituan.com',
            'Origin': 'http://meishi.meituan.com'
        }
        self.offset = offset

        self.post_data = {"app": "",
                     "areaId": 0,
                     "cateId": 1,
                     "deal_attr_23": "",
                     "deal_attr_24": "",
                     "deal_attr_25": "",
                     "limit": 15,
                     "lineId": 0,
                     "offset": 0,
                     "optimusCode": 10,
                     "originUrl": "http://meishi.meituan.com/i/?ci=1&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1",
                     "partner": 126,
                     "platform": 3,
                     "poi_attr_20033": "",
                     "poi_attr_20043": "",
                     "riskLevel": 1,
                     "sort": "default",
                     "stationId": 0,
                     "uuid": "b878b837-a83f-4b4c-8d07-f25df5bd36a6",
                     "version": "8.3.3", }

    def get_data(self,url,post_data):



        response = requests.post(url,headers=self.headers,data=post_data)

        return response.content.decode()

    def save_data(self,res):

        data = json.loads(res)

        names = jsonpath.jsonpath(data,'$..name')
        # prices = jsonpath.jsonpath(data,'$..avgPrice')
        urls = jsonpath.jsonpath(data,'$..ctPoi')
        poi_id = jsonpath.jsonpath(data,'$..poiid')

        url_list = []
        i=0
        for url in urls:

            url_s = 'http://meishi.meituan.com/i/poi/'+poi_id[i]+'?ct_poi='+url
            url_list.append(url_s)
            i +=1
        return names,url_list

    def parse_data(self,names,url_list):

        data_list = []
        i = 0

        for name in names:

            data_dict = dict()
            data_dict[name] = url_list[i]
            data_list.append(data_dict)
            i += 1
        return data_list


    def download(self,data_list):

        with open('meituan.txt','w') as f:
            for i in data_list:

                f.write(str(i)+'\n')



    def run(self):

        url = self.url


        while True:

            self.post_data["offset"] = self.offset * 15

            post_data = self.post_data

            res = self.get_data(url,post_data)

            names,url_list = self.save_data(res)

            data_list = self.parse_data(names,url_list)

            self.download(data_list)

            self.offset -= 1

            if self.offset == 0:
                break

if __name__ == '__main__':
    mt = MeiTuan(5)
    mt.run()

