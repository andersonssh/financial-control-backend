import pendulum


def get_now():
    return pendulum.now().to_datetime_string()


if __name__ == "__main__":
    print(get_now())
