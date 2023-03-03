// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;

interface IMint {
    function mint(address _to, uint _amount) external;
}