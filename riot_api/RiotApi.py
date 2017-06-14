import requests
import RiotConst as Const


class RiotApi(object):

    def __init__(self, api_key, region):
        self.api_key = api_key
        self.region = region

    def _request(self, api_url, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        response = requests.get(
            Const.URL['base'].format(
                proxy=self.region,
                region=self.region,
                url=api_url
            ),
            params=args
        )
        return response.json()

    def get_summoner_by_name(self, name):
        api_url = Const.URL['summoner_by_name'].format(
            version=Const.API_VERSIONS['summoner'],
            names=name,
            )
        return self._request(api_url)
