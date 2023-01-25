
// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./Layer_zero/NonblockingLzApp.sol";

contract Counter is ERC20, NonblockingLzApp {

    ILayerZeroEndpoint immutable public endpoint;
    uint256 immutable mainChainId;
    uint256 public initialSupply;
    uint public counter;
    event Log (uint16 _srcChainId, bytes _srcAddress, uint64 _nonce, bytes _payload);
    
    constructor (
        string memory _name,
        string memory _symbol,
        address _endpoint,
        uint256 _mainChainId
    ) ERC20 (
        _name,
        _symbol
    ) NonblockingLzApp (
        _endpoint
    )
    {
        endpoint = ILayerZeroEndpoint(_endpoint);   
        if(_mainChainId == ILayerZeroEndpoint(_endpoint).getChainId()){
            _mint(msg.sender, initialSupply);
        }
        mainChainId = _mainChainId;
    }

    function incrementCounter(uint16 _dstChainId, uint _nativeFee) public payable {
        // _lzSend calls endpoint.send()
        _lzSend(_dstChainId, bytes("hello"), payable(msg.sender), address(0x0), bytes("0x001"), _nativeFee);
    }

    function _nonblockingLzReceive(uint16 _srcChainId, bytes memory _srcAddress, uint64 _nonce, bytes memory _payload) internal override {
        counter += 1;
        emit Log(_srcChainId, _srcAddress, _nonce, _payload);
    }
    // function sendToken(uint16 _dstChainId, bytes calldata _to, uint256 _value, address _zroPaymentAddress, bytes calldata _adapterParam) public {
    //     if (mainChainId == endpoint.getChainId()) {
    //         _transfer(msg.sender, address(this), _value);
    //     }
    //     else {
    //         _burn(msg.sender, _value);
    //     }
    //     bytes memory remoteAndLocalAddresses = abi.encodePacked(remoteAddress, localAddress);
    //     endpoint.send{value: msg.value} (
    //         10001,                   // destination LayerZero chainId
    //         remoteAndLocalAddresses, // send to this address on the destination          
    //         bytes("hello"),          // bytes payload
    //         msg.sender,              // refund address
    //         address(0x0),            // future parameter
    //         bytes("")                // adapterParams (see "Advanced Features")
    //     );
    //     // sendFrom(msg.sender, _dstChainId, _to, _value, payable(msg.sender), _zroPaymentAddress, _adapterParam);
    //     // address _from, uint16 _dstChainId, bytes calldata _toAddress, uint _amount, address payable _refundAddress, address _zroPaymentAddress, bytes calldata _adapterParams
    // }
}