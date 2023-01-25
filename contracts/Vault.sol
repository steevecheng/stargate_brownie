// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;

// imports
import "./OFT/OFT.sol";
import "./OrderTaker.sol";

// libraries
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Vault is OFT, OrderTaker {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;

    // invest
    address[] public pendingInvestors;
    mapping(address => uint256) pendingInvests;
    uint256 totalPendingInvests = 0;
    // harvest
    address[] public pendingHarvestors;
    mapping(address => uint16[]) pendingHarvestPoolIndexes;
    mapping(address => mapping(uint16 => uint256)) public pendingHarvests;
    uint256 inmozPerStablecoin;
    struct VaultDescriptor {
        uint16 chainId;
        address vaultAddress;
    }

    struct SyncResponse {
        uint256 totalStargate;
        uint256 totalStablecoin;
        uint256 totalInmoz;
    }

    constructor(
        string memory _name,
        string memory _symbol,
        address _lzEndpoint,
        uint16 _selfChainId,
        uint256 _initialSupply,
        address _IRouter,
        address _ILpStaking,
        address _IStgToken,
        PoolInfo[] memory _poolInfos
    )
        OFT(_name, _symbol, _lzEndpoint, _initialSupply)
        OrderTaker(_selfChainId, _IRouter, _ILpStaking,_IStgToken, _poolInfos)
    {}

    function requestInvest(uint16 poolIndex, uint256 amountSD) external {
        address token = poolInfos[poolIndex].erc20Address;
        address _investor = msg.sender;
        IERC20(token).safeTransferFrom(_investor, address(this), amountSD);

        if (pendingInvests[_investor] == 0) {
            pendingInvestors.push(_investor);
        }
        pendingInvests[_investor] += amountSD;
        totalPendingInvests += amountSD;
    }

    function requestHarvest(uint256 amountIM, uint16 poolIndex) external {
        address _harvestor = msg.sender;
        pendingHarvestors.push(_harvestor);

        if (indexOf(pendingHarvestPoolIndexes[_harvestor], poolIndex) == -1) {
            pendingHarvestPoolIndexes[_harvestor].push(poolIndex); // don't push if already pushed.
        }
        pendingHarvests[_harvestor][poolIndex] += amountIM;
    }

    function acceptInvests() private {
        for (uint i = 0; i < pendingInvestors.length; i++) {
            uint256 pendingInvest = pendingInvests[pendingInvestors[i]];
            _mint(pendingInvestors[i], pendingInvest * inmozPerStablecoin);
            pendingInvests[pendingInvestors[i]] = 0;
        }
        delete pendingInvestors;
        totalPendingInvests = 0;
    }

    function acceptHarvests() private {
        for (uint256 i = 0; i < pendingHarvestors.length; i++) {
            uint256 harvestedInmoz = 0;
            address pendingHarvestor = pendingHarvestors[i];
            for (uint256 j = 0; j < pendingHarvestPoolIndexes[pendingHarvestor].length; j++) {
                uint16 poolIndex = pendingHarvestPoolIndexes[pendingHarvestor][j];
                PoolInfo storage poolInfo = poolInfos[poolIndex];
                uint256 pendingHarvestAmount = pendingHarvests[pendingHarvestor][poolIndex];
                pendingHarvests[pendingHarvestor][poolIndex] = 0;
                harvestedInmoz += pendingHarvestAmount;
                // give back stablecoin. harvest is succesful here !!
                address token = poolInfo.erc20Address;
                IERC20(token).safeTransfer(
                    pendingHarvestor,
                    harvestedInmoz / inmozPerStablecoin
                );
            }
            _burn(pendingHarvestor, harvestedInmoz);
        }
        delete pendingHarvestors;
    }

    function prepareSyncResponse() internal onlyOwner view returns (SyncResponse memory){
        SyncResponse memory syncResponse;
        syncResponse.totalStargate = IERC20(IStgToken).balanceOf(address(this));
        syncResponse.totalStablecoin = 0;
        for (uint i=0; i<poolInfos.length; i++) {
            PoolInfo storage poolInfo = poolInfos[i];
            uint256 _totalSupply = IStargateLpStaking(poolInfo.Ipool).totalSupply();
            uint256 _totalLiquidity = IStargateLpStaking(poolInfo.Ipool).totalLiquidity();
            uint256 _balance = IERC20(poolInfo.Ipool).balanceOf(address(this));
            syncResponse.totalStablecoin += _balance.div(_totalSupply).mul(_totalLiquidity);
        }
        syncResponse.totalStablecoin -=  totalPendingInvests;
        syncResponse.totalInmoz = totalSupply();
        return syncResponse;
    }

    function execute(Order[] memory _orders) external onlyOwner {
        acceptInvests();
        executeOrders(_orders);
        acceptHarvests();
    }
    // function to check if array has same element
    function indexOf(uint16[] storage arr, uint16 searchFor) internal view returns (int16) {
        for (uint16 i = 0; i < arr.length; i++) {
            if (arr[i] == searchFor) {
                return int16(i);
            }
        }
        return -1; // not found
    }
}
