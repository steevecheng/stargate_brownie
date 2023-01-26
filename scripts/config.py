stargateConfig = {
    "stargateToken": {
        "name": "StargateToken for Mozaic",
        "symbol": "MSTG",
        "mainEndpointId": 10021,
        "initialSupplyMainEndpoint": 1000000000000000000000000000
    },
    "vsStargateToken": {
        "name": "veStargateToken",
        "symbol": "veSTG"
    },
    "gasAmounts": {
        "1": "215000",
        "2": "500000",
        "3": "500000",
        "4": "500000"
    },
}

testnetEndpoint = {
    "goerli": {
        "chainId": 10021,
        "endpoint": "0xbfD2135BFfbb0B5378b56643c2Df8a87552Bfa23",
        "stargate": "0xe0D6deF971250715Cb97794D4105CBf28f389BB8",
    },
    "bsc-test": {
        "chainId": 10002,
        "endpoint": "0x6Fcb97553D41516Cb228ac03FdC8B9a0a9df04A1"
    },
    "fuji": {
        "chainId": 10006,
        "endpoint": "0x93f54D755A063cE7bB9e6Ac47Eccc8e33411d706",
        "stargate": "0x1Cb74544AaafBA3350C0E1149DDb304Bb0A0ff61"
    },
    "mumbai": {
        "chainId": 10009,
        "endpoint": "0xf69186dfBa60DdB133E91E9A4B5673624293d8F8",
        "stargate": "",
    },
    "arbitrum-goerli": {
        "chainId": 10143,
        "endpoint": "0x6aB5Ae6822647046626e83ee6dB8187151E1d5ab"
    },
    "optimism-goerli": {
        "chindId": 10132,
        "endpoint": "0xae92d5aD7583AD66E49A0c67BAd18F6ba52dDDc1"
    },
    "ftm-test": {
        "chainId": 10012,
        "endpoint": "0x7dcAD72640F835B0FA36EFD3D6d3ec902C7E5acf"
    }
}

pool= {
    "USDC": {
        "pid": 1,
        "decimals": 18,
        "name": "USDC",
        "symbol": "USDC"
    },
    "USDT": {
        "pid": 2,
        "decimals": 18,
        "name": "USDT",
        "symbol": "USDT"
    },
    "BUSD": {
        "pid": 5,
        "decimals": 18,
        "name": "BUSD",
        "symbol": "BUSD"
    }
}

address = {
    "ethereum": {
        "Endpoint.sol": "0x66A71Dcef29A0fFBDBE3c6a460a3B5BC225Cd675"
    },
    "bsc": {
        "Endpoint.sol": "0x3c2269811836af69497E5F486A85D7316753cf62"
    },
    "avalanche": {
        "Endpoint.sol": "0x3c2269811836af69497E5F486A85D7316753cf62"
    },
    "polygon": {
        "Endpoint.sol": "0x3c2269811836af69497E5F486A85D7316753cf62"
    }
}