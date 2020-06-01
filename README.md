Work in progress documentation

* [Creating QRC20 Tokens](https://github.com/JB395/Various-Documentation/blob/master/README.md#creating-qrc20-tokens)
* [Adding Tokens](https://github.com/JB395/Various-Documentation/blob/master/README.md#adding-tokens)
* [Send Tokens](https://github.com/JB395/Various-Documentation/blob/master/README.md#send-tokens)
* [Enable Log Events](https://github.com/JB395/Various-Documentation/blob/master/README.md#enable-log-events)
* [Multiple Tokens in Wallet](https://github.com/JB395/Various-Documentation/blob/master/README.md#multiple-tokens-in-wallet)

# Creating QRC20 Tokens

You can use [QRC20Token](https://github.com/qtumproject/QRC20Token) code to create your own QRC20 token on Qtum. For this example, we will use Qtum testnet, first getting some testnet QTUM.

After installing the Qtum Core wallet from https://qtumeco.io/wallet or https://github.com/qtumproject/qtum/releases, get the wallet receiving address by selecting **Window** - **Receiving addresses**, select and copy the wallet receiving address qXGdYmLypZRy8pTpj9EdTBHkqtv6cv99ky.

![1  Copy Receiving Address](https://user-images.githubusercontent.com/29760787/83368341-727d9780-a386-11ea-973d-5f8b13767802.jpg)

We need some QTUM to pay for the smart contract gas and transaction fees and can get some testnet QTUM from the [Qtum Testnet Faucet](http://testnet-faucet.qtum.info/). Paste the receiving address into the faucet address field and press the blue checkmark button.

![2  Testnet Faucet](https://user-images.githubusercontent.com/29760787/83368347-7a3d3c00-a386-11ea-940e-5ba4c83b32b8.jpg)

Next, copy the token code at [QRC20Token](https://github.com/qtumproject/QRC20Token). In the QRC20Token.sol file you can change `name`, `symbol`, and `totalSupply` to your preference. For this example, we will edit later to name the token "QRC TEST 527", the symbol "QT527" and have a total supply of 1,000,000,000 which is entered as "10 * * 9". We will leave `decimals` set for 8, to give 8 decimal places for each token, so for example, you should send a 1.12345678 token amount. 

![3  Solidity](https://user-images.githubusercontent.com/29760787/83368355-7dd0c300-a386-11ea-820c-2ce2788e5777.jpg)

After editing the Solidity file, save it locally or just copy to paste into Remix.

Next, we will use Remix to compile the Solidity code into bytecode. In a browser, go to Remix at http://remix.ethereum.org/ and select the SOLIDITY Environment.

![4  Select Solidity](https://user-images.githubusercontent.com/29760787/83368369-8d500c00-a386-11ea-9c80-98243d69bcd8.jpg)

Click the "+" button to create a new file.

![5  New File](https://user-images.githubusercontent.com/29760787/83368379-92ad5680-a386-11ea-9175-c8d42da28bab.jpg)

Enter the file name "QRC20Token.sol" and "OK" to create a new file. 

![6  Enter File Name](https://user-images.githubusercontent.com/29760787/83368383-96d97400-a386-11ea-84e7-7dd367aa9f00.jpg)

Paste in the source code from the QRC20Token.sol file.

![7  Paste in Code](https://user-images.githubusercontent.com/29760787/83368385-9a6cfb00-a386-11ea-88d6-5624214580bf.jpg)

Here you can see the code has been edited to name the token "QRC TEST 527", with the symbol "QT527", and a supply of 1 billion.

Also, create a new file, enter the file name "SafeMath.sol" and paste in the code for [SafeMath.sol](https://github.com/qtumproject/QRC20Token/blob/master/SafeMath.sol).
 
Select the compiler button on the left side.
 
![8  Compiler](https://user-images.githubusercontent.com/29760787/83368393-a062dc00-a386-11ea-8ae2-6c236a4cd288.jpg)

The compiler tab is shown below. You can leave the Solidity version set for 0.4.26. At the top, click the tab for QRC20Token.sol to select that file to compile, and click the blue **Compile QRC20Token.sol** button to compile the source code into bytecode.

![9  Run Compiler](https://user-images.githubusercontent.com/29760787/83368395-a35dcc80-a386-11ea-9b16-762ff3d31439.jpg)

Ignore the warnings.

Click on the Bytecode button to copy the bytecode.

![10  Copy Bytecode](https://user-images.githubusercontent.com/29760787/83368400-a789ea00-a386-11ea-85cf-4efa71e8d900.jpg)

Paste the copied bytecode into a text editor, and select just the numeric characters for the object code (shown here highlighted in blue). The object code starts with "60806" and ends with "00029" (not shown in this image).

![11  Get Object](https://user-images.githubusercontent.com/29760787/83368405-aa84da80-a386-11ea-9e2f-6ff1709343d9.jpg)

On the wallet, go to **Smart Contracts** - **Create** and paste the copied object code into the "Bytecode" field.

![12  Paste in Bytecode](https://user-images.githubusercontent.com/29760787/83368410-af498e80-a386-11ea-9cfc-ae5908f393ff.jpg)

At the bottom of the Create Contract form, click the drop-down on "Sender Address" and select qXGdYmLypZRy8pTpj9EdTBHkqtv6cv99ky. This sets the address to be used by the contract. Leave the gas set at 25000000 and price set at 0.0000040 unless you know how to safely change these. Click the **Create Contract** button and **Yes** to send the transaction. 

![13  Select Address](https://user-images.githubusercontent.com/29760787/83368414-b2447f00-a386-11ea-8d0f-5928865e835e.jpg)

The wallet will confirm the transaction on the "Result 1" tab. Copy the Contract Address 137d046beb3cb66c0cdd389bf8bab4faeae16c0b.

![14  Results](https://user-images.githubusercontent.com/29760787/83368416-b4a6d900-a386-11ea-8e44-9c773aa94fa0.jpg)

The wallet Transaction page will show the transactions so far. First, the wallet received 90.0 QTUM sent from the Testnet faucet. Next, the contract create transaction sent the contract bytecode and fees of 1.01414 QTUM. Finally, the wallet received a gas refund of 0.623456 QTUM. Gas refunds are sent in the coinstake transaction, so they are show as "mined" in the wallet and must mature for 500 blocks before they can be used. 

![15  Transactions](https://user-images.githubusercontent.com/29760787/83368419-b7093300-a386-11ea-8508-86a14c7737ca.jpg)

You can also see the contract create transaction on [testnet.qtum.info](https://testnet.qtum.info/tx/0db7a5f38c1959d473405165bf842dcf726c9b79615b0b294514cb44e53fb801)

![16  Explorer](https://user-images.githubusercontent.com/29760787/83368426-bc667d80-a386-11ea-8039-6e3bc2f519f0.jpg)

The transaction was sent with 2,500,000 gas at price of 0.00000040 QTUM. The contract creation used 941,360 gas giving a gas refund of 2,500,000 - 941,360 = 1,558,640 at price of 0.00000040 or 0.623456 QTUM for the refund. 

# Adding Tokens

Smart contract transactions are sent to the smart contract address, not the wallet address, and for the wallet to see or make smart contract transactions we must inform the wallet, in this case by "adding" the token. To see the new token in the wallet, select **QRC Tokens** and the "**+**" button to the right of the Add new token.

![17  Add Token](https://user-images.githubusercontent.com/29760787/83368428-bf616e00-a386-11ea-8a72-ba2a19c21959.jpg)

Paste the contract address 137d046beb3cb66c0cdd389bf8bab4faeae16c0b into the "Contract Address" field, and rest of the form will be autofilled. At the bottom of the form click the drop-down arrow to the right of the Token address field and select qXGdYmLypZRy8pTpj9EdTBHkqtv6cv99ky and **Confirm**. If the wallet is using multiple addresses, chose the correct Qtum address that was used to create the token.

![18  Paste Contract Address](https://user-images.githubusercontent.com/29760787/83368432-c1c3c800-a386-11ea-9b7b-5b4224934683.jpg)

You will see the Log events prompt "Enable log events from the option menu to receive token transactions". We will do this step below.

![21  Log Events](https://user-images.githubusercontent.com/29760787/83368438-c9836c80-a386-11ea-9c0b-f27ef946be7c.jpg)

# Send Tokens

To send QRC20 tokens, select **QRC20 Tokens** and **Send**. Note there is single row listing for the QT527 token tied to address qXGdYmLypZRy8pTpj9EdTBHkqtv6cv99ky here, but tokens could be tied to different addresses of this wallet, in which case they would be listed individually and need to be sent individually.

Fill in the fields for "PayTo" and "Amount". The "Description" field is optional. Click **Send** and **Yes** to complete the transaction.

![19  Send QRC20 Tokens](https://user-images.githubusercontent.com/29760787/83368435-c4beb880-a386-11ea-9ebe-277f20e0b6ab.jpg)

Wallet **Transactions** will now show the contract send transaction. Right-click on the transaction to see the details including the transaction ID.

# Enable Log Events

We can follow up now on the previous prompt to enable log events. For the wallet to fully display token transactions it needs to have log events enabled. Select **Settings** - **Options** and click to select **Enable log events**. You must restart the wallet and rescan. The prompt will show "Client restart required to activate changes." Select **OK** then **Yes**. The wallet will exit, then restart the wallet. 

![20  Enable Log Events](https://user-images.githubusercontent.com/29760787/83368436-c7b9a900-a386-11ea-96f6-690abe10bfef.jpg)

When the wallet restarts, click **OK** to rebuild the block database. 

The wallet status will show "Reindexing blocks on disk..." and "Syncing headers" for several minutes or several tens of minutes, depending on your computer. 

![22  Restarting Rebuild Database](https://user-images.githubusercontent.com/29760787/83368451-d607c500-a386-11ea-9caa-cb855bb3e07d.jpg)

# Multiple Tokens in Wallet

QRC20 token balances are managed by the smart contract for individual Qtum addresses, even if these Qtum addresses are for the same wallet.

Continuing the example above, we sent 500 QT527 tokens to the wallet on a new receiving address qRdxBZSvUx1edUfygyHr35mVgmX9pAMLrZ. To show this new transaction of QT527 tokens in the wallet we must complete the Add Token step for this new address.

![23  Add 2nd Token](https://user-images.githubusercontent.com/29760787/83447393-5cbbb100-a41e-11ea-889e-8675e626341e.jpg)

Now the tokens for each tied address are shown separately and each row can be used separately for send and receive operations.

![24  Two QRC20 Tokens Listed](https://user-images.githubusercontent.com/29760787/83448628-3bf45b00-a420-11ea-8288-795e482c381a.jpg)

***










