# List of valid keys for the INI file
VALID_KEYS = [
    "Ready", "Guard", "Prone", "Walk", "FireUp", "FireProne", "Down", "Crawl", 
    "Up", "Idle1", "Idle2", "Die1", "Die2", "Die3", "Die4", "Die5", 
    "Fly", "Hover", "FireFly", "Tumble", "SecondaryFire", "SecondaryProne", 
    "Deploy", "Deployed", "DeployedFire", "DeployedIdle", "Undeploy", 
    "Paradrop", "Cheer", "Panic", "Shovel", "Carry", "AirDeathStart", 
    "AirDeathFalling", "AirDeathFinish", "Tread", "Swim", "WetAttack", 
    "WetIdle1", "WetIdle2", "WetDie1", "WetDie2", "Struggle"
]

SWIM_RELATED_KEYS = ["WetAttack", "WetIdle1", "WetIdle2", "WetDie1", "WetDie2"]
FLY_RELATED_KEYS = ["Hover", "FireFly", "Tumble", "AirDeathStart", "AirDeathFalling", "AirDeathFinish"]

def parse_ini_data(input_data):
    data = {}
    lines = input_data.split("\n")
    for line in lines:
        line = line.strip()
        if "=" in line:
            key, value = line.split("=", 1)
            if key.strip() in VALID_KEYS:
                data[key.strip()] = value.strip()
    return data

def handle_walk_related_keys(data, added_keys):
    if "Walk" in data:
        walk_values = data["Walk"].split(",")
        walk_value_str = f"{walk_values[0]},1,{walk_values[1]}"
        cheer_value_str = f"{walk_values[0]},{walk_values[1]},0,E"

        if "Ready" not in data and "Guard" not in data:
            data["Ready"] = walk_value_str
            data["Guard"] = walk_value_str
            added_keys.extend(["Ready", "Guard"])

        if "Up" not in data and "Down" not in data:
            data["Up"] = walk_value_str
            data["Down"] = walk_value_str
            added_keys.extend(["Up", "Down"])

        if "Struggle" not in data:
            data["Struggle"] = "0,6,0"
            added_keys.append("Struggle")

        if "Panic" not in data:
            data["Panic"] = data["Walk"]
            added_keys.append("Panic")

        if "Cheer" not in data:
            if "FireUp" in data:
                fireup_values = data["FireUp"].split(",")
                cheer_value_str = f"{fireup_values[0]},{fireup_values[1]},0,E"
            data["Cheer"] = cheer_value_str
            added_keys.append("Cheer")

        if "Crawl" not in data:
            data["Crawl"] = data["Walk"]
            added_keys.append("Crawl")

        if "Crawl" in data and "Prone" not in data:
            crawl_values = data["Crawl"].split(",")
            data["Prone"] = f"{crawl_values[0]},1,{crawl_values[1]}"
            added_keys.append("Prone")

    if "Ready" in data and "Guard" not in data:
        data["Guard"] = data["Ready"]
        added_keys.append("Guard")
    if "Guard" in data and "Ready" not in data:
        data["Ready"] = data["Guard"]
        added_keys.append("Ready")

    if "Up" in data and "Down" not in data:
        data["Down"] = data["Up"]
        added_keys.append("Down")
    if "Down" in data and "Up" not in data:
        data["Up"] = data["Down"]
        added_keys.append("Up")

def handle_crawl_prone(data, added_keys):
    if "Crawl" in data and "Prone" not in data:
        crawl_values = data["Crawl"].split(",")
        data["Prone"] = f"{crawl_values[0]},1,{crawl_values[1]}"
        added_keys.append("Prone")

def handle_fire_secondary_prone(data, added_keys):
    if "FireProne" not in data and "FireUp" in data:
        fireup_values = data["FireUp"].split(",")
        fireprone_value_str = f"{fireup_values[0]},1,{fireup_values[1]}"
        data["FireProne"] = fireprone_value_str
        added_keys.append("FireProne")

    if "SecondaryProne" not in data and "SecondaryFire" in data:
        values = data["SecondaryFire"].split(",")
        if len(values) > 1:
            values[1] = "1"
        data["SecondaryProne"] = ",".join(values)
        added_keys.append("SecondaryProne")

def handle_idle_keys(data, added_keys):
    if "Idle1" in data:
        idle1_values = data["Idle1"].split(",")
        data["Idle1"] = f"{idle1_values[0]},{idle1_values[1]},0,E"
    if "Idle2" not in data and "Idle1" in data:
        idle1_values = data["Idle1"].split(",")
        data["Idle2"] = f"{idle1_values[0]},{idle1_values[1]},0,W"
        added_keys.append("Idle2")

def handle_swim_related_keys(data, added_keys):
    if "Swim" in data:
        values = data["Swim"].split(",")
        for key in SWIM_RELATED_KEYS:
            if key not in data:
                if key in ["WetIdle1", "WetIdle2"]:
                    data[key] = f"{values[0]},{values[1]},0," + ("E" if key == "WetIdle1" else "W")
                elif key in ["WetDie1", "WetDie2"]:
                    data[key] = f"{values[0]},{values[1]},0"
                added_keys.append(key)
        if "Tread" not in data:
            data["Tread"] = data["Swim"]
            added_keys.append("Tread")
    else:
        for key in SWIM_RELATED_KEYS:
            data.pop(key, None)

def handle_fly_related_keys(data, added_keys):
    if "Fly" in data:
        fly_values = data["Fly"].split(",")
        for key in FLY_RELATED_KEYS:
            if key not in data:
                if key == "Tumble":
                    data[key] = f"{fly_values[0]},{fly_values[1]},0"
                else:
                    data[key] = data["Fly"]
                added_keys.append(key)
    else:
        for key in FLY_RELATED_KEYS:
            data.pop(key, None)

def handle_deploy_related_keys(data, added_keys):
    if "Deploy" in data:
        deploy_values = data["Deploy"].split(",")
        deploy_value_str = f"{deploy_values[0]},{deploy_values[1]},0"

        if "Deployed" not in data:
            deployed_first_value = int(deploy_values[0]) + int(deploy_values[1]) - 1
            data["Deployed"] = f"{deployed_first_value},1,0"
            added_keys.append("Deployed")

        if "DeployedFire" not in data:
            if "FireUp" in data:
                data["DeployedFire"] = data["FireUp"]
            else:
                data["DeployedFire"] = data["Deploy"]
            added_keys.append("DeployedFire")

        if "DeployedIdle" not in data:
            data["DeployedIdle"] = "0,0,0"
            added_keys.append("DeployedIdle")

        if "Undeploy" not in data:
            data["Undeploy"] = data["Deploy"]
            added_keys.append("Undeploy")

def handle_die_keys(data, added_keys):
    for key in VALID_KEYS:
        if key.startswith("Die") and key in data:
            values = data[key].split(",")
            if len(values) < 3:
                values.append("0")
            data[key] = ",".join(values)
    if "Die1" in data:
        die1_value = data["Die1"]
        for i in range(2, 6):
            die_key = f"Die{i}"
            if die_key not in data:
                data[die_key] = die1_value
                added_keys.append(die_key)

def ensure_formatting_consistency(data):
    for key, value in data.items():
        if key not in ["Idle1", "Idle2", "Die1", "Die2", "Die3", "Die4", "Die5"]:
            values = value.split(",")
            if len(values) == 2:
                values.append(values[1])
            data[key] = ",".join(values)

def process_ini_data(input_data):
    data = parse_ini_data(input_data)
    added_keys = []
    handle_walk_related_keys(data, added_keys)
    handle_crawl_prone(data, added_keys)
    handle_fire_secondary_prone(data, added_keys)
    handle_idle_keys(data, added_keys)
    handle_swim_related_keys(data, added_keys)
    handle_fly_related_keys(data, added_keys)
    handle_deploy_related_keys(data, added_keys)
    handle_die_keys(data, added_keys)
    ensure_formatting_consistency(data)

    output_lines = []
    for key in VALID_KEYS:
        if key == "; YR Only from here:":
            output_lines.append("; YR Only from here:\n")
        elif key in data:
            output_lines.append(f"{key}={data[key]}")

    return "\n".join(output_lines), added_keys