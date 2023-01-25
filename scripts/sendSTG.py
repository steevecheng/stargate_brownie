from brownie import Factory, accounts, Router, MockToken, LZEndpointMock, Bridge, StargateToken, LPStaking, StargateFeeLibraryV01, StargateFeeLibraryV02, Pool, web3, interface
import scripts.config as config

def main():
    stg = interface.IStargateToken("0xe0D6deF971250715Cb97794D4105CBf28f389BB8")
    stg.send