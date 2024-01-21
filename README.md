# Sensor Tech lab
This Python codebase is designed to parse and convert raw data from a variety of temperature sensors into meaningful temperature values. It is tailored for a contact temperature measurement setup that employs the following sensors interfaced with a microcontroller's (STM32F407_DISCO) GPIOs:

- RTD sensor Ni1000SOT
- NTC thermistor
- NTC thermistor with MAX6682MUA integrated circuit
- K-type thermocouple 80PK-1 with MAX6675ISA integrated circuit
- DS18B20 semiconductor sensor
- LM35DZ semiconductor sensor
- TMP101NA semiconductor sensor
  
## Features
- Data Conversion: Converts raw sensor data into decimal temperature values.
- Time Point Extraction: Retrieves temperature data at specific percentages (20%, 40%, 60%, 80%) of the total measurement time.
- Data Visualization: Plots temperature data for all sensors to compare their readings visually.
- Averaging Techniques: Implements average calculation in groups of 10 and rolling averages for smoothing the data.
- Flexible Data Handling: Includes functionality to work with each sensor individually, accommodating different data formats and conversion methods.

## Visualization
The code provides matplotlib plots to visualize the temperature readings from each sensor, as well as the average and rolling average calculations. This helps in understanding the behavior of each sensor over time and under different conditions.
