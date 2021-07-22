import random
import sys
from faker import Faker
from DMmain import db, Employee


def create_fake_users(n):
    """Generate fake users."""
    faker = Faker()
    for i in range(n):
        idsuffix = random.randint(1111,9999)
        idprefix = "HC"

        employee = Employee(name=faker.name(),
                    eID = idprefix + str(idsuffix),
                    dpt = faker.company(),
                    pos = faker.job())
        db.session.add(employee)
    db.session.commit()
    print(f'Added {n} fake users to the database.')


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('Pass the number of users you want to create as an argument.')
        sys.exit(1)
    create_fake_users(int(sys.argv[1]))
