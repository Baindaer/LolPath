import lolpath.RiotConst as Const
from lolpath.RiotApi import RiotApi


def main():
    api = RiotApi(Const.API_KEY, 'la1')
    r = api.get_summoner_by_name('baindaer')
    s = api.get_static_data()
    print(r)
    print(s)

if __name__ == "__main__":
    main()
