import datetime
import random
import string

class Szoba:
    def __init__(self, ar):
        self.ar = ar

    def get_ar(self):
        return self.ar


class EgyagyasSzoba(Szoba):
    def __init__(self):
        super().__init__(8000)


class KetagyasSzoba(Szoba):
    def __init__(self):
        super().__init__(10000)


class Foglalas:
    def __init__(self, szoba, datum_kiode, datum_kiode_ki):
        self.szoba = szoba
        self.datum_kiode = datum_kiode
        self.datum_kiode_ki = datum_kiode_ki
        self.id = generate_unique_id()

    def get_id(self):
        return self.id

    def get_datum_kiode(self):
        return self.datum_kiode

    def get_datum_kiode_ki(self):
        return self.datum_kiode_ki

    def get_szoba(self):
        return self.szoba

    def get_ar(self):
        arrival_date = datetime.date.fromisoformat(self.datum_kiode)
        departure_date = datetime.date.fromisoformat(self.datum_kiode_ki)
        nights_stayed = (departure_date - arrival_date).days + 1
        return self.szoba.get_ar() * nights_stayed

    def __str__(self):
        return f"Foglalás: {self.id}, {self.szoba.__class__.__name__}, {self.datum_kiode} - {self.datum_kiode_ki}, {self.get_ar()} Ft"


def generate_unique_id():
    import random
    import string
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters_and_digits) for i in range(8))
    return result_str


class Szalloda:
    def __init__(self, nev, szobak=None):
        self.nev = nev
        self.szobak = szobak if szobak else []
        self.foglalasok = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)
        self.foglalasok.append([])

    def get_szobak(self):
        return self.szobak

    def get_foglalasok(self):
        return self.foglalasok


class SzallodaKezeles:
    def __init__(self, szalloda):
        self.szalloda = szalloda
        self.foglalasok = []

    def foglalas(self, datum_kiode, datum_kiode_ki):
        today = datetime.date.today()
        arrival_date = datetime.date.fromisoformat(datum_kiode)
        departure_date = datetime.date.fromisoformat(datum_kiode_ki)

        if arrival_date < today:
            print("Hibás dátum! A befogadó dátuma nem lehet régebbi a mai naptól.")
            return False
        if departure_date < arrival_date:
            print("Hibás időintervallum! A kiadó dátuma nem lehet korábbi a befogadó dátumnál.")
            return False

        # Check if room is available
        if len(self.szalloda.get_szobak()) == 0:
            print("Nincs szabad szoba!")
            return False

        # Select a random room
        room_type = random.choice([EgyagyasSzoba, KetagyasSzoba])
        room = room_type()
        price_per_night = 8000 if isinstance(room, EgyagyasSzoba) else 10000
        nights_stayed = (departure_date - arrival_date).days + 1
        price = price_per_night * nights_stayed
        foglalas = Foglalas(room, datum_kiode, datum_kiode_ki)
        self.foglalasok.append(foglalas)
        print(f"Sikeres foglalás! Azonosító: {foglalas.get_id()}")
        print(f"ár: {foglalas.get_ar()} Ft")
        return True

    def lemond(self, foglalas_id):
        for i, foglalas in enumerate(self.foglalasok):
            if foglalas.get_id() == foglalas_id:
                del self.foglalasok[i]
                print("Sikeres lemondás!")
                return
        print("Nincs ilyen foglalás azonosítója.")

    def listazas(self):
        for i, foglalas in enumerate(self.foglalasok):
            print(f"{i+1}. Foglalás: {foglalas}")


# Main program
def main():
    today = datetime.date.today()
    szalloda = Szalloda("Szallas", [EgyagyasSzoba(), KetagyasSzoba()])
    kezeles = SzallodaKezeles(szalloda)

    # Initialize reservations
    for i in range(5):
        kezeles.foglalas(str(today + datetime.timedelta(days=random.randint(1, 30))), str(today + datetime.timedelta(days=random.randint(31, 60))))

    # Run program
    while True:
        print("1. Foglalás")
        print("2. Foglalás lemondása")
        print("3. Foglalás listázása")
        print("4. Kilépés")
        choice = input("Válasszon egy lehetőséget: ")

        if choice == "1":
            datum_kiode = input("Adja meg az érkezés dátumát (yyyy-mm-dd): ")
            datum_kiode_ki = input("Adja meg a távozás dátumát (yyyy-mm-dd): ")
            kezeles.foglalas(datum_kiode, datum_kiode_ki)
        elif choice == "2":
            foglalas_id = input("Adja meg a foglalás azonosítóját: ")
            kezeles.lemond(foglalas_id)
        elif choice == "3":
            kezeles.listazas()
        elif choice == "4":
            break
        else:
            print("Hibás válasz! Kérjük válasszon egyéb lehetőséget.")


if __name__ == "__main__":
    main()