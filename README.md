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

Click the "+" button to create a new file.

![5  New File](https://user-images.githubusercontent.com/29760787/83368379-92ad5680-a386-11ea-9175-c8d42da28bab.jpg)

Enter the file name "QRC20Token.sol" and "OK" to create a new file. 

![6  Enter File Name](https://user-images.githubusercontent.com/29760787/83368383-96d97400-a386-11ea-84e7-7dd367aa9f00.jpg)

Paste in the source code.

![7  Paste in Code](https://user-images.githubusercontent.com/29760787/83368385-9a6cfb00-a386-11ea-88d6-5624214580bf.jpg)

Here you can see the code is edited to name the token "QRC TEST 527", with the symbol "QT527" and a supply of 1 billion.

Also create a new file, enter the file name "SafeMath.sol" and paste the code for safe math.
 
Select the compiler button on the left side.
 
![8  Compiler](https://user-images.githubusercontent.com/29760787/83368393-a062dc00-a386-11ea-8ae2-6c236a4cd288.jpg)

You can leave the Solidity version set for 0.4.26. At the top, click the tab for QRC20Token.sol to select that file to compile, and click the blue **Compile QRC20Token.sol** button.

![9  Run Compiler](https://user-images.githubusercontent.com/29760787/83368395-a35dcc80-a386-11ea-9b16-762ff3d31439.jpg)

Ignore the warnings.

Click on the Bytecode button to copy the bytecode.

![10  Copy Bytecode](https://user-images.githubusercontent.com/29760787/83368400-a789ea00-a386-11ea-85cf-4efa71e8d900.jpg)

Paste the copied bytecode into a text editor, and select the object code (shown here in blue). The object code starts with "60806" and ends with "00029".

![11  Get Object](https://user-images.githubusercontent.com/29760787/83368405-aa84da80-a386-11ea-9e2f-6ff1709343d9.jpg)

On the wallet, go to **Smart Contracts** - **Create** and paste the copied object code into the "Bytecode" field.

![12  Paste in Bytecode](https://user-images.githubusercontent.com/29760787/83368410-af498e80-a386-11ea-9cfc-ae5908f393ff.jpg)

At the bottom of the Create Contract form click the drop down on Sender Address and select qXGdYmLypZRy8pTpj9EdTBHkqtv6cv99ky. This sets the address to be used by the contract. Leave the gas set at 25000000 and price set at 0.0000040 unless you know how to change this. Click the **Create Contract** button and **Yes** to send the transaction. 

![13  Select Address](https://user-images.githubusercontent.com/29760787/83368414-b2447f00-a386-11ea-8d0f-5928865e835e.jpg)

The wallet will confirm the transaction with a Results form. Copy the Contract Address 137d046beb3cb66c0cdd389bf8bab4faeae16c0b.

![14  Results](https://user-images.githubusercontent.com/29760787/83368416-b4a6d900-a386-11ea-8e44-9c773aa94fa0.jpg)

The wallet Transaction page will show the transactions so far. First, the wallet received 90.0 QTUM sent from the Testnet faucet. Next, the contract create transation sent the contract bytecode and fees of 1.01414 QTUM. Finally, the wallet received a gas refund of 0.623456 QTUM. Gas refunds are sent in the coinstake transaction, so they shown as "mined" on the blockchain, and must mature for 500 blocks before they can be uses. 

![15  Transactions](https://user-images.githubusercontent.com/29760787/83368419-b7093300-a386-11ea-8508-86a14c7737ca.jpg)

You can also see the contract create transaction on [testnet.qtum.info](https://testnet.qtum.info/tx/0db7a5f38c1959d473405165bf842dcf726c9b79615b0b294514cb44e53fb801)

XXXXX math.

![16  Explorer](https://user-images.githubusercontent.com/29760787/83368426-bc667d80-a386-11ea-8039-6e3bc2f519f0.jpg)

# Adding Tokens

To see the new token in the wallet select **QRC Tokens** and the "**+**" button to the right of the Add new token.

![17  Add Token](https://user-images.githubusercontent.com/29760787/83368428-bf616e00-a386-11ea-8a72-ba2a19c21959.jpg)

Paste the contract address 137d046beb3cb66c0cdd389bf8bab4faeae16c0b into the Contract address field, and rest of the form will be filled in. At the bottom of the form click the drop down arrow to the right of the Token address field and select qXGdYmLypZRy8pTpj9EdTBHkqtv6cv99ky and **Confirm**. Could be multiples, XXXXX

![18  Paste Contract Address](https://user-images.githubusercontent.com/29760787/83368432-c1c3c800-a386-11ea-9b7b-5b4224934683.jpg)

You will see the Log events prompt "Enable log events from the option menu in order to receive token transactions" We will do this as the last step.

# Send Tokens

To send QRC20 tokens, select **QRC20 Tokens** and **Send**. Note there is single listing for the QT527 token tied to address qXGdYmLypZRy8pTpj9EdTBHkqtv6cv99ky here, but tokens could be tied to different addresses of this wallet, in which case they would be listed individually and sent individually.

Fill in the fields for "PayTo" and "Amount". The "Description" field is optional. Click **Send** and **Yes** to complete the transaction.

![19  Send QRC20 Tokens](https://user-images.githubusercontent.com/29760787/83368435-c4beb880-a386-11ea-9ebe-277f20e0b6ab.jpg)

Wallet **Transactions** will now show the contract send transaction. Right-click on teh transaction to see the details including the transaction ID.

# Enable Log Events

We can follow up now on the previous prompt to enable log events. In order for the wallet to fully display token transactions it needs to have log event enabled. Select **Settings** - **Options** and click on **Enable log events**. You must restart the wallet and rescan. The prompt will show "Client restart required to activate changes." Select **OK** then **Yes**. The wallet will exit, then restart the wallet. 

![20  Enable Log Events](https://user-images.githubusercontent.com/29760787/83368436-c7b9a900-a386-11ea-96f6-690abe10bfef.jpg)

WHen the wallet restarts, click **OK** to rebuild the block database. 

![21  Log Events](https://user-images.githubusercontent.com/29760787/83368438-c9836c80-a386-11ea-9c0b-f27ef946be7c.jpg)

The wallet status will show "Reindexing blocks on disk..." and "Syncing headers" for several minutes or several tens of minutes, depending on your computer. 

![22  Restarting Rebuild Database](https://user-images.githubusercontent.com/29760787/83368451-d607c500-a386-11ea-9caa-cb855bb3e07d.jpg)













