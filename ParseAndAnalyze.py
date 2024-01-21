import Sensor
import HelperFunctions as hf
import matplotlib.pyplot as plt
from colorama import Fore, Style
import numpy as np

# 1.)   Convert raw data to temperature values for each sensor
Ni_1000_SOT = Sensor.Ni1000SOT(hf.parse_data('sensorData/Ni1000SOT.csv'))
Ni_1000_SOT.convert_to_decimal()

NTC = Sensor.NTCThermistor(hf.parse_data('sensorData/NTC.csv'))
NTC.convert_to_decimal()

NTC_MAX6682 = Sensor.NTCThermistorMAX6682(hf.parse_data('sensorData/NTC-MAX6682.csv'))
NTC_MAX6682.convert_to_decimal()

Thermocouple_MAX6675 = Sensor.ThermoCoupleMAX6675(hf.parse_data('sensorData/TERMOPAR-MAX6675.csv'))
Thermocouple_MAX6675.convert_to_decimal()

DS18B20 = Sensor.DS18B20(hf.parse_data('sensorData/DS18B20.csv'))
DS18B20.convert_to_decimal()

LM35DZ = Sensor.LM35DZ(hf.parse_data('sensorData/LM35DZ.csv'))
LM35DZ.convert_to_decimal()

TMP101NA = Sensor.TMP101NA(hf.parse_data('sensorData/TMP101NA.csv'))
TMP101NA.convert_to_decimal()

all_sensors = [Ni_1000_SOT, NTC, NTC_MAX6682, Thermocouple_MAX6675, DS18B20, LM35DZ, TMP101NA]

# 1.a)  Get the temperature at 20%, 40%, 60% and 80% of t_total
all_sensors_times = [[sensor.temps[int(340 * 0.2)], sensor.temps[int(340 * 0.4)], sensor.temps[int(340 * 0.6)],
                      sensor.temps[int(340 * 0.8)]] for sensor in all_sensors]
print(Fore.GREEN, Style.BRIGHT, "\n1.a) Temperatures of each sensor at 20%, 40%, 60% and 80% of t_total: ")
hf.display_table(all_sensors_times)

# 1.b)  Plot the temperature data of all 7 sensors
plt.figure(figsize=(10, 6))

for sensor in all_sensors:
    plt.plot(sensor.temps)

plt.title('Temperature Readings from 7 Sensors')
plt.xlabel('Measurement Number')
plt.ylabel('Temperature (°C)')
plt.legend(['Ni_1000_SOT', 'NTC', 'NTC_MAX6682', 'Thermocouple_MAX6675', 'DS18B20', 'LM35DZ', 'TMP101NA'])
plt.show()

# 2.)   Calculate avg in groups of 10 and get the temperature values at 20%, 40%, 60% and 80% of t_total
all_sensors_10_avg = [hf.group_by_10_avg(sensor.temps) for sensor in all_sensors]
all_sensors_10_avg_time_points = hf.extract_4_time_points(all_sensors_10_avg, 10)
print(Fore.GREEN, Style.BRIGHT, "\n2. Averages collected from groups of 10 at 20%, 40%, 60% and 80% of t_total: ")
hf.display_table(all_sensors_10_avg_time_points)

# 3.)   Calculate rolling avg in groups of 10 and get the temperature values at 20%, 40%, 60% and 80% of t_total
all_sensors_10_roll_avg = [hf.group_by_10_roll_avg(sensor.temps) for sensor in all_sensors]
all_sensors_10_roll_avg_time_points = hf.extract_4_time_points(all_sensors_10_roll_avg, 1)
print(Fore.GREEN, Style.BRIGHT, "\n3. Rolling averages collected from groups of 10 at 20%, 40%, 60% and 80% of "
                                "t_total: ")
hf.display_table(all_sensors_10_roll_avg_time_points)

# 5.)   Plot the original temp data against the data from the 2nd and 3rd question
plt.figure(figsize=(10, 6))
plt.plot(DS18B20.temps)
# Stretch out the averages because we have 34 data points, instead of 340
stretched_averages = np.repeat(all_sensors_10_avg[4], 10)
plt.plot(stretched_averages)
plt.plot(all_sensors_10_roll_avg[4])
plt.title('Temperature Readings from DS18B20')
plt.xlabel('Measurement Number')
plt.ylabel('Temperature (°C)')
plt.legend(['DS18B20 source temps', 'DS18B20 averages (stretched out)', 'DS18B20 rolling averages'])
plt.show()
