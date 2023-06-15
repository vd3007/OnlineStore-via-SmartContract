# OnlineStore-via-SmartContract
### References: [jspruance/block-explorer-tutorials](https://github.com/jspruance/block-explorer-tutorials/tree/main)
## Introduction
We've using the upper example to re-create the smart contract. <br>
**Important!** Some of the codes in _Final_Project.py_ needs to be replaced! <br>
1. Ether node connecting: <br>
   ```
   w3 = Web3(Web3.HTTPProvider('<your testnet url>'))
   ```
2. Contract address: <br>
   ```
   contract_address = '<your contract address>'
   ```
3. Contract ABI: <br>
   ```
   contract_abi = [ <your contract ABI> ] 
   ```
## User Interface 
![UI](https://raw.githubusercontent.com/vd3007/OnlineStore-via-SmartContract/main/UI.png "UI")
## Improvement
We consider some improvements that can enhance the project! <br>
* The buyer input private key for the purchase <br>
  1. Try to using function to **call out private key** from buyer address(If it's exist). <br>
  2. Pop out a window that can allow buyer enter their private key to prevent wallet been stolen from others! <br>
* Notice that your **currency value**! <br>
  * Ethernet = **ether** <br>
  * Mumbai = **MATIC** <br>
