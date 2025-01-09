import csv


def tsv_data(filename):
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            data = ", ".join(row).split("\t")
            yield data


def get_uids():
    uids = []

    for data in tsv_data("./data/characters.tsv"):
        if data[0] != "#uid":
            uids.append(data[0])

    return uids


def get_uids_by_house(house):
    uids = []

    for data in tsv_data("./data/houses.tsv"):
        if data[1] == house:
            uids.append(data[0])

    return uids


def get_characters_by_uids(uids):
    characters = {}

    for data in tsv_data("./data/characters.tsv"):
        if data[0] in uids:
            characters[data[0]] = {"name": data[1], "gender": data[3]}

    return characters


def get_sids_by_uids(uids):
    sids = {uid: [] for uid in uids}

    for data in tsv_data("./data/scenes_characters.tsv"):
        uid = data[1]
        if uid in uids:
            sid = data[0]
            sids[uid].append(sid)

    return sids


def get_scenes_by_sids(sids):
    scenes = {sid: {} for sid in sids}

    for data in tsv_data("./data/scenes.tsv"):
        sid = data[0]
        if sid in sids:
            scenes[sid] = {
                "eid": data[1],
                "t_start": data[3],
                "t_end": data[4],
                "duration": int(data[5]),
            }

    return scenes


def get_scenes_by_uids(uids):
    scenes = {uid: {} for uid in uids}
    sids = get_sids_by_uids(uids)

    for uid, sids_ in sids.items():
        scenes[uid] = get_scenes_by_sids(sids_)

    return scenes


def get_screentime_per_episode_by_uids(uids):
    result = {uid: {} for uid in uids}
    scenes_by_uid = get_scenes_by_uids(uids)

    for uid, scenes in scenes_by_uid.items():
        for sid, scene in scenes.items():
            eid = scene["eid"]

            if eid not in result[uid]:
                result[uid][eid] = 0

            duration = scene["duration"]

            result[uid][eid] += duration

    return result


def get_total_screentime_by_scenes(scenes):
    return sum([s["duration"] for s in scenes.values()])


def get_screentime_info(uids):
    c_info = get_characters_by_uids(uids)
    s_info = get_scenes_by_uids(uids)

    st_info = {uid: {} for uid in uids}

    for uid in uids:

        total_st = get_total_screentime_by_scenes(s_info[uid])

        st_info[uid] = c_info[uid] | {"screentime": total_st, "sids": ", ".join(s_info[uid].keys())}

    return st_info


def get_screentime_by_house(house):
    uids = get_uids_by_house(house)
    return get_screentime_info(uids)


def get_screentime_per_episode_by_house(house):
    uids = get_uids_by_house(house)
    return get_screentime_per_episode_by_uids(uids)


def write_screentime_info_to_tsv(info):
    with open("st_info.csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        titles = list(info[list(info.keys())[0]].keys())
        writer.writerow(["uid"] + titles)

        rows = [[uid] + list(i.values()) for uid, i in info.items()]
        writer.writerows(rows)


def write_screentime_per_episode(info):
    with open("st_p_episode_.tsv", "w") as tsvfile:
        writer = csv.writer(tsvfile, delimiter="\t")
        titles = ["uid", "eid", "duration"]
        writer.writerow(titles)

        for uid, episodes in info.items():
            for eid, duration in episodes.items():
                writer.writerow([uid, eid, duration])


if __name__ == "__main__":
    pass
    # info = get_screentime_per_episode_by_house("Targaryen")
    # info = get_screentime_info(get_uids())
    # write_screentime_per_episode(info)

    st_info = get_screentime_info(get_uids())
    write_screentime_info_to_tsv(st_info)
