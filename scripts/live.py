import yaml
from pathlib import Path
import json

from brownie import accounts, web3, interface, Contract

from scripts import config


def main():
    path = Path(__file__).parent / "../brownie-config.yaml"
    with path.open(mode="r") as stream:
        try:
            yamlJson = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    chainName = "polygon"
    contract = "Endpoint.sol"
    network = yamlJson["networks"]["default"]
    address = config.address[chainName][contract]
    contractObj = Contract.from_explorer(address)
    variableIfno = []
    variableList = ["chainId", "latestVersion", "defaultSendVersion", "defaultReceiveVersion", "defaultSendVersion", "defaultSendLibrary", "defaultReceiveLibraryAddress"]
    # variableValue = [{x: exec(f"contractObj.{x}()")} for x in variableList]
    for variable in variableList:
        variableIfno.append(
            {variable: eval(f"contractObj.{variable}()")}
        )
    info = {
        contract: {
            "chainName": chainName,
            "network": network,
            "address": address,
            "contract": contract,
            "var": variableIfno
        }
    }
    string = json.dumps(info)
    # f = open(f"{contract}.txt", "a+")
    # f.write(string + "\n")

    with open(f"{contract}.json", "a+") as file1:
        # Writing data to a file
        file1.writelines(string + "\n")
    