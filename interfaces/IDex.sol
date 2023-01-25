// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;
pragma abicoder v2;

// imports
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "../interfaces/IStargateToken.sol";

interface IDex {

    function USDCtoSTG(uint256 usdcAmount) external;

    function USDTtoSTG(uint256 usdtAmount) external;

    function STGtoUSDT(uint256 stgAmount) external;

    function STGtoUSDC(uint256 stgAmount) external;

    function mint(uint256 _pid, uint256 _amount) external;
    
    function totalSupply() external view returns(uint256);

    function totalLiquidity() external view returns(uint256);
}