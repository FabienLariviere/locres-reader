from src.model import LocresFile


if __name__ == "__main__":
    locres = LocresFile("...\Content\Localization\Game\en\Game.locres")
    locres.unpack()
    locres.dump()
