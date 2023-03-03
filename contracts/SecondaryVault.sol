// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;
import "./Vault.sol";

contract SecondaryVault is Vault {
    VaultDescriptor primaryVault;

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
    function addPrimaryVault(VaultDescriptor memory _primaryVault) external onlyOwner {
        primaryVault = _primaryVault;
    }

    function onSyncRequest() external onlyOwner payable {
        SyncResponse memory syncResponse = prepareSyncResponse();
        bytes memory payload = abi.encode(
            syncResponse.totalStargate,
            syncResponse.totalStablecoin,
            syncResponse.totalInmoz
        );
        _lzSend(
            primaryVault.chainId,
            payload,
            payable(msg.sender),
            address(0x0),
            bytes(""),
            msg.value
        );
    }

    function _nonblockingLzReceive(
        uint16 srcChainId,
        bytes memory,
        uint64,
        bytes memory payload
    ) internal override {
        inmozPerStablecoin = abi.decode(payload, (uint256));
    }
}
