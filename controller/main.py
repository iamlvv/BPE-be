from .utils import *


@bpsky.route("/", methods=["GET"])
def main():
    return "Welcome to BPSky"
