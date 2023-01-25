from brownie import Factory, accounts, Router, MockToken, LZEndpointMock, Bridge, StargateToken, LPStaking, StargateFeeLibraryV01, StargateFeeLibraryV02, Pool, web3, interface, PrimaryVault
import scripts.config as config
def main():
    PrimaryVaultContract = PrimaryVault.deploy(
        "Mozaic Layer Zero Token",
        "INMOZ",
        "0xbfD2135BFfbb0B5378b56643c2Df8a87552Bfa23",
        10121,
        100000000000000000000000,
        "0x7612aE2a34E5A363E137De748801FB4c86499152",
        "0x3eC94aDa1F6fC1af82E16cf27305CFae692E35B8",
        "0xe0D6deF971250715Cb97794D4105CBf28f389BB8",
        [
            ("0xdf0360ad8c5ccf25095aa97ee5f2785c8d848620","0xa02e1f8c4546367763fa78fc077ba89291d4bc6c"),
            ("0x5BCc22abEC37337630C0E0dd41D64fd86CaeE951","0x925d10060ab7D3150895C87a4138e7Fd379508bB")
        ],
        {"from": accounts.load("0")}
    )