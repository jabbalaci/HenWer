#!/usr/bin/env python

import re
import os

site = 'http://fetish.iiichan.net/old/'       # site's address
name = 'One Thread, One Fetish (archive from 23-Jun-2008)'
referer = None

main_site = 'http://fetish.iiichan.net/'

archive = [
('http://fetish.iiichan.net/old/1211100560.html', '3D effect (18)'),
('http://fetish.iiichan.net/old/1212680740.html', 'Aeris (5)'),
('http://fetish.iiichan.net/old/1210531620.html', 'Arnie concentration (167)'),
('http://fetish.iiichan.net/old/1214212672.html', 'Bald and Partially Bald Women (2)'),
('http://fetish.iiichan.net/old/1173154411.html', 'Barefoot girls (20)'),
('http://fetish.iiichan.net/old/1211349197.html', 'BB Tribute (68)'),
('http://fetish.iiichan.net/old/1208647191.html', 'BBWs (31)'),
('http://fetish.iiichan.net/old/1186638038.html', 'Belly & navel (56)'),
('http://fetish.iiichan.net/old/1208306671.html', 'big clits (12)'),
('http://fetish.iiichan.net/old/1208465282.html', 'Big Nipples (11)'),
('http://fetish.iiichan.net/old/1213234573.html', 'Bloomers! (7)'),
('http://fetish.iiichan.net/old/1207240729.html', 'Bondage thread: Third Strike (1000)'),
('http://fetish.iiichan.net/old/1213241878.html', 'Bondage Thread: take 4 (64)'),
('http://fetish.iiichan.net/old/1182403995.html', 'Breast Expansion (126)'),
('http://fetish.iiichan.net/old/1206108718.html', 'CastityBelt (59)'),
('http://fetish.iiichan.net/old/1210732548.html', 'catched couples xD (6)'),
('http://fetish.iiichan.net/old/1212450690.html', 'Cheerleaders (7)'),
('http://fetish.iiichan.net/old/1205609629.html', 'Crucifixion (79)'),
('http://fetish.iiichan.net/old/1213157680.html', 'Cum bath (5)'),
('http://fetish.iiichan.net/old/1210136740.html', 'D-2 Tribute (330)'),
('http://fetish.iiichan.net/old/1200768532.html', 'Demoness/Succubus (96)'),
('http://fetish.iiichan.net/old/1207633852.html', 'Diapered Girls Episode 2 (269)'),
('http://fetish.iiichan.net/old/1213494522.html', 'Disgaea females----___>:( no futas or cocks allowed!!!!!! (11)'),
('http://fetish.iiichan.net/old/1212652898.html', 'Drinking urine/poop. (6)'),
('http://fetish.iiichan.net/old/1178683433.html', 'Eggs (60)'),
('http://fetish.iiichan.net/old/1210059664.html', 'Electroshock (49)'),
('http://fetish.iiichan.net/old/1207361831.html', 'Encasement (55)'),
('http://fetish.iiichan.net/old/1200917811.html', 'Enemas & anal insertions (125)'),
('http://fetish.iiichan.net/old/1211144321.html', 'Erika bondage thread (37)'),
('http://fetish.iiichan.net/old/1214256066.html', 'Face Stretching (9)'),
('http://fetish.iiichan.net/old/1212854558.html', 'Female Ejaculation (6)'),
('http://fetish.iiichan.net/old/1182451196.html', 'Femdom!!! (no pegging) (165)'),
('http://fetish.iiichan.net/old/1213725725.html', 'f/ inflation and expansion (7)'),
('http://fetish.iiichan.net/old/1206148226.html', 'First Blood! (242)'),
('http://fetish.iiichan.net/old/1190183423.html', 'Forced Feminization (165)'),
('http://fetish.iiichan.net/old/1208585654.html', 'Full body nudity, from the head to the toes (22)'),
('http://fetish.iiichan.net/old/1173152816.html', 'Fundoshi Girls (123)'),
('http://fetish.iiichan.net/old/1188406997.html', 'Funny stuff (169)'),
('http://fetish.iiichan.net/old/1211081693.html', 'Futa Wrestling (34)'),
('http://fetish.iiichan.net/old/1211616939.html', 'Gary Roberts (101)'),
('http://fetish.iiichan.net/old/1173374142.html', 'Giant Breasts (84)'),
('http://fetish.iiichan.net/old/1202510244.html', 'Giantess (56)'),
('http://fetish.iiichan.net/old/1174414527.html', 'Girls and weird machines (595)'),
('http://fetish.iiichan.net/old/1202030478.html', 'Girls on Sawhorses (149)'),
('http://fetish.iiichan.net/old/1209166242.html', 'Girls Pissing Themselves (160)'),
('http://fetish.iiichan.net/old/1213783867.html', 'Girls used as furniture (22)'),
('http://fetish.iiichan.net/old/1212995486.html', 'Glasses (14)'),
('http://fetish.iiichan.net/old/1203555714.html', 'Group/multiple girls (36)'),
('http://fetish.iiichan.net/old/1202839828.html', 'Gynoid, Robot, Cyborg, Mecha, Hardsuit Girls, etc... (176)'),
('http://fetish.iiichan.net/old/1214181806.html', 'Hairy Thread (13)'),
('http://fetish.iiichan.net/old/1190517218.html', 'Huge Futas (102)'),
('http://fetish.iiichan.net/old/1190957690.html', 'Human pet (262)'),
('http://fetish.iiichan.net/old/1210470858.html', 'Intresting date sim girls (4)'),
('http://fetish.iiichan.net/old/1207425520.html', 'Jenny/X-J9 (193)'),
('http://fetish.iiichan.net/old/1214069526.html', 'katara and starfire porn (2)'),
('http://fetish.iiichan.net/old/1213807712.html', 'Kemono Inukai Fanthread (42)'),
('http://fetish.iiichan.net/old/1211786842.html', 'Kokuyosya tribute (26)'),
('http://fetish.iiichan.net/old/1212993378.html', 'Krystal (144)'),
('http://fetish.iiichan.net/old/1211415581.html', 'Lesbian Bondage (44)'),
('http://fetish.iiichan.net/old/1182012232.html', 'Masks (270)'),
('http://fetish.iiichan.net/old/1189084855.html', 'Mind Control, Hypnosis and much much more (51)'),
('http://fetish.iiichan.net/old/1212654185.html', 'MOLDE CASE (18)'),
('http://fetish.iiichan.net/old/1184137536.html', 'momoyama (59)'),
('http://fetish.iiichan.net/old/1211428447.html', 'Monoglove (63)'),
('http://fetish.iiichan.net/old/1196986053.html', 'Monster Girls (72)'),
('http://fetish.iiichan.net/old/1211761396.html', 'More like this (peehole) (16)'),
('http://fetish.iiichan.net/old/1211844359.html', 'morpheus - any more? (1)'),
('http://fetish.iiichan.net/old/1211207760.html', 'Naisyobeya Tribute (103)'),
('http://fetish.iiichan.net/old/1210091096.html', 'No stimulation (13)'),
('http://fetish.iiichan.net/old/1173317540.html', 'NWS /azu/ (808)'),
('http://fetish.iiichan.net/old/1212192311.html', 'Onoe Network Tribute thread (7)'),
('http://fetish.iiichan.net/old/1173212724.html', 'Peeing (580)'),
('http://fetish.iiichan.net/old/1213713178.html', 'Phallic Overstuffing (1)'),
('http://fetish.iiichan.net/old/1208307445.html', 'Pierce, Tattoo, body-mod (40)'),
('http://fetish.iiichan.net/old/1211168593.html', 'Pokeporn~ (9)'),
('http://fetish.iiichan.net/old/1213633046.html', 'Pony Grils&Working Slaves (9)'),
('http://fetish.iiichan.net/old/1211350156.html', 'Rape -> Escape -> Revenge (6)'),
('http://fetish.iiichan.net/old/1210773368.html', 'Really tall girls, (Like, super tall or mini-gts) (15)'),
('http://fetish.iiichan.net/old/1204749572.html', 'Restrained and left to suffer with Vibrator/Dildo (194)'),
('http://fetish.iiichan.net/old/1210841225.html', 'Secret Agents (8)'),
('http://fetish.iiichan.net/old/1186720324.html', 'Self Bondage (361)'),
('http://fetish.iiichan.net/old/1209403406.html', 'Sexy Dolls (42)'),
('http://fetish.iiichan.net/old/1193691207.html', 'Slime Monsters (111)'),
('http://fetish.iiichan.net/old/1193090979.html', 'Spanking (161)'),
('http://fetish.iiichan.net/old/1211340661.html', 'Specific Futa (61)'),
('http://fetish.iiichan.net/old/1213657723.html', 'Still turning people into dolls (3)'),
('http://fetish.iiichan.net/old/1173365162.html', 'Stocks (152)'),
('http://fetish.iiichan.net/old/1174874011.html', 'STRAIGHTJACKETS REVOLUTION.... (^_^U he no idea for a more interesting name) (314)'),
('http://fetish.iiichan.net/old/1213249491.html', 'Taking care of sick girls (1)'),
('http://fetish.iiichan.net/old/1209354767.html', 'Tentacles (16)'),
('http://fetish.iiichan.net/old/1204158094.html', 'Tickle Tickle Tickle (66)'),
('http://fetish.iiichan.net/old/1182664716.html', 'Tight spandex clothing (485)'),
('http://fetish.iiichan.net/old/1209824342.html', 'Totoro front page works (6)'),
('http://fetish.iiichan.net/old/1178756616.html', 'Transformation? (239)'),
('http://fetish.iiichan.net/old/1213292829.html', 'Transgender (12)'),
('http://fetish.iiichan.net/old/1204342517.html', 'Transgender Captions (47)'),
('http://fetish.iiichan.net/old/1213974367.html', 'trapped and fucked (6)'),
('http://fetish.iiichan.net/old/1208414903.html', 'WAM (75)'),
('http://fetish.iiichan.net/old/1214106755.html', 'Whipped (1)'),
('http://fetish.iiichan.net/old/1213515366.html', 'X-ray / Egg fertilization / Impregnate! (6)'),
]

def get_result():
    #print archive

    li = ['MAIN PAGE']   # the list is initialized with the main page
    urls = [main_site]        # main page of the site
    for e in archive:
        #print link[0], "->", link[1]
        urls.append(e[0])
        li.append(e[1])
        # debug
        #get_relative_save_dir("fetish", e[1])
    # add main page to the end too
    li.append('MAIN PAGE')
    urls.append(main_site)

    return (li, urls)

def gather_gallery_list():
    #li = []     # list of galleries (names)
    #urls = []   # URLs of the galleries
    return get_result()

def get_referer():
    return referer

def get_relative_save_dir(part1, part2):
    part2 = part2.lower()
    result = re.search(r'(.*)\(.*\)', part2)
    if result:
        part2 = result.group(1)
    part2 = re.sub(r'&#\d+;', '', part2)
    part2 = re.sub(r'[ /]', '_', part2)
    part2 = re.sub(r'\W', '', part2)
    part2 = re.sub(r'_+', '_', part2)
    part2 = re.sub(r'^_+', '', re.sub(r'_+$', '', part2))
    path = os.path.join(part1.lower(), part2)
    #print ">>>", path
    return path

#############################################################################

if __name__ == "__main__":
    print gather_gallery_list()
