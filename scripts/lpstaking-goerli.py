from brownie import Factory, accounts, Router, MockToken, LZEndpointMock, Bridge, StargateToken, LPStaking, StargateFeeLibraryV01, StargateFeeLibraryV02, Pool, web3, interface
import scripts.config as config
def main():

    stgPerBlock = 1670000000000000000
    testnet = "goerli"
    usdcToken = "0xdf0360ad8c5ccf25095aa97ee5f2785c8d848620"
    usdtToken = "0x5BCc22abEC37337630C0E0dd41D64fd86CaeE951"
    sUsdcToken = "0xa02e1f8c4546367763fa78fc077ba89291d4bc6c"
    sUsdtToken = "0x925d10060ab7D3150895C87a4138e7Fd379508bB"
    routerAddress = "0x7612aE2a34E5A363E137De748801FB4c86499152"

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
    stg.transfer(LpStakingContract.address, stgReleaseAmount, {"from": accounts.load("0")})


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


