from brownie import Factory, accounts, Router, MockToken, LZEndpointMock, Bridge, StargateToken, LPStaking, StargateFeeLibraryV01, StargateFeeLibraryV02, Pool, web3, interface
import scripts.config as config
def main():

    stgPerBlock = 670000000000000000
    testnet = "fuji"
    usdcToken = "0x4A0D1092E9df255cf95D72834Ea9255132782318"
    usdtToken = "0x134Dc38AE8C853D1aa2103d5047591acDAA16682"
    sUsdcToken = "0xf14b09e2524855460d3a2cf7e682b8e8b1ba0f35"
    sUsdtToken = "0x024511D18C8932523dD91770ec015be365806D4E"
    routerAddress = "0x13093E05Eb890dfA6DacecBdE51d24DabAb2Faa1"

    stgReleaseAmount = 1000000000000000000000000

    currentBlock = web3.eth.blockNumber
    startBlock = currentBlock + 20
    print(currentBlock, startBlock)

    
    LpStakingContract = LPStaking.deploy(
        config.testnetEndpoint[testnet]["stargate"],
        stgPerBlock,
        startBlock,
        startBlock,
        {"from": accounts.load("0")}
    )
    print(LpStakingContract.address)
    stg  = interface.IERC20(config.testnetEndpoint[testnet]["stargate"])
    # stg.transfer(LpStakingContract.address, stgReleaseAmount, {"from": accounts.load("0")})


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


