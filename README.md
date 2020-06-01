Work in progress documentation

# Implementation

You can use [QRC20Token](https://github.com/qtumproject/QRC20Token) code to create your own QRC20 token on Qtum. For this example, we will use Qtum testnet, first getting some testnet QTUM.

After installing the Qtum Core wallet from https://qtumeco.io/wallet or https://github.com/qtumproject/qtum/releases, get the wallet receiving address by selecting **Window** - **Receiving addresses**, select and copy the wallet receiving address qXGdYmLypZRy8pTpj9EdTBHkqtv6cv99ky.

![1  Copy Receiving Address](https://user-images.githubusercontent.com/29760787/83368341-727d9780-a386-11ea-973d-5f8b13767802.jpg)

We will need some QTUM to pay for the contract create gas and transaction fees, and can get some testnet QTUM from the [Qtum Testnet Faucet](http://testnet-faucet.qtum.info/). Paste the receiving address into the faucet and press the blue button checkmark.

![2  Testnet Faucet](https://user-images.githubusercontent.com/29760787/83368347-7a3d3c00-a386-11ea-940e-5ba4c83b32b8.jpg)

Next we can copy the token smart contract code at [QRC20Token](https://github.com/qtumproject/QRC20Token). In the QRC20Token.sol file you can change `name`, `symbol`, and `totalSupply` to your preference. For this example we will name the token "QRC TEST 527", give the symbol "QT527" and have a total supply of 1,000,000,000 which is entered as "10 * * 9". We will leave `decimals` set for 8, to give 8 decimal places for each token.

![3  Solidity](https://user-images.githubusercontent.com/29760787/83368355-7dd0c300-a386-11ea-820c-2ce2788e5777.jpg)

After editing the Solidity file, save it locally or just copy to paste into Remix.

Next we will use Remix to compile the Solidity code into bytecode. In a browser, go to Remix at http://remix.ethereum.org/ and select the SOLIDITY Environment.

![4  Select Solidity](https://user-images.githubusercontent.com/29760787/83368369-8d500c00-a386-11ea-9c80-98243d69bcd8.jpg)





