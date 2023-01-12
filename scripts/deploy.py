from brownie import MockToken, accounts


def main():
    return MockToken.deploy("Token", "TKN", {"from": accounts.load("0")})