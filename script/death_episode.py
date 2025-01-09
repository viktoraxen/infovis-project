from screentime_info_by_house import *


def get_deaths_per_scene():
    deaths = {}

    for data in tsv_data("./data/scenes_characters.tsv"):
        sid = data[0]
        uid = data[1]
        died = data[3]

        if died == "true":
            if sid not in deaths:
                deaths[sid] = []

            deaths[sid].append(uid)

    return deaths


def scenes_per_episode():
    scenes = {}
    for data in tsv_data("./data/scenes.tsv"):
        sid = data[0]
        eid = data[1]

        if sid == "#sid":
            continue

        if eid not in scenes:
            scenes[eid] = []

        scenes[eid].append(sid)

    return scenes


def get_deaths_per_episode():
    deaths = get_deaths_per_scene()
    scenes = scenes_per_episode()
    deaths_per_episode = {}

    for eid, sids in scenes.items():
        deaths_per_episode[eid] = []

        for sid in sids:
            if sid in deaths:
                deaths_per_episode[eid] += deaths[sid]

    return deaths_per_episode


def write_deaths():
    deaths = get_deaths_per_episode()

    with open("deaths.tsv", "w") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["eid", "uids"])

        for uid, deaths in deaths.items():
            writer.writerow([uid, ", ".join(deaths)])


write_deaths()
