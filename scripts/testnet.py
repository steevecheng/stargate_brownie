from brownie import Factory, accounts, Router, MockToken, LZEndpointMock, Bridge, StargateToken, LPStaking, StargateFeeLibraryV01, StargateFeeLibraryV02, Pool, web3
import scripts.config as config

def main():
    stgpb = 1261078307883562000
    startBlock = 8304253
    chainId = 1
    RouterContract = Router.deploy({"from": accounts.load("0")})
    MockUSDCContract = MockToken.deploy("Mock USDC", "USDC", {"from": accounts.load("0")})
    MockUSDTContract = MockToken.deploy("Mock USDT", "USDT", {"from": accounts.load("0")})
    # chage chain id
    LZEndpointMockContract = LZEndpointMock.deploy(chainId, {"from": accounts.load("0")})
    BridgeContract = Bridge.deploy(
        LZEndpointMockContract.address, 
        RouterContract.address, 
        {"from": accounts.load("0")}
    )
    FactoryContract = Factory.deploy(
        RouterContract.address, 
        {"from": accounts.load("0")}
    )
    StargateTokenContract = StargateToken.deploy(
        config.stargateConfig["stargateToken"]["name"], 
        config.stargateConfig["stargateToken"]["symbol"], 
        LZEndpointMockContract.address, 
        config.stargateConfig["stargateToken"]["mainEndpointId"], 
        config.stargateConfig["stargateToken"]["initialSupplyMainEndpoint"], 
        {"from": accounts.load("0")}
    )
    LPStakingContract = LPStaking.deploy(
        StargateTokenContract.address, 
        stgpb, 
        startBlock, 
        startBlock, 
        {"from": accounts.load("0")}
    )
    # StargateFeeLibraryV01Contract = StargateFeeLibraryV01.deploy(
    #     FactoryContract.address, 
    #     {"from": accounts.load("0")}
    # )
    StargateFeeLibraryV02Contract = StargateFeeLibraryV02.deploy(
        FactoryContract.address, 
        {"from": accounts.load("0")}
    )

    RouterContract.setBridgeAndFactory(BridgeContract.address, FactoryContract.address)
    
    FactoryContract.setDefaultFeeLibrary(StargateFeeLibraryV02Contract.address)
    RouterContract.createPool(
        config.pool["USDC"]["pid"], 
        MockUSDCContract.address, 
        config.pool["USDC"]["decimals"], 
        config.pool["USDC"]["decimals"], 
        "Stargate USDC", 
        "S*USDC"
    )
    RouterContract.createPool(
        config.pool["USDT"]["pid"], 
        MockUSDCContract.address, 
        config.pool["USDT"]["decimals"], 
        config.pool["USDT"]["decimals"], 
        "Stargate USDT", 
        "S*USDT"
    )

    PoolUSDCContract = Pool.deploy(
        config.pool["USDC"]["pid"], 
        RouterContract.address, 
        MockUSDCContract.address, 
        config.pool["USDC"]["decimals"], 
        config.pool["USDC"]["decimals"], 
        StargateFeeLibraryV02Contract.address, 
        "Stargate USDC", 
        "S*USDC", 
        {"from": accounts.load("0")}
    )
    PoolUSDTContract = Pool.deploy(
        config.pool["USDT"]["pid"], 
        RouterContract.address, 
        MockUSDTContract.address, 
        config.pool["USDT"]["decimals"], 
        config.pool["USDT"]["decimals"], 
        StargateFeeLibraryV02Contract.address, 
        "Stargate USDT", 
        "S*USDT", 
        {"from": accounts.load("0")}
    )

    LPStakingContract.add(1, PoolUSDCContract.address)
    LPStakingContract.add(2, PoolUSDTContract.address)

    print("finished")
