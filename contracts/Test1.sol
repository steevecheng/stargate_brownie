// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;
pragma abicoder v2;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Test1 {
    // NOTE: storage layout must be the same as contract A
    uint public num;
    address public sender;
    uint public value;
    event TestEvent(address, uint256);
    function setVars(uint _num) public payable {
        require(false, "occur error");
        num = _num;
        sender = msg.sender;
        value = msg.value;
        emit TestEvent(sender, value);
    }
}
