from brownie import Factory, accounts, Router, MockToken, LZEndpointMock, Bridge, StargateToken, LPStaking, StargateFeeLibraryV01, StargateFeeLibraryV02
import scripts.config as config

def main():
    RouterContract = Router.deploy({"from": accounts[0]})
    MockTokenContract = MockToken.deploy("Token", "TKN", {"from": accounts[0]})
    LZEndpointMockContract = LZEndpointMock.deploy(1, {"from": accounts[0]})  # change chain id
    Bridge.deploy(LZEndpointMockContract.address, RouterContract.address, {"from": accounts[0]})
    FactoryContract = Factory.deploy(RouterContract.address, {"from": accounts[0]})
    # FactoryContract = Factory.deploy("0xDB42997ba31a0035f75808D6e18a56c82b5B73bc", {"from": accounts[0]}, publish_source=True)
    StargateTokenContract = StargateToken.deploy(
        config.stargateConfig["stargateToken"]["name"], 
        config.stargateConfig["stargateToken"]["symbol"], 
        LZEndpointMockContract.address, 
        config.stargateConfig["stargateToken"]["mainEndpointId"], 
        config.stargateConfig["stargateToken"]["initialSupplyMainEndpoint"], 
        {"from": accounts[0]}
    )
    LPStaking.deploy(StargateTokenContract.address, 261078307883562000, 13326790, 13326790, {"from": accounts[0]})
    StargateFeeLibraryV01Contract = StargateFeeLibraryV01.deploy(FactoryContract.address, {"from": accounts[0]})
    StargateFeeLibraryV02Contract = StargateFeeLibraryV02.deploy(FactoryContract.address, {"from": accounts[0]})
    FactoryContract.setDefaultFeeLibrary(StargateFeeLibraryV02Contract.address)
    # FactoryContract = Contract.from_explorer("0xB1F8C31e29ebB9eEe389320CE5C7f85b5E83686A")
    # FactoryContract.setDefaultFeeLibrary("0x8ED960db65287c76C2fE34184F57b3a154D88bcf", {"from": accounts[0]})

    print("finished")