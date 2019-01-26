from iqoptionapi.ws.chanels.base import Base
class GetFinancialInformation(Base):
    name = "sendMessage"
    def __call__(self,activeId):
        data = {
            "name":"get-financial-information",
            "version":"1.0",
            "body":{
                "query":"query GetAssetProfileInfo($activeId:ActiveID!, $locale: LocaleName){\n active(id: $activeId) {\n id\n name(source: TradeRoom, locale: $locale)\n ticker\n media {\n siteBackground\n }\n charts {\n dtd {\n change\n }\n m1 {\n change\n }\n y1 {\n change\n }\n ytd {\n change\n }\n }\n index_fininfo: fininfo {\n ... on Index {\n description(locale: $locale)\n }\n }\n fininfo {\n ... on Pair {\n type\n description(locale: $locale)\n currency {\n name(locale: $locale)\n }\n base {\n name(locale: $locale)\n ... on Stock {\n company {\n country {\n nameShort\n }\n gics {\n sector\n industry\n }\n site\n domain\n }\n keyStat {\n marketCap\n peRatioHigh\n }\n }\n ... on CryptoCurrency {\n site\n domain\n coinsInCirculation\n maxCoinsQuantity\n volume24h\n marketCap\n }\n }\n }\n }\n }\n }",
                "operationName": "GetAssetProfileInfo",
                "variables":{
                    "activeId":activeId
                }
            }
        }
        self.send_websocket_request(self.name, data)
 
 