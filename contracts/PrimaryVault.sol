// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;
import "./Vault.sol";

contract PrimaryVault is Vault {
    VaultDescriptor[] secondaryVaults;
    uint256 totalStg;
    uint256 totalStableCoin;
    uint256 totalInmoz;

    constructor(
        string memory _name,
        string memory _symbol,
        address _lzEndpoint,
        uint16 _selfChainId,
        uint256 _initialSupply,
        address _IRouter,
        address _ILpStaking,
        address _IStgToken,
        PoolInfo[] memory _poolInfos
    )
        Vault(
            _name,
            _symbol,
            _lzEndpoint,
            _selfChainId,
            _initialSupply,
            _IRouter,
            _ILpStaking,
            _IStgToken,
            _poolInfos
        )
    {}

    // this function is executed only once.
    // after executing this function, should execute setTrustedRemote function for layerzero integration.
    function addSecondaryVaults(VaultDescriptor[] memory _secondaryVaults) external onlyOwner {
        for (uint256 i; i < _secondaryVaults.length; i++) {
            secondaryVaults.push(_secondaryVaults[i]);
        }
    }

    function _nonblockingLzReceive(
        uint16 srcChainId,
        bytes memory,
        uint64,
        bytes memory payload
    ) internal override {
        (uint256 _totalStg, uint256 _totalStableCoin, uint256 _totalInmoz) = abi
            .decode(payload, (uint256, uint256, uint256));
        totalStg += _totalStg;
        totalStableCoin += _totalStableCoin;
        totalInmoz += _totalInmoz;
    }

    function syncVaults() external onlyOwner payable{
        SyncResponse memory syncResponse = prepareSyncResponse();
        totalStg += syncResponse.totalStargate;
        totalStableCoin += syncResponse.totalStablecoin;
        totalInmoz += syncResponse.totalInmoz;
        uint256 stargatePrice;
        inmozPerStablecoin =
            totalInmoz /
            (totalStableCoin + totalStg * stargatePrice);
        for (uint256 i = 0; i < secondaryVaults.length; i++) {
            bytes memory payload = abi.encode(inmozPerStablecoin);
            _lzSend(
                secondaryVaults[i].chainId,
                payload,
                payable(address(this)),
                address(0x0),
                bytes(""),
                msg.value
            );
        }
        initSyncVault();
    }

    function initSyncVault() private {
        totalStg = 0;
        totalStableCoin = 0;
        totalInmoz = 0;
    }
}
