class Util:
    @staticmethod
    def readFile(filepath):
        with open(filepath, "r") as f:
            print(f.readline())