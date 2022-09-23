from config import Config
from parser import Parser
from savers.SaverWrapper import SaverWrapper


def main() -> None:
    config = Config.load_json("config.json")
    saver = SaverWrapper(config.saver)
    parser = Parser(saver.last_check())
    headers = saver.save_headers(parser.parse_headers(config.url))
    choice = input("What you want to parse?: ")
    if choice == "all":
        for header in headers:
            saver.save(list(parser.parse_category(config.url + header.name, header.name)))


if __name__ == '__main__':
    main()
