from brownie import Factory, accounts, Router, MockToken, LZEndpointMock, Bridge, StargateToken, LPStaking, StargateFeeLibraryV01, StargateFeeLibraryV02, Pool, web3
import scripts.config as config
def main():
    LpStakingContract = LPStaking.deploy(
        stargateTokencontract,
        8368893,
        8368893,
        {"from": accounts.load("0")}
    )