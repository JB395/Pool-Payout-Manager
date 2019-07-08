Work in progress documentation

# Qtum Testnet

Qtum Testnet offers a public blockchain for testing and development. Free QTUM Testnet coins are available from a faucet and users can test transactions, staking, smart contract creation and operations, QRC20 transactions, etc. Testnet is a separate blockchain from Mainnet. It has different blocks, different transactions, and different coins, but the operation, protocols and specifications are identical to Mainnet (unless new features are being introduced on Testnet).

The Qtum Core wallet application can be set to run on Testnet with the command line parameter "`-testnet`" on startup. A Testnet wallet works identically to a Mainnet wallet except it will use the \Qtum\testnet3 data directory and default port 13888. An additional test mode "regtest" is described below.

# Testnet Explorer

Explorer https://testnet.qtum.info/

Older Explorer https://testnet.qtum.org/

# Testnet Faucet

Get free Testnet QTUM, once every 24 hours http://testnet-faucet.qtum.info

![1 QtumTestnetFaucet](https://user-images.githubusercontent.com/29760787/60820451-718cb780-a16f-11e9-99be-989ca3388f71.jpg)
 Qtum Testnet Faucet

# Testnet on the Qtum Web Wallet

Select Settings – Network – Testnet https://qtumwallet.org/

Select the network (Testnet or Mainnet) **before** restoring from a key file and entering the password.

## Testnet on the Qtum Core wallet

1. Download and install the Qtum Core wallet for Mac, Linux or Windows from https://qtumeco.io/wallet or for all versions from https://github.com/qtumproject/qtum/releases. See the user documentation for wallets at https://docs.qtum.site/

2. Launch the wallet on Testnet

You can launch the wallet on Testnet by using the "`-testnet`" command line parameter on startup.

The Qtum Testnet data directories are:

* On macOS/OS X: ~/Library/Application Support/Qtum/testnet3
* On Linux: ~/.qtum/testnet3
* On Windows: %APPDATA%\Qtum\testnet3

## macOS

Using Apple macOS, to launch the qtum-qt GUI wallet on Testnet use Terminal and change directory to the Qtum app and launch the wallet with the `--testnet` parameter, using these commands:

```
cd /Applications/Qtum-Qt.app/Contents/MacOS
./Qtum-Qt --testnet
```

![2 MacQtum-Qt--testnet](https://user-images.githubusercontent.com/29760787/60820453-718cb780-a16f-11e9-849c-449b960ce151.jpg) 
./Qtum-Qt --testnet

## Linux

Using Linux, launch the wallet with "`./qtumd -testnet`" from the bin directory. The command from the home directory is
`~/qtum/qtum-0.17.6/bin/./qtum-qt -testnet`

![3 qtum-qt-testnet Linux](https://user-images.githubusercontent.com/29760787/60820454-718cb780-a16f-11e9-9174-3e1763ca45bf.jpg) 
~/qtum/qtum-0.17.6/bin/./qtum-qt -testnet

The same approach can be used to launch qtumd (the server wallet), using Terminal with change directory to navigate to the bin directory and launch qtumd on Testnet:

![4 qtumd-testnet Linux](https://user-images.githubusercontent.com/29760787/60820441-705b8a80-a16f-11e9-9255-f23c4a911d27.jpg) 
./qtumd -testnet

For qtumd use the Command Line Interface (CLI) qtum-cli to give commands, and for the Testnet wallet use the "`-testnet`" parameter. Here the "`getblockchaininfo`" command is used to verify Testnet:

![5 getblockchaininfoLinux](https://user-images.githubusercontent.com/29760787/60820442-705b8a80-a16f-11e9-996a-71985e859caf.jpg) 
./qtum-cli -testnet getblockchaininfo

## Windows

The Qtum Windows installation includes Startup shortcuts for Mainnet and Testnet (the Testnet shortcut automatically invokes the "`-testnet`" parameter). To launch Testnet on windows for the qtum-qt GUI wallet, click the Testnet app on the Start menu:

![6 WindowsStartMenuTestnet](https://user-images.githubusercontent.com/29760787/60820443-705b8a80-a16f-11e9-9c8c-dc1bdfab0f24.jpg)
Launching qtum-qt for Testnet

To run qtumd for Testnet on Windows, open a command prompt window ("Command Prompt"), change directories to (on 64-bit Windows) C:\Program Files\Qtum\daemon and launch with the command `qtumd.exe -testnet`:

![7 qtumd-testnetWindows](https://user-images.githubusercontent.com/29760787/60820444-705b8a80-a16f-11e9-9f60-bca340316a7e.jpg)
 qtumd.exe -testnet

To use the Command Line Interface, open another Command Prompt window, change directories to Program Files/Qtum/daemon, and enter the commands for qtum-cli with the "`-testnet`" prefix. For example, to confirm Testnet with `qtum-cli.exe -testnet getblockchaininfo`:

![8 getblockchaininfo Windows](https://user-images.githubusercontent.com/29760787/60820445-70f42100-a16f-11e9-839b-cbed6cac9571.jpg) 
qtum-cli.exe -testnet getblockchaininfo

## The configuration file "qtum.conf"

Another way to launch the Core wallet on Testnet is to include "`testnet=1`" in the configuration file "qtum.conf". This file should be located in the Qtum Mainnet data directory, and when the wallet launches it will read the configuration file and startup on Testnet:

![9 ConfFIleTestnet](https://user-images.githubusercontent.com/29760787/60820446-70f42100-a16f-11e9-8128-741bfb739e4a.jpg)  
(here the configuration file is renamed "qtum.conf.txt" for editing and renamed "qtum.conf" after)

# regtest

Regression Test (regtest) is another test blockchain that runs as local blockchain. regtest can be run in a Docker container (https://github.com/qtumproject/documents/blob/master/en/Launch-Qtum-with-Docker.md). To run the Core wallet for regtest on a desktop or server, use the "`-regtest`" parameter to launch as shown in the examples above.

![10 regtestqtum-qt](https://user-images.githubusercontent.com/29760787/60820447-70f42100-a16f-11e9-8652-6c991b56f24a.jpg)
qtum-qt on regtest, mining two blocks a minute

A typical sequence after regtest is launched is to manually create blocks (using the "`generate`" command) and then run tests using transactions created:

![11 regtestgenerate600](https://user-images.githubusercontent.com/29760787/60820448-70f42100-a16f-11e9-83e4-d7dd62bdf42e.jpg) 
generate 600

regtest wallets use the /Qtum/regtest or \Qtum\regtest data directory, have default port 23888, and will be generating Proof of Work blocks with block rewards of 20,000 QTUM for the first 5,000 blocks.

# Testnet Troubleshooting

1. If your new or updated wallet is having trouble making peer connections for Testnet, try the "`addnode`" command with the peers below. The correct response is "null" for qtum-qt or nothing for qtumd, and then the wallet will try for the next few minutes to make the peer connection. Enter one or more of these commands:

```
addnode 35.197.235.28:13888 add
addnode 52.79.250.137:13888 add
addnode 47.89.255.216:13888 add
addnode 120.27.209.201:13888 add
addnode 35.197.132.10:13888 add
```
 
![12 Addnode](https://user-images.githubusercontent.com/29760787/60820449-70f42100-a16f-11e9-8293-b27ba9bb62e3.jpg) 
-testnet addnode 47.89.255.216:13888 add

2. On the Web Wallet see "*Restore from key file failed. Maybe the password is not correct*"

In switching between Mainnet and Testnet with the Web Wallet (Settings – Network), switch networks **before** loading the key file and entering the password.

3. The Testnet Faucet gives "*You can only request tokens once every 24 hours*" on first use or > 24 hours after the previous use.

Click the address bar checkmark button several times until the green confirmation bar appears:

![13 FaucetSuccess](https://user-images.githubusercontent.com/29760787/60820450-70f42100-a16f-11e9-91cc-d06c09db2e23.jpg) 
http://testnet-faucet.qtum.info




