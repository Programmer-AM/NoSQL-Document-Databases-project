import csv
import glob

files = glob.glob('dataset-path')

def clean_status(status):
    status = status.split('. Released')
    return status[0]

def clean_gprs_or_edge(gprs):
    if gprs == 'Yes':
        return gprs
    else:
        return 'No'

def clean_dimensions_data(dimensions):
    dimensions = dimensions.split(' mm (')
    dimensions = dimensions[0].split(' x ')
    if len(dimensions) == 3 and (type(dimensions[0]) == int or float) \
            and (type(dimensions[1]) == int or float) \
            and (type(dimensions[2]) == int or float):
        return dimensions
    else:
        return list()

def clean_announce_data(announce):
    announce = announce.split(".")[0]
    try:
        year, month = announce.split(", ")
        if month == "January":
            month = 1
        elif month == "February":
            month = 2
        elif month == "March" or month == "Q1":
            month = 3
        elif month == "April":
            month = 4
        elif month == "May":
            month = 5
        elif month == "June" or month == "Q2":
            month = 6
        elif month == "July":
            month = 7
        elif month == "August":
            month = 8
        elif month == "September" or month == "Q3":
            month = 9
        elif month == "October":
            month = 10
        elif month == "November":
            month = 11
        elif month == "December" or month == "Q4":
            month = 12
        else:
            month = 1
        return year, month
    except:
        return -1, -1
def clean_os_data(os):
    os_splited = os.split(' ')

    if len(os_splited) >= 2:
        if os_splited[0] == "Android" or os_splited[0] == "iOS":
            if (type(os_splited[1]) == int or float):
                version = os_splited[1].split(',')[0]
                return os_splited[0], version

    return os

def clean_internal_data(internal):
    internal = internal.split(", ")[0]
    internal = internal.split("GB ")
    if len(internal) >= 2:
        return internal[0], internal[1]
    else:
        return -1, -1

def clean_loundspeaker(loundspeaker):
    if "stereo" in loundspeaker:
        return "stereo"
    elif "dual speakers" in loundspeaker:
        return "dual speakers"
    else:
        return loundspeaker

def clean_usb_data(usb):
    if "Type-C" in usb:
        return "Type-C"
    elif "microUSB" in usb:
        return "microUSB"
    elif "miniUSB" in usb:
        return "miniUSB"
    else:
        return usb

def check_empty(data):
    if data == "":
        return -1
    else:
        return data


def is_number(str):
    try:
        x = float(str)
        return True
    except:
        return False


def is_empty(str):
    if str in (None, ""):
        return True
    return False


def clean_weight(weight):
    weight_val = weight.split(" g")[0]
    weight_val.strip()

    if not is_number(weight_val):
        return -1

    return weight_val


def clean_sim(str):
    sim = str.split(" SIM")[0]
    if is_empty(sim):
        return -1

    return sim


def clean_size(str):
    size = str.split(" inches")[0]
    if is_empty(size):
        return -1
    return size


def clean_resolution(str):
    """magicna funkcija"""

    if 'chars' in str:
        return -1, -1, -1

    if 'lines' in str:
        tmp = str.split(" pixels")[0]
        if 'lines' in tmp:
            return -1, -1, -1
        return tmp, -1, -1

    if 'inch' in str:
        return str.split(" pixels")[0], -1, -1

    if 'ratio' not in str:
        return str.split(" pixels")[0], -1, -1

    if 'ppi' not in str:
        tmp = str.split(" pixels, ")
        return tmp[0], tmp[1].split(' ratio')[0], -1

    tmp = str.split(" pixels, ")
    resolution, ratio, ppi = "", "", ""

    try:
        resolution = tmp[0]
        tmp1 = tmp[1].split(" ratio (~")
        ratio = tmp1[0]
        ppi = tmp1[1].split(" ppi")[0]
    except:
        pass

    if is_empty(resolution):
        resolution = -1
    if is_empty(ratio):
        ratio = -1
    if is_empty(ppi):
        ppi = -1

    return resolution, ratio, ppi


def clean_camera(str):
    camera = str.split(' MP')[0]
    if not is_number(camera):
        camera = "VGA"

    return camera


def clean_sensors(str):
    if is_empty(str):
        return []

    if 'Yes' in str:
        return ['Accelerometer']

    return str.split(', ')


def clean_colors(str):
    if is_empty(str) or any(chr.isdigit() for chr in str):
        return ['Black']

    return str.split(", ")


def clean_features(str):
    if is_empty(str):
        return -1

    return str.split(", ")


phones = list()
for file in files:
    print(file)
    with open(file, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                if row['Model Name'] in (None, ""):
                    continue
                phone = {}
                phone['brand'] = check_empty(row['Brand'])
                phone['model_name'] = check_empty(row['Model Name'])
                phone['status'] = check_empty(clean_status(row['Status']))
                phone['gprs'] = check_empty(clean_gprs_or_edge(row['GPRS']))
                phone['edge'] = check_empty(clean_gprs_or_edge(row['EDGE']))

                # Dimensions
                dimensions = clean_dimensions_data(row['Dimensions'])
                if len(dimensions) == 3:
                    phone['height'] = check_empty(dimensions[0])
                    phone['width'] = check_empty(dimensions[1])
                    phone['thickness'] = check_empty(dimensions[2])
                else:
                    phone['height'] = -1
                    phone['width'] = -1
                    phone['thickness'] = -1

                # Announced
                year, month = clean_announce_data(row["Announced"])
                phone["announced_year"] = check_empty(year)
                phone["announced_month"] = check_empty(month)

                # OS
                os_cleaned_data = clean_os_data(row['OS'])
                if len(os_cleaned_data) == 2:
                    phone['os'] = check_empty(os_cleaned_data[0])
                    phone['version'] = check_empty(os_cleaned_data[1])
                else:
                    phone['os'] = check_empty(os_cleaned_data)
                    phone['version'] = -1

                # Chipset
                phone['chipset'] = check_empty(row['Chipset'])

                # CPU
                phone['cpu'] = check_empty(row['CPU'])

                # Card slot
                phone['card_slot'] = check_empty(row['Card slot'])

                # Internal
                if "MB" in row['Internal']:
                    continue
                storage, ram = clean_internal_data(row['Internal'])
                phone['storage_gb'] = check_empty(storage)
                phone['ram_gb'] = check_empty(ram)

                # video
                phone['video'] = check_empty(row['Video'])

                # Loudspeaker
                phone['loudspeaker'] = check_empty(clean_loundspeaker(row['Loudspeaker']))

                # 3.5mm jack
                phone["jack_3.5mm"] = check_empty(row['3.5mm jack'])

                # WLAN
                phone['wlan'] = check_empty(row['WLAN'])

                # Bluetooth
                phone['bluetooth'] = check_empty(row['Bluetooth'])

                # GPS
                phone['gps'] = check_empty(row['GPS'])

                # USB
                phone['usb'] = check_empty(clean_usb_data(row['USB']))

                # Type_1 - Battery
                phone['battery'] = check_empty(row['Type_1'])

                # Charging
                phone['charging'] = check_empty(row['Charging'])

                # Protection
                phone['protection'] = check_empty(row['Protection'])

                phone['weight'] = clean_weight(row['Weight'])
                phone['sim'] = clean_sim(row['SIM'])
                phone['screen_type'] = row['Type']
                phone['size'] = clean_size(row['Size'])
                phone['resolution'], phone['ratio'], phone['ppi'] = clean_resolution(row['Resolution'])
                phone['camera'] = clean_camera(row['Single'])
                phone['sensors'] = clean_sensors(row['Sensors'])
                phone['colors'] = clean_colors(row['Colors'])
                phone['features'] = clean_features(row['Features'])
                phone['image'] = clean_features(row['Model Image'])
                #print(phone)
                phones.append(phone)
            except:
                continue

#print(phones)

with open('Phones_tab_separated.tsv', 'w') as output_file:
    brojac = 0
    fieldnames = phones[0].keys()
    fieldnames_list = list()
    for fieldname in fieldnames:
        fieldnames_list.append(fieldname)
    print(fieldnames_list)
    writer = csv.DictWriter(output_file, delimiter='\t', fieldnames=fieldnames_list, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()

    for phone in phones:
        try:
            writer.writerow(phone)
        except:
            brojac +=1
            continue
    print(brojac)