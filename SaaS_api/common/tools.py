from faker import Faker

fk = Faker("zh_CN")


def generate_mobile():
    """生成随机手机号"""
    return fk.phone_number()


if __name__ == '__main__':
    print(generate_mobile())
