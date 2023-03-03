from brownie import Factory, accounts, Router, MockToken, LZEndpointMock, Bridge, StargateToken, LPStaking, StargateFeeLibraryV01, StargateFeeLibraryV02, Pool, web3, interface
import scripts.config as config
def main():
    
    stgPerBlock = 280000000000000000
    testnet = "mumbai"
    usdcToken = "0x742DfA5Aa70a8212857966D491D67B09Ce7D6ec7"
    usdtToken = "0x6Fc340be8e378c2fF56476409eF48dA9a3B781a0"
    sUsdcToken = "0xFC0fd6425c6FFE98e4eAe17443C10F5DdBDAAEC3"
    sUsdtToken = "0xf7a9E29651a697d28551466e14bc3158A8d2A5B1"
    routerAddress = "0x817436a076060D158204d955E5403b6Ed0A5fac0"

    stgReleaseAmount = 1000000000000000000000000

    currentBlock = web3.eth.blockNumber
    startBlock = currentBlock + 20
    print(currentBlock, startBlock)
    
    StargateTokenContract = StargateToken.deploy(
        config.stargateConfig["stargateToken"]["name"],
        config.stargateConfig["stargateToken"]["symbol"],
        config.testnetEndpoint[testnet]["endpoint"],
        config.stargateConfig["stargateToken"]["mainEndpointId"],
        config.stargateConfig["stargateToken"]["initialSupplyMainEndpoint"],
        {"from": accounts.load("0")}
    )

    LpStakingContract = LPStaking.deploy(
        StargateTokenContract.address,
        stgPerBlock,
        startBlock,
        startBlock,
        {"from": accounts.load("0")}
    )
    print(LpStakingContract.address)
    # stg  = interface.IERC20(StargateTokenContract.address)
    StargateTokenContract.transfer(LpStakingContract.address, stgReleaseAmount, {"from": accounts.load("0")})


    # add Liquidity
    router = interface.IStargateRouter(routerAddress)

    # get 10 s*usdc
    usdc = interface.IERC20(usdcToken)
    usdc.approve(routerAddress, 1000000000, {"from": accounts.load("0")})
    router.addLiquidity(1, 1000000000, accounts.load("0"), {"from": accounts.load("0")}) 

    # get 10 s*usdt
    usdt = interface.IERC20(usdtToken)
    usdt.approve(routerAddress, 2000000000, {"from": accounts.load("0")})
    router.addLiquidity(2, 2000000000, accounts.load("0"), {"from": accounts.load("0")})

    # add pool to lpstaking
    LpStakingContract.add(55, sUsdcToken, {"from": accounts.load("0")})
    LpStakingContract.add(45, sUsdtToken, {"from": accounts.load("0")})

    # deposit lp token
    lpstakingAddress = LpStakingContract.address
    # lpstakingAddress = "0x1Cb74544AaafBA3350C0E1149DDb304Bb0A0ff61"
    susdc = interface.IERC20(sUsdcToken)
    susdc.approve(lpstakingAddress, 10000000, {"from": accounts.load("0")})
    LpStakingContract.deposit(0, 10000000, {"from": accounts.load("0")})

    susdt = interface.IERC20(sUsdtToken)
    susdt.approve(lpstakingAddress, 10000000, {"from": accounts.load("0")})
    LpStakingContract.deposit(1, 10000000, {"from": accounts.load("0")})


