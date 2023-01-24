from brownie import accounts, chain, web3, rpc, history, Factory, GmozToken, InmozToken, OmnichainFungibletoken, Pool, Router
import scripts.config as config

def main():
    stgpb = 261078307883562000
    startBlock = 17975405
    chainId = 6
    RouterContract = Router.deploy("0x8731d54E9D02c286767d56ac03e8037C07e01e98", {"from": accounts[0]})
    FactoryContract = Factory.deploy(RouterContract.address, {"from": accounts[0]})
    GmozTokenContract = GmozToken.deploy("G", "G", RouterContract.address, "0x8731d54E9D02c286767d56ac03e8037C07e01e98", 1, 1000, {"from": accounts[0]})
    InmozTokenContract = InmozToken.deploy("I", "I", "0x8731d54E9D02c286767d56ac03e8037C07e01e98", 1, 1000, {"from": accounts[0]})
    PoolContract1 = InmozToken.deploy("I", "I", "0x8731d54E9D02c286767d56ac03e8037C07e01e98", 1, 1000, {"from": accounts[0]})
    
    MockUSDCContract = MockToken.deploy("Mock USDC", "USDC", {"from": accounts[0]})
    MockUSDTContract = MockToken.deploy("Mock USDT", "USDT", {"from": accounts[0]})
    LZEndpointMockContract = LZEndpointMock.deploy(chainId, {"from": accounts[0]})  # change chain id
    BridgeContract = Bridge.deploy(
        LZEndpointMockContract.address, 
        RouterContract.address, 
        {"from": accounts[0]}
    )
    FactoryContract = Factory.deploy(
        RouterContract.address, 
        {"from": accounts[0]}
    )
    # FactoryContract = Factory.deploy("0xDB42997ba31a0035f75808D6e18a56c82b5B73bc", {"from": accounts[0]}, publish_source=True)
    StargateTokenContract = StargateToken.deploy(
        config.stargateConfig["stargateToken"]["name"], 
        config.stargateConfig["stargateToken"]["symbol"], 
        LZEndpointMockContract.address, 
        config.stargateConfig["stargateToken"]["mainEndpointId"], 
        config.stargateConfig["stargateToken"]["initialSupplyMainEndpoint"], 
        {"from": accounts[0]}
    )

    LPStakingContract = LPStaking.deploy(
        StargateTokenContract.address, 
        stgpb, 
        startBlock, 
        startBlock, 
        {"from": accounts[0]}
    )
    StargateFeeLibraryV01Contract = StargateFeeLibraryV01.deploy(
        FactoryContract.address, 
        {"from": accounts[0]}
    )
    StargateFeeLibraryV02Contract = StargateFeeLibraryV02.deploy(
        FactoryContract.address, 
        {"from": accounts[0]}
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
        {"from": accounts[0]}
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
        {"from": accounts[0]}
    )

    LPStakingContract.add(1, PoolUSDCContract.address)
    LPStakingContract.add(1, PoolUSDTContract.address)

    print("finished")
