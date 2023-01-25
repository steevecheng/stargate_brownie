// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;

interface IVault {

    struct Order {
        uint16 srcChainId;
        uint16 srcPoolId;
        uint16 dstChainId;
        uint16 dstPoolId;
        uint256 transferAmount;
        uint256 burnValue;
        uint256 mintValue;
        uint256 poolIndex;
    }
    
    struct VaultDescriptor {
        uint16 chainId;
        address vaultAddress;
    }
    
    function requestInvest(uint16 poolIndex, uint256 amountSD) external;

    function requestHarvest(uint256 amountIM, uint16 poolIndex) external;

    function execute(Order[] memory _orders) external;

    function pendingHarvest(address _owner, uint16 _pid) external view returns(uint256);

    function pendingInverst(address _owner) external view returns(uint256);
    
    function addSecondaryVaults(VaultDescriptor[] memory _secondaryVaults) external;

    function sendFrom(address _from, uint16 _dstChainId, bytes calldata _toAddress, uint _amount, address payable _refundAddress, address _zroPaymentAddress, bytes calldata _adapterParams) external payable;
    
    function setUseCustomAdapterParams(bool _useCustomAdapterParams) external;
}
