from brownie import Factory, accounts, Router, MockToken, LZEndpointMock, Bridge, StargateToken, LPStaking, StargateFeeLibraryV01, StargateFeeLibraryV02, Pool, web3
import scripts.config as config
def main():
    StargateTokenContract = StargateToken.deploy(
        config.stargateConfig["stargateToken"]["name"],
        config.stargateConfig["stargateToken"]["symbol"],
        config.testnetEndpoint["fuji"]["endpoint"],
        config.stargateConfig["stargateToken"]["mainEndpointId"],
        config.stargateConfig["stargateToken"]["initialSupplyMainEndpoint"],
        {"from": accounts.load("0")}
    )
    print(StargateTokenContract.address)