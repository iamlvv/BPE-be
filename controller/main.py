from .utils import *


@bpsky.route("/api/v1/", methods=["GET"])
def main():
    return "Welcome to BPSky"
