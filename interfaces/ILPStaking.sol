// SPDX-License-Identifier: BUSL-1.1

pragma solidity 0.8.0;

interface ILPStaking {
    function poolLength() external view returns (uint256);
    function pendingStargate(uint256 _pid, address _user) external view returns (uint256);

    function massUpdatePools() external;

    function updatePool(uint256 _pid) external;

    function deposit(uint256 _pid, uint256 _amount) external;

    function withdraw(uint256 _pid, uint256 _amount) external;

    function emergencyWithdraw(uint256 _pid) external;

    function getMultiplier(uint256 _from, uint256 _to) external view returns (uint256);
    function add(uint256 _allocPoint, address _lpToken) external;

    function set(uint256 _pid, uint256 _allocPoint) external;
}