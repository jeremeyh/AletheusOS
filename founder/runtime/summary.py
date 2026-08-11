from timeline.storage.store import store


def summary():

    timeline = store.load()

    print()

    print("Founder Timeline Summary")

    print("=" * 40)

    print("Events:", len(timeline))

    if timeline:
        print()

        print("Latest:")

        print(timeline[-1]["event"])
