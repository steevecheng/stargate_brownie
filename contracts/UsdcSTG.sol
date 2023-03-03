// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;
pragma abicoder v2;

// imports
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "../interfaces/IStargateToken.sol";

contract UsdcSTG is Ownable{
    uint256 totalUSDC = 0;
    uint256 totalSTG = 0;

    uint256 immutable usdcDesimals = 6;
    uint256 immutable stgDesimals = 18;
    
    address usdcToken;
    address stgToken;

    constructor(
        address _usdc,
        address _stg
    ) {
        usdcToken = _usdc;
        stgToken = _stg;
    }

    function USDCtoSTG(uint256 usdcAmount) public {
        IERC20(usdcToken).transferFrom(msg.sender, address(this), usdcAmount);
        totalUSDC += usdcAmount;
        uint256 stgAmount = totalSTG * usdcAmount / totalUSDC;
        IERC20(stgToken).transfer(msg.sender, stgAmount);
        totalSTG -= stgAmount;
    }

    function STGtoUSDC(uint256 stgAmount) public {
        IERC20(stgToken).transferFrom(msg.sender, address(this), stgAmount);
        totalSTG += stgAmount;
        uint256 usdcAmount = totalUSDC * stgAmount / totalSTG;
        IERC20(usdcToken).transfer(msg.sender, usdcAmount);
        totalUSDC -= usdcAmount;
    }

    function mint(uint256 _pid, uint256 _amount) public {
        if(_pid == 0) {
            IERC20(usdcToken).transferFrom(msg.sender, address(this), _amount);
            totalUSDC += _amount;
        }
        if(_pid == 1) {
            IERC20(stgToken).transferFrom(msg.sender, address(this), _amount);
            totalSTG += _amount;
        }
    }
    
    function totalSupply() external view returns(uint256) {
        return totalUSDC;
    }

    function totalLiquidity() external view returns(uint256) {
        return totalSTG;
    }
}