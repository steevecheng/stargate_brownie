// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;

// imports
import "@openzeppelin/contracts/access/Ownable.sol";

// libraries
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

// interfaces
import "../interfaces/IStargateRouter.sol";
import "../interfaces/IStargateLpStaking.sol";

contract OrderTaker is Ownable {
    using SafeMath for uint256;
    uint16 chainId; // LayerZero defined chain ID;
    address IRouter; // Stargate Router Address.
    address ILpStaking; // Stargate Farming Pool Address.
    address IStgToken; // Stargate Token Address.
    struct PoolInfo {
        address erc20Address; // Eg, address to Stargate token.
        address Ipool; // Stargate Liquidity Pool Address.
    }
    PoolInfo[] public poolInfos;

    struct Order {
        uint16 srcChainId;
        uint16 srcPoolId;
        uint16 dstChainId;
        uint16 dstPoolId;
        uint256 transferAmount;
        uint256 burnValue;
        uint256 mintValue;
        uint256 poolIndex;
    }
    Order[] orders;

    uint16 selfChainId;

    constructor(
        uint16 _selfChainId,
        address _IRouter,
        address _ILpStaking,
        address _IStgToken,
        PoolInfo[] memory _poolInfos
    ) {
        selfChainId = _selfChainId;
        IRouter = _IRouter;
        ILpStaking = _ILpStaking;
        IStgToken = _IStgToken;
        for (uint256 i = 0; i < _poolInfos.length; i += 1) {
            poolInfos.push(_poolInfos[i]);
        }
    }

    function setOrders(Order[] memory _orders) private {
        delete orders;
        for (uint256 i = 0; i < _orders.length; i += 1) {
            orders.push(_orders[i]);
        }
    }

    function executeOrders(Order[] memory _orders) internal onlyOwner {
        setOrders(_orders);
        require(orders.length > 0, "There is no orders");
        for (uint256 i = 0; i < orders.length; i++) {
            Order storage _order = orders[i];
            require(
                _order.srcChainId == selfChainId,
                "order should be taken in same chain"
            );
            // swap stablecoin
            if (_order.transferAmount > 0) {
                IStargateRouter(IRouter).swap(
                    _order.dstChainId,
                    _order.srcPoolId,
                    _order.dstPoolId,
                    payable(msg.sender),
                    _order.transferAmount,
                    0,
                    IStargateRouter.lzTxObj(0, 0, "0x"),
                    abi.encodePacked(msg.sender),
                    bytes("")
                );
            }
            // mint into stargate pool
            {
                IStargateRouter(IRouter).addLiquidity(
                    _order.srcPoolId,
                    _order.mintValue,
                    address(this)
                );
                uint256 lptoken = IStargateLpStaking(
                    poolInfos[_order.poolIndex].Ipool
                ).balanceOf(address(this));
                IStargateLpStaking(ILpStaking).deposit(
                    _order.srcPoolId,
                    lptoken
                );
            }
            // burn from stargate pool
            if (_order.burnValue > 0) {
                uint256 _totalSupply = IStargateLpStaking(
                    poolInfos[_order.poolIndex].Ipool
                ).totalSupply();
                uint256 _totalLiquidity = IStargateLpStaking(
                    poolInfos[_order.poolIndex].Ipool
                ).totalLiquidity();
                uint256 lptoken = _order.burnValue.mul(_totalSupply).div(
                    _totalLiquidity
                );

                IStargateLpStaking(ILpStaking).withdraw(
                    _order.srcPoolId,
                    lptoken
                );

                IStargateRouter(IRouter).instantRedeemLocal(
                    _order.srcPoolId,
                    lptoken,
                    address(this)
                );
            }
            // sell STG
            
        }
    }
}
