import math


class Sensor:
    def __init__(self, raw_sensor_data):
        self.sensor_data = raw_sensor_data
        self.temps = []

    def convert_to_decimal(self):
        self.sensor_data = [round(int(x, 16), 2) for x in self.sensor_data]


class Ni1000SOT(Sensor):
    # U_NI is raw data from the sensor, V_CC is 5 V
    def convert_to_decimal(self):
        # Convert the hex values to integers (assuming they are little-endian)
        int_values = [int(x, 16) for x in self.sensor_data]

        # ADC details
        adc_resolution = 10  # 10-bit resolution
        adc_max_value = 2 ** adc_resolution - 1  # Maximum digital value for 10-bit ADC
        v_ref = 5.0  # Reference voltage of the ADC

        # Convert ADC digital values to analog voltages U_NI
        U_NI = [v_ref * value / adc_max_value for value in int_values]

        R1 = 2967
        R2 = 10000
        R3 = 3800
        R4 = 14880
        VCC = 5
        # Calculate R_NI for every output voltage U_NI and store it in a list
        R_NI = [(-R4 * R3 * R1 * VCC - R3 * R2 * R1 * x) / (R2 * (R3 * x - R4 * VCC - R3 * VCC)) for x in
                U_NI]

        a_apo = - 412.6
        b_apo = 140.41
        c_apo = 0.00764
        d_apo = - 6.25 * 10 ** -17
        e_apo = -1.25 * 10 ** -24
        # Convert every data point of R_NI to temp from the datasheet eq
        self.temps = [a_apo + b_apo * (1 + c_apo * x) ** 0.5 + d_apo * x ** 5 + e_apo * x ** 7 for x in R_NI]
        self.temps = [round(x / 2, 2) for x in self.temps]


class NTCThermistor(Sensor):
    def convert_to_decimal(self):
        R1 = 16000
        R2 = 25000
        VCC = 3.3
        B = 4280  # In Kelvins
        A = 5.8293 * 10 ** -3  # Nominal param of NTC thermistor at 25 deg C

        # Convert the hex values
        int_values = [int(x, 16) for x in self.sensor_data]

        adc_resolution = 10  # 10-bit resolution
        adc_max_value = 2 ** adc_resolution - 1  # Maximum digital value for 10-bit ADC
        v_ref = VCC  # Reference voltage of the ADC

        # Convert ADC digital values to analog voltage V_NTC
        V_NTC = [v_ref * value / adc_max_value for value in int_values]

        # Calculate R_NTC for every output voltage V_NTC and store it in a list
        R_NTC = [(R1 * R2 * (VCC - x)) / (R1 * x - R2 * (VCC - x)) for x in V_NTC]

        self.temps = [round((B / math.log(x / A)) - 273.15, 2) for x in R_NTC]


class NTCThermistorMAX6682(Sensor):
    def convert_to_decimal(self):
        # Convert the hex values to integers (assuming they are little-endian)
        D_OUT_values_11_bit = [int(x, 16) >> 5 for x in self.sensor_data]
        self.temps = [round(x * 0.125, 2) for x in D_OUT_values_11_bit]


class ThermoCoupleMAX6675(Sensor):
    def convert_to_decimal(self):
        D_OUT_values_12_bit = [(int(x, 16) >> 3) & 0xFFF for x in self.sensor_data]
        resolution = 0.25  # Resolution of MAX6675 in degrees per bit

        # Convert ADC digital values to temperature
        self.temps = [round(x * resolution, 2) for x in D_OUT_values_12_bit]


class DS18B20(Sensor):
    def convert_to_decimal(self):
        self.temps = [float(int(x, 16)) for x in self.sensor_data]


class LM35DZ(Sensor):
    def convert_to_decimal(self):
        int_values = [int(x, 16) for x in self.sensor_data]

        adc_resolution = 10  # 10-bit resolution
        adc_max_value = 2 ** adc_resolution - 1  # Maximum digital value for 10-bit ADC
        v_ref = 3.3  # Reference voltage of the ADC

        # Convert ADC digital values to analog voltages V_OUT
        V_OUT = [(v_ref * value) / adc_max_value for value in int_values]

        self.temps = [round(x / 0.01, 2) for x in V_OUT]


class TMP101NA(Sensor):
    def convert_to_decimal(self):
        int_values = [int(x, 16) for x in self.sensor_data]

        temperatures = []
        for value in int_values:
            # Extract bits T11 - T0
            raw_temp = value >> 4

            # Convert raw temperature to Celsius (one count is 0.0625°C)
            temperature = round(raw_temp * 0.0625, 2)
            temperatures.append(temperature)

        self.temps = temperatures
