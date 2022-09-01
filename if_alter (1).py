from collections import namedtuple
base_url: str = "https://biggeek.ru/"

UrlPath = namedtuple("UrlPath", ["path", "desc"])

url_paths: dict[str, UrlPath] = {
    '5': UrlPath("catalog/smartfony", "Смартфоны"),
    '6': UrlPath("catalog/aksessuary", "Аксессуары"),
    '7': UrlPath("catalog/akusticheskie-sistemi", "Акустические Системы"),
    '8': UrlPath("catalog/dlya-avto", "Для Авто"),
    # ...
}


def parser(url_path: str) -> None:
    print(f"Parsed data from: {base_url + url_path}")


def main() -> None:
    while True:
        print("Categories:")
        print('\n '.join(f'{key}: {url_paths[key].desc}' for key in url_paths))
        choice: str = input("What to parse?: ")
        if choice.lower() == "q":
            print("Bye!")
            return
        if choice in url_paths:
            parser(url_paths[choice].path)
        else:
            print("Wrong choice")


if __name__ == '__main__':
    main()
