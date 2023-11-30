class Vehicle:
    """
    Class to make vehicle and determine car type

    Parametres:
        registration (string):  The registration number on the cars license plate
        model (string):         The brand of the car
        owner (string):         Name of the registered owner
        year (int):             Production year
        type (string):          Fuel usage
    """

    def __init__(self, registration, model, year, owner):
        # Constructor that recieves and uses parameters
        self.registration   = registration
        self.model          = model
        self.owner          = owner
        self.year           = int(year)
        self.type           = self.determine_type()

    def determine_type(self):
        # Method for determining fuel type by license plate
        if self.registration[0] == "E":
            return "Electric"
        elif self.registration[0] == "D":
            return "Diesel"
        else:
            return "Petrol"


class Date:
    """
    Class for making date

    Parameters:
        date (str): The date the car passed

    Attributes:
        year (str): The year as it was in the date parameter
        month (str): The month as it was in the date parameter
        day (str): The day as it was in the date parameter
        hours (str): Array with all 24 hours to keep track of passages during said hours
    """
    def __init__(self, date):
        self.date = date
        self.year = self.date[:4]
        self.month = self.date[4:6]
        self.day = self.date[6:8]
        self.hours = [[] for _ in range(24)]


class TollBooth:
    """
    Class for 
    """
    def __init__(self):
        self.vehicles = []
        self.dates = []

    def read_data(self, data):
        self.vehicles = []
        self.dates = []
        with open(data, "r") as file:
            lines = file.readlines()
            for line in lines:
                entries = line.strip().split("/n")
                for entry in entries:
                    units = entry.split(";")
                    for unit in units:
                        values = unit.split(",")
                        if len(values) == 4:
                            self.vehicles.append(
                                Vehicle(values[0], values[1], values[2], values[3])
                            )
                        if len(values) == 3:
                            if not any(date.date == values[0] for date in self.dates):
                                self.dates.append(Date(values[0]))
                            next(
                                date for date in self.dates if date.date == values[0]
                            ).hours[int(values[1])].append(values[2])
            self.dates = sorted(self.dates, key=lambda date: date.date)

            for date in self.dates:
                for i, hour in enumerate(date.hours):
                    date.hours[i] = [
                        next(
                            (
                                vehicle
                                for vehicle in self.vehicles
                                if vehicle.registration == car
                            ),
                            None,
                        )
                        for car in hour
                    ]

    def find_busy_day(self):
        u = 0
        busy_day = None
        for date in self.dates:
            i = 0
            for hour in date.hours:
                for vehicle in hour:
                    i += 1
            if i > u:
                u = i
                busy_day = date
        return busy_day, u
    
    def find_busy_hour(self):
        u = 0
        busy_hour = None
        for h in range(24):
            i = 0
            for date in self.dates:
                for vehicle in date.hours[h]:
                    i += 1
            if i > u:
                u = i
                busy_hour = h
        return busy_hour, u
    
    def find_busy_car(self):
        u = 0
        busy_car = None

        for vehicle in self.vehicles:
            i = 0
            for date in self.dates:
                for hour in date.hours:
                    for passing in hour:
                        if vehicle == passing:
                            i += 1
            if i > u:
                u = i
                busy_car = vehicle
        return busy_car, u
            
                

    def print(self):
        for date in self.dates:
            print(date.hours)


bb = TollBooth()

bb.read_data("trond.txt")
print(bb.dates[0].hours[5][1].owner)
busy_day, i = bb.find_busy_day()
print(
    f"The {busy_day.day}th of {busy_day.month} in {busy_day.year} was hella busy with {i} passings!!!"
)

busy_hour, u = bb.find_busy_hour()
print(f"Hour {busy_hour} of the day was hella busy with {u} passings !!!")

busy_car, y = bb.find_busy_car()
print(f"{busy_car.owner}'s vehicle {busy_car.model}, is the hella busy car with {y} passings !!!")
