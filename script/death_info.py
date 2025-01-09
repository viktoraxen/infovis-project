from screentime_info_by_house import *


def get_killer(uid):
    for data in tsv_data("./data/killers.tsv"):
        if data[0] == uid:
            return data[3]


def build_death_info():
    death_info = {}

    for data in tsv_data("./data/characters.tsv"):
        uid = data[0]

        if uid == "#uid":
            continue

        name = data[1]
        birth_year = data[5]
        death_year = data[7]

        try:
            lifespan = int(death_year) - int(birth_year)
        except ValueError:
            lifespan = "Unknown"

        death_details = data[8]
        killer = get_killer(uid)

        death_info[uid] = {
            "name": name,
            "birth_year": birth_year,
            "death_year": death_year,
            "lifespan": lifespan,
            "death_details": death_details,
            "killer": killer,
        }

    return death_info


def write_death_info():
    death_info = build_death_info()

    with open("death_info.tsv", "w") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(
            [
                "uid",
                "name",
                "birth_year",
                "death_year",
                "lifespan",
                "death_details",
                "killer",
            ]
        )

        for uid, info in death_info.items():
            writer.writerow([uid] + list(info.values()))


write_death_info()
