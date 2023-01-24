// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;
import "../contracts/Pool.sol";

interface IFactory {
    function setDefaultFeeLibrary(address) external;
    function allPoolsLength() external view returns (uint256);
    function getPool(uint256) external returns (Pool);
    function router() external returns(address);
}
