// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;

import "./ILayerZeroEndpoint.sol";

interface IStargateToken {
    function pauseSendTokens(bool _pause) external;

    function setDestination(uint16 _dstChainId, bytes calldata _destinationContractAddress) external;

    function chainId() external view returns (uint16);
    function sendTokens(
        uint16 _dstChainId, // send tokens to this chainId
        bytes calldata _to, // where to deliver the tokens on the destination chain
        uint256 _qty, // how many tokens to send
        address _zroPaymentAddress, // ZRO payment address
        bytes calldata _adapterParam // txParameters
    ) external;
    
    //---------------------------DAO CALL----------------------------------------
    // generic config for user Application
    function setConfig(
        uint16 _version,
        uint16 _chainId,
        uint256 _configType,
        bytes calldata _config
    ) external;

    function setSendVersion(uint16 _version) external;

    function setReceiveVersion(uint16 _version) external;
}
// 0x714c1f77abc8ec4d6232e72f10be13aa3afe9c94  fantom
// 0x0000000000000000000000000000000000000000
// 0x9747909d36446468ef48f3400004310bd0acd7b5  goerli