from brownie import accounts, web3, interface, UsdcSTG, UsdtSTG, convert

def main():
    chain = "mumbai"
    token = "usdt"
    tokenInfo = {
        "goerli": {
            "usdc" :"0xdf0360ad8c5ccf25095aa97ee5f2785c8d848620",
            "usdt" :"0x5BCc22abEC37337630C0E0dd41D64fd86CaeE951",
            "stgToken" :"0xe0D6deF971250715Cb97794D4105CBf28f389BB8",
        },
        "fuji": {
            "usdc": "0x4A0D1092E9df255cf95D72834Ea9255132782318",
            "usdt": "0x134Dc38AE8C853D1aa2103d5047591acDAA16682",
            "stgToken": "0x1Cb74544AaafBA3350C0E1149DDb304Bb0A0ff61",
        },
        "mumbai": {
            "usdc": "0x742DfA5Aa70a8212857966D491D67B09Ce7D6ec7",
            "usdt": "0x6Fc340be8e378c2fF56476409eF48dA9a3B781a0",
            "stgToken": "0x19Bda030d8520c5d4A6de15f5B5e127c25D8ca8A",
        },
        "initercmint": 10000000000000,
        "initstgmint": 6000000000000000000000000,
    }
    if token == "usdc":
        dexContract = UsdcSTG.deploy(tokenInfo[chain][token], tokenInfo[chain]["stgToken"], {"from": accounts.load("0")})
    if token == "usdt":
        dexContract = UsdtSTG.deploy(tokenInfo[chain][token], tokenInfo[chain]["stgToken"], {"from": accounts.load("0")})

    erc20Contract = interface.IERC20(tokenInfo[chain][token])
    stgContract = interface.IERC20(tokenInfo[chain]["stgToken"])

    erc20Contract.approve(dexContract.address, tokenInfo["initercmint"], {"from": accounts.load("0")})
    dexContract.mint(0, tokenInfo["initercmint"], {"from": accounts.load("0")})

    stgContract.approve(dexContract.address, tokenInfo["initstgmint"], {"from": accounts.load("0")})
    dexContract.mint(1, tokenInfo["initstgmint"], {"from": accounts.load("0")})