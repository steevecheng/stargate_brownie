from brownie import Router, accounts


def main():
    return Router.deploy({"from": accounts.load("0")})