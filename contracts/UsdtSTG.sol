// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;
pragma abicoder v2;

// imports
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "../interfaces/IStargateToken.sol";

contract UsdtSTG is Ownable{
    uint256 totalUSDT = 0;
    uint256 totalSTG = 0;

    uint256 immutable usdtDesimals = 6;
    uint256 immutable stgDesimals = 18;
    
    address usdtToken;
    address stgToken;

    constructor(
        address _usdt,
        address _stg
    ) {
        usdtToken = _usdt;
        stgToken = _stg;
    }

    function USDTtoSTG(uint256 usdtAmount) public {
        IERC20(usdtToken).transferFrom(msg.sender, address(this), usdtAmount);
        totalUSDT += usdtAmount;
        uint256 stgAmount = totalSTG * usdtAmount / totalUSDT;
        IERC20(stgToken).transfer(msg.sender, stgAmount);
        totalSTG -= stgAmount;
    }

    function STGtoUSDT(uint256 stgAmount) public {
        IERC20(stgToken).transferFrom(msg.sender, address(this), stgAmount);
        totalSTG += stgAmount;
        uint256 usdtAmount = totalUSDT * stgAmount / totalSTG;
        IERC20(usdtToken).transfer(msg.sender, usdtAmount);
        totalUSDT -= usdtAmount;
    }

    function mint(uint256 _pid, uint256 _amount) public {
        if(_pid == 0) {
            IERC20(usdtToken).transferFrom(msg.sender, address(this), _amount);
            totalUSDT += _amount;
        }
        if(_pid == 1) {
            IERC20(stgToken).transferFrom(msg.sender, address(this), _amount);
            totalSTG += _amount;
        }
    }
    
    function totalSupply() external view returns(uint256) {
        return totalUSDT;
    }

    function totalLiquidity() external view returns(uint256) {
        return totalSTG;
    }
}