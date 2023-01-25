from brownie import Factory, accounts, Router, MockToken, LZEndpointMock, Bridge, StargateToken, LPStaking, StargateFeeLibraryV01, StargateFeeLibraryV02, Pool, web3, interface, SecondaryVault
import scripts.config as config
def main():
    SecondaryVaultContract = SecondaryVault.deploy(
        "Mozaic Layer Zero Token",
        "INMOZ",
        "0x93f54D755A063cE7bB9e6Ac47Eccc8e33411d706",
        10106,
        100000000000000000000000,
        "0x13093E05Eb890dfA6DacecBdE51d24DabAb2Faa1",
        "0x65B26B3d6BF4Ad42C00c5871119b31439ae8c700",
        "0x1Cb74544AaafBA3350C0E1149DDb304Bb0A0ff61",
        [
            ("0x4A0D1092E9df255cf95D72834Ea9255132782318","0xf14b09e2524855460d3a2cf7e682b8e8b1ba0f35"),
            ("0x134Dc38AE8C853D1aa2103d5047591acDAA16682","0x024511D18C8932523dD91770ec015be365806D4E")
        ],
        {"from": accounts.load("0")}
    )