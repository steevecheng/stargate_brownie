// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;
pragma abicoder v2;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Test {
    uint public num;
    address public sender;
    uint public value;

    function setVars(address _contract, uint _num) public payable returns(bool, bytes memory){
        // A's storage is set, B is not modified.
        (bool success, bytes memory data) = _contract.delegatecall(
            abi.encodeWithSignature("setVars(uint256)", _num)
        );
        return (success, data);
    }
}
