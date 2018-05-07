import json
import re

temp1 = json.load(open("data/data5780478585632429823.json","r"))
temp2 = json.load(open("data/data6413802006216303256.json","r"))
temp3 = json.load(open("data/data4055732929854859059.json","r"))


data = {}
for a in temp1["features"]:
    a1 = a["properties"]
    name = "_".join(a1["sa2_name16"].replace("-"," ").split())
    t = {}
    t["pop_den"] = a1["pop_dens_p_per_km2"]
    t["med_age"] = a1["mdn_age_usu_res_erp_30_june_p_yrs"]
    t["name"] = name
    t["main"] = a1["sa2_main16"]
    data[a1["sa2_main16"]] = t

for a in temp2["features"]:
    a1 = a["properties"]
    name = "_".join(a1["sa2_name16"].replace("-"," ").split())
    t = {}
    t["med_wek_inc"] = a1["median_tot_prsnl_inc_weekly"]
    data[a1["sa2_main16"]].update(t)

for a in temp3["features"]:
    a1 = a["properties"]
    name = "_".join(a1["sa2_name16"].replace("-"," ").split())
    t = {}
    tmp = a1["high_yr_schl_comp_yr_9_eq_p"]*9 + a1["high_yr_schl_comp_yr_10_eq_p"]*10+a1["high_yr_schl_comp_yr_11_eq_p"]*11 + \
              a1["high_yr_schl_comp_yr_12_eq_p"]*12 + \
              a1["high_yr_schl_comp_yr_8_belw_p"]*8
    if a1["tot_p"] == 0:
        tmp = 0
    else:
        tmp = tmp / a1["tot_p"]
    t["tot_p"] = a1["tot_p"]
    t["ave_edu_yea"] = tmp
    data[a1["sa2_main16"]].update(t)

aurin = data


with open("data/geo.json","r") as f:
    geo = json.load(f)

glist = []
gdict = {}
for g in geo["features"]:
    td = {}
    try:
        td["name"] = g["properties"]["SA2_NAME16"]
        td["main"] = g["properties"]["SA2_MAIN16"]
        td["cor"] = g["geometry"]["coordinates"]
        glist.append(td)
        gdict[td["main"]] = td
    except:
        pass

for a in aurin.values():
    a["cor"] = gdict[a["main"]]["cor"]
    if isinstance(a["cor"][0][0][0],float):
        a["cor"] = a["cor"][0]
    else:
        a["cor"] = a["cor"][0][0]
    
alist = []
for d in aurin.values():
    alist.append(d)
    
for a in alist:
    if not a["ave_edu_yea"] :
        a["ave_edu_yea"] = 0
    if not a["med_age"] :
        a["med_age"] = 0
    if not a["med_wek_inc"] :
        a["med_wek_inc"] = 0
    if not a["pop_den"] :
        a["pop_den"] = 0
    if not a["tot_p"] :
        a["tot_p"] = 0

edu = []
age = []
inc = []
den = []
tot = []
for a in alist:
    if a["ave_edu_yea"]>0:
        edu.append(a["ave_edu_yea"])
    if a["med_age"]>0:
        age.append(a["med_age"])
    if a["med_wek_inc"]>0:
        inc.append(a["med_wek_inc"])
    if a["pop_den"]>0:
        den.append(a["pop_den"])
    if a["tot_p"]>0:
        tot.append(a["tot_p"])

for a in alist:
    if a["ave_edu_yea"]> 0: 
        a["ave_edu_yea_c"] =  (a["ave_edu_yea"] - min(edu)) / (max(edu)-min(edu))
    else:
        a["ave_edu_yea_c"] = 0
        
    if a["med_age"]> 0: 
        a["med_age_c"] =  (a["med_age"] - min(age)) / (max(age)-min(age))
    else:
        a["med_age_c"] = 0
        
    if a["med_wek_inc"]> 0: 
        a["med_wek_inc_c"] = (a["med_wek_inc"] - min(inc)) / (max(inc)-min(inc))
    else:
        a["med_wek_inc_c"] =0
        
    if a["pop_den"]> 0: 
        a["pop_den_c"] = (a["pop_den"] - min(den)) / (max(den)-min(den))
    else:
        a["pop_den_c"] = 0
        
    if a["tot_p"]> 0: 
        a["tot_p_c"] = (a["tot_p"] - min(tot)) / (max(tot)-min(tot))
    else:
        a["tot_p_c"] = 0
        
with open("aurin.json","w") as f:
    json.dump(alist,f)