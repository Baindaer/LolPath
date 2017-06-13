from RiotApi import RiotApi
import RiotConst as Const


def main():
    api = RiotApi(Const.API_KEY, 'la1')
    r = api.get_summoner_by_name('baindaer')
    print r

if __name__ == "__main__":
    main()
