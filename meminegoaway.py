class Vehicle:
    def __init__(self, registration, model, year, owner):
        self.registration   = registration
        self.model          = model
        self.owner          = owner
        self.year           = int(year)
        self.type           = self.determine_type()

    def determine_type(self):
        if self.registration[0] == "E":
            return "Electric"
        elif self.registration[0] == "D":
            return "Diesel"
        else:
            return "Petrol"


class Date:
    def __init__(self, date):
        self.date = date
        self.year = self.date[:4]
        self.month = self.date[4:6]
        self.day = self.date[6:8]
        self.hours = [[] for _ in range(24)]


class TollBooth:
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
        day = None
        hour = None

        for date in self.dates:
            for hour in date.hours

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
