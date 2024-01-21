import csv
import math
from statistics import mean
import pandas as pd
from colorama import Fore


def parse_data(csv_name):
    with open(csv_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        # First row contains the raw data
        parsed_data = next(reader, None)
    return parsed_data


def group_by_10_avg(sensor_temps: list[int]):
    ret_val = []
    j = 0
    cnt = 0

    for i in range(10, len(sensor_temps) + 1, 10):
        k = sensor_temps[j:i]
        v = round(mean(k), 2)
        ret_val.append(v)
        j += 10
        cnt += 1
    return ret_val


def group_by_10_roll_avg(sensor_temps: list[int]):
    window_size = 10

    roll_averages = [round(sum(sensor_temps[i:i + window_size]) / window_size, 2) for i in
                     range(len(sensor_temps) - window_size + 1)]
    return roll_averages


def extract_4_time_points(sensor_temps: list[list[float]], divisor: int):
    t_20 = math.floor(340 * 0.2 / divisor)
    t_40 = math.floor(340 * 0.4 / divisor)
    t_60 = math.floor(340 * 0.6 / divisor)
    t_80 = math.floor(340 * 0.8 / divisor)

    ret_val = []
    for st in sensor_temps:
        ret_val.append([st[t_20], st[t_40], st[t_60], st[t_80]])
    return ret_val


def display_table(data: list[list[float]]):
    sensors = ["Ni1000SOT", "NTC", "NTC+MAX6682", "TERMOPAR+MAX6675", "DS18B20",
               "LM35DZ", "TMP101NA"]

    # Create a DataFrame with an additional column for the percentages
    df = pd.DataFrame(data, columns=["20%", "40%", "60%", "80%"])
    df.index = sensors

    # Display the DataFrame as a table
    df.style.set_table_styles([{
        'selector': 'th',
        'props': [('font-size', '12pt')]
    }], overwrite=False).set_caption("Temperature Readings")
    print(Fore.BLUE, df)
