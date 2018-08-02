#!/usr/bin/env python
# encoding=utf-8

# 此脚本为补全heroes表中的英雄头像url，但是只有104个url

__author__ = 'Vietronic'
__date__ = '$2018-7-31$'

import json
from ..Database import Database

HERO_PATH = './config/heroes.json'

db = Database()

with open(HERO_PATH, 'r+') as f:
    heroes = json.load(f)
    f.close()

print(len(heroes))

for id in heroes:
    con = {"id":id}
    hero = {"img":  heroes[id]["img"]}
    db.updateJsonData(hero, con,"heroes")