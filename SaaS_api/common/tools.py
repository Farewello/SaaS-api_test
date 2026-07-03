from faker import Faker

fk = Faker("zh_CN")

class Tools:
    def generate_mobile(self):
        return fk.phone_number()

if __name__ == '__main__':
    print(Tools().generate_mobile())