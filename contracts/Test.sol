// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;
pragma abicoder v2;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";
contract Test {
    function rate(uint256 b) public pure returns (uint256){
        return (2**255 + (2**255 - 1)) / b;
    }
}
