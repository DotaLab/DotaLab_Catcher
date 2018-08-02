#!/usr/bin/env python
# encoding=utf-8

__author__ = 'Vietronic'
__date__ = '$2018-7-23$'

import requests
import psycopg2
from Config import ApiConfig
from Database import Database


class Entity:
    def __init__(self):
        # 初始化API数据
        apic = ApiConfig()
        self.API_URL = apic.api_url()
        self.API_KEY = apic.api_key()
        return


    def getJSON(self, url):
        # 错误处理机制防止获取页面出错
        try:
            # 获取页面
            temp = requests.get(url)
            # 如果响应状态码不是 200，就主动抛出异常
            temp.raise_for_status()
        except requests.RequestException as e:
            print(e)
            # 如果出错则返回空
            return None
        else:
            # 返回获得的json
            t = temp.json()
            return t


    def getHeroIdAll(self):
        db = Database()

        key = ["id"]
        hero_ids = db.selectJsonData( key, "heroes")

        hero_id = []
        for i in hero_ids:
            hero_id.append(i[0])
        return hero_id


    def getHeroes(self):
        DBprop = ["id","name","localized_name","primary_attr","attack_type","roles"]

        info = self.getJSON(self.API_URL + "heroes" + self.API_KEY)

        db = Database()

        if info is None:
            return

        for i in info:
            hero = {}
            for prop in i:
                if prop in DBprop:
                    hero[prop] = i[prop]

            if db.selectJsonDataCount( hero, "heroes") == 0:
                db.deleteJsonData({'id': hero['id']}, "heroes")
                db.insertJsonData( hero, "heroes")
        return 


    def getHeroStat(self):
        db = Database()

        DBprop = ["id","name","localized_name","img","icon","pro_win","pro_pick","hero_id","pro_ban"]
        
        info = self.getJSON(self.API_URL + "heroStats" + self.API_KEY)

        if info is None:
            return

        for i in info:
            hero_stats = {}
            for prop in i:
                if prop in DBprop:
                    hero_stats[prop] = i[prop]

            if db.selectJsonDataCount( hero_stats, "hero_stats") == 0:
                db.deleteJsonData({'id': hero_stats['id']}, "hero_stats")
                db.insertJsonData( hero_stats, "hero_stats")
        return 
    
    
    def getHeroesMatchups(self):
        db = Database()

        DBprop = ["hero_id","games_played","wins"]

        hero_ids = self.getHeroIdAll()

        if hero_ids is None:
            return

        for id in hero_ids:
            info = self.getJSON(self.API_URL + "heroes/" + str(id) + "/matchups" + self.API_KEY)

            if info is None:
                return

            for i in info:
                matchup = {}
                for prop in i:
                    if prop in DBprop:
                        matchup[prop] = i[prop]
                matchup["hero"] = str(id)

                if db.selectJsonDataCount( matchup, "heroes_matchups") == 0:
                    con_data = {'hero': matchup['hero'], 'hero_id': matchup['hero_id']}
                    db.deleteJsonData( con_data, "heroes_matchups")
                    db.insertJsonData( matchup, "heroes_matchups")
        return 


    def getHeroesDurations(self):
        db = Database()

        DBprop = ["hero_id","duration_bin","games_played","wins"]

        hero_ids = self.getHeroIdAll()

        if hero_ids is None:
            return

        for id in hero_ids:
            info = self.getJSON(self.API_URL + "heroes/" + str(id) + "/durations" + self.API_KEY)

            if info is None:
                return

            for i in info:
                duration = {}
                for prop in i:
                    if prop in DBprop:
                        duration[prop] = i[prop]
                duration["hero_id"] = str(id)

                if db.selectJsonDataCount( duration, "heroes_durations") == 0:
                    con_data = {'hero_id': duration['hero_id'], 'duration_bin': duration['duration_bin']}
                    db.deleteJsonData( con_data, "heroes_durations")
                    db.insertJsonData( duration, "heroes_durations")
        return 


    def getRankings(self):
        db = Database()

        DBprop = ["account_id", "steamid", "avatar", "avatarmedium", "avatarfull", "profileurl", "personaname", "last_login timestamp", "full_history_time timestamp", "cheese integer", "fh_unavailable", "loccountrycode", "last_match_time"]

        hero_ids = self.getHeroIdAll()

        if hero_ids is None:
            return

        for id in hero_ids:
            info = self.getJSON(self.API_URL + "rankings?hero_id=" + str(id))
        
            if info is None:
                return

            for rankinfo in info["rankings"]:
                rank = {}
                rank["hero_id"] = id
                rank["account_id"] = rankinfo["account_id"]
                rank["score"] = rankinfo["score"]
                if db.selectJsonDataCount( rank, "rankings") == 0:
                    db.deleteJsonData( rank, "rankings")
                    db.insertJsonData( rank, "rankings")

                player = {}
                for prop in rankinfo:
                    if prop in DBprop:
                        player[prop] = rankinfo[prop]

                if db.selectJsonDataCount( player, "players") == 0:
                    db.deleteJsonData( player, "players")
                    db.insertJsonData( player, "players")
        return

    def getPublicMatches(self):
        db = Database()
        
        matches = self.getJSON(self.API_URL + "publicMatches" + self.API_KEY)

        DBprop = ["match_id", "match_seq_num", "radiant_win", "start_time", "duration", "avg_mmr", "num_mmr", "lobby_type", "game_mode", "avg_rank_tier", "num_rank_tier", "cluster"]

        
        for match in matches:
            info = {}
            for prop in match:
                if prop in DBprop:
                    info[prop] = match[prop]
            if db.selectJsonDataCount( info, "public_matches") == 0:
                db.insertJsonData( info, "public_matches")

            
        return


def main():
    e = Entity()
    e.getPublicMatches()
    return


if __name__ == '__main__':
    main()
