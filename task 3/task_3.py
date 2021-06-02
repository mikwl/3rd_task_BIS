"""c)	For the third code task you should create UI tests for https://www.metric-conversions.org/ .
You have to create the following tests:
- Test for converting Celsius to Fahrenheit temperature;
- Test for converting meters to feet;
- Test for converting ounces to grams"""


def celsius_to_fahrenheit(celsius):
    fahrenheit = celsius * 9/5 + 32
    if celsius < -273.15:
        return "That's impossible"
    else:
        fahrenheit = celsius * 9/5+32
        return fahrenheit

print(f"{celsius_to_fahrenheit(50)} fahrenheit")

def meters_to_feet(meter):
    return meter * 3.2808

print(f"{meters_to_feet(5)} feets")

def ounces_to_grams(ounce):
    return round((ounce/.035274),3)

print(f"{ounces_to_grams(3)} grams")
