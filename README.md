# OnlineStore-via-SmartContract
### References: [jspruance/block-explorer-tutorials](https://github.com/jspruance/block-explorer-tutorials/tree/main)
## Introduction
This is a small project through smart contract & python.  
We've using the upper example to re-create the smart contract. Meanwhile thanks to **[jspruance]**(https://github.com/jspruance) for providing an example.  
Returning to the point, it allow us using python UI to connect to the smart contract.  
But before that, you need to deploy the smart contract on the **[RemixIDE]**(https://remix.ethereum.org/#lang=en&optimize=false&runs=200&evmVersion=null&version=soljson-v0.8.11+commit.d7f03943.js).  
In this case, we've using **MetaMask** to get our account address and private-key to execute the functions.  
## Cautions 
**Important!** Some of the codes in ***Final_Project.py*** needs to be replaced! <br>
1. Ether node connecting: <br>
   ```python
   w3 = Web3(Web3.HTTPProvider('<your testnet url>'))
   ```
2. Contract address: <br>
   ```python
   contract_address = '<your contract address>'
   ```
3. Contract ABI: <br>
   ```python
   contract_abi = [ <your contract ABI> ] 
   ```
### Attention! Do not expose your private key to others!
## User Interface 
![UI](https://raw.githubusercontent.com/vd3007/OnlineStore-via-SmartContract/main/UI.png "UI")
## Improvement
We consider **some improvements** that can enhance the project! <br>
* The buyer input private key for the purchase <br>
  * Try to using function to **call out private key** from buyer address **(If it's exist)**. <br>
  * Pop out a window that can allow buyer enter their private key to prevent wallet been stolen from others! <br>
* Notice that your **currency value**! <br>
  * Ethernet = **ether** <br>
  * Mumbai = **MATIC** <br>
* Adding more functions beyond smart contract <br>
  * Upload the picture of the groceries.  
  * Sort product with different category.  
