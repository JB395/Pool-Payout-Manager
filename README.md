# PoolPayoutManager.py (PPM)

Copyright (c) 2020 Jackson Belove

Proof of Concept beta software, use at your own risk

MIT License

# About PPM

PPM is a Proof of Concept program to monitor qtumd operating as a 100% fee super staker
(a pool), tracks and makes payouts, sends emails and logs activity.
PPM uses qtum-cli to send CLI queries to the qtumd server application
to identify staking events, and log various activities of the super staker.
PPM sends a query to check for a new block approximately every 4 seconds, but will
wait 5 confirmations before checking a new block (to let orphans settle out).
PPM will require qtumd to be running and staking enabled (decrypted for
staking only), or will stay in an error loop until these two conditions are met.

As a Proof of Concept, PPM uses many global variables and simple (linear search) arrays for data
storage (the delegates and their accumulated payout). Data responses from the node are typically stored
in the global variable "data", which may then be parsed by the main program or various functions. The principal
arrays are delegateArray[] which stores the delegates for this super staker, and poolShareArray[] which
stores the payout accrued by each block reward for the delegate. Delegate payouts must reach a minimum of 
0.001 QTUM, (configurable) or else they are carried over to accrue in the next period.

# Pay Per Mature UTXO (PPMU)

Delegated addresses accrue payout for each pool block reward based on their address’s mature UTXOs (weight)
of minimum size accepted by the pool, divided by the overall pool weight for that block reward.
Individual pool members may add or remove UTXOs from their delegated address at any time, join
or leave the pool at any time, and all pool members are be treated fairly according to the mature
UTXOs staking for each block.

# qtumd launch parameters (pool)
```
./qtumd -testnet -superstaking -stakingminfee=100 -stakingminutxovalue=25 -txindex -reservebalance=1500
```
# Path and folders

qtumd and PPM do not require any path setup. These files should be located
in the same directory/folder, and both qtumd and PPM run from that directory.
PPM will write the log files and block number pool share files to subdirectories
as shown.

## Directory configuration

```
└─┬─ thisDirectory                          # working directory for PoolPayoutManager
  ├─── qtumd                                # daemon wallet executable
  ├─── qtum-cli                             # command line interface executable
  ├─── PoolPayoutManager.py                 # this Python script
  ├─── currentpoolshare.csv                 # file with all the delegates and their current pool share
  ├─── PPMConfig.txt                        # configuration file for PPM
  │ 
  ├──┬─ logs                                # log with new file name each day (GMT)
  │  ├─── PPM_Log_04_Aug_2020.csv
  │  ├─── PPM_Log_05_Aug_2020.csv
  │  ├─── PPM_Log_06_Aug_2020.csv
  │  └─── etc.
  │
  └─┬─ poolshare                            # block number pool share files
    ├─── 651302poolshare.csv                # the "current" pool share after each pool block reward
    ├─── 651352poolshare.csv
    ├─── 651357poolshare.csv
    └─── etc.
```

A note on the terminology for "stake" and "staking". Strictly speaking, the
"stake" is the quantity of QTUM that your wallet selects to "send" to the 
blockchain when the wallet is randomly chosen to receive a block
reward. The wallet will choose one or more UTXOs (previous discrete transactions
received by the wallet), to commit to the stake. This amount of QTUM is "staked"
for 501 blocks, and is subtracted from the wallet's ongoing
staking weight for the 501-block interval. At the end of 501 blocks, the staked
UTXO matures, and that stake ends.

The wallet can be "staking" and decrypted for "staking", but there is only a
"stake" defined during the block reward period. Just because the wallet is
staking doesn't mean it currently has a stake. In the code and comments below,
"stake" refers to the quantity of QTUM "staked" during the block reward period,
and "staking" refers to the mode of the wallet to evaluate UTXOs fo consensus and
publish the next block, receiving the block reward.

For the wallet configured as a super staker the wallet holds a set of UTXOs to commit
stakes when it finds a kernel (reaches consensus to publish the next block and win
the block reward) for either delegated address UTXOs or its own UTXOs. 

While this code began for Qtum Skynet in summer 2017, command responses show
super staking version 0.19.1 from summer 2020.

Because of orphan blocks, the PPM looks at blocks "orphanDelay" late, giving the blockchain
time to resolve forks and valid headers that are not accepted on mainnet. If immediately
detecting each new block, the staker will accept its new blocks even if they turn out to
be orphans. This could lead the pool to recognize more block reward payments than the reality
(because orphan blocks and block rewards are cancelled out). PPM uses delayedBlock and
delayedOldBlock to manage the delay and various functions work with the delayedBlock.

Email alerts may be enabled for various events and hourly updates. The PPM configuration
file provides two emails addresses and selection between them using "setDomestic" to
select a domestic or international email. These emails may be sent to an SMS gateway,
depending on your mobile provider. There is also an array doNotDisturb[] that allows
hourly stopping of emails (for overnight do not disturb). The email account is from
Gmail, with setup instructions given in the file "Gmail Device Password Setup".

# To Add

* Config file add something about payout interval, day/time, etc.
* Recovery if wallet is locked and then unlocked, recovery from error state
* Have send_email() return a string of the actual email sent (or not if during a do not disturb period) so that the display is correct
* Better recovery for loss of network connection (alerts on low connections now)    

# Logging

A log is written as comma separated values (.csv) for easy importing into Excel.
The log filename is changed daily at 0000 GMT, and has the name PPM_Log_DD_MMM_YYYY.csv.
The first column of the log file has these reference numbers:

000 Startup and system messages
100 New block received
200 End of the day
300 Payouts
400 Block reward, staking actions
500 
600
700
800 Missed block (commented out)
900 Errors

Example
```
000,Program,start,or,restart,version,2020-08-06
000,Logging,start,_2232,hours,GMT,06_Aug2020
000,unix time, date time, block, balance, stake, weight, net weight, del weight, num del,
     connections, staking, expected Hours, staker, staker reward, delegate, delegate reward,
     percent, mypool, pool balance, debug extra
000,Program,start,or,restart,version,2020-08-06
000,Logging,start,_2243,hours,GMT,06_Aug2020
100,1596753827,18:43:47,650817,2487856.7,0.0, 2358532.5,4678088,-129324,57,10, yes,0.0,
     qYGvbBDDmYWcHXG2omsHoRDUheB4FN5CsR,4.000,qU12Fa5RHM535kSDvywxPjCmbL7gwkQJZ6,0.000,100,no,277.390,prevoutStakeN 1
100,1596753892,18:44:52,650818,2487856.7,0.0, 2358532.5,4667365,-129324,57,10, yes,0.0,
     qS3MvbBY8y8xNZx2GVyMEdnQJTCPWoPLUR,4.000,none,0.000,nan,no,277.390,
```  
# Console

PPM prints to a local console for delayed blocks and messages.

![Console](https://user-images.githubusercontent.com/29760787/91210410-2e770600-e6db-11ea-8021-16d6cbb3770c.png)

# Program Summary

## Functions

* send_email()
  * send if doNotDisturb = False, send queued messages
  * else queue the message to send later

* parse_number(), parse_alphanum() and parse_logical()
  *  decode various types of text data

* get_weight_for_delegate()
  * compute the mature weight of a delegate for UTXOs >= minimum size

* get_delegations_for_staker()
  * get the current delegations for the staker. 
  * Called if the pool wins that block reward. Calls get_weight_for_delegate() to calculate the
    pool share for each delegate for that block reward.

* get_delegate_count()
  * lightweight version of get_delegations_for_staker(). 
  * Called at program startup and with each new block to update delegates.

* read_current_pool_share_file()
  * reads the current pool share file (the accrued payout for each delegate) on startup.

* write_current_pool_share_file()
  * Writes the delegate array with the payout for each delegate based on their weight. 
  * Written after each block reward. Also writes the same data as a block number file to the /poolshare subdirectory for archive.

* b58encode_int()
  * base 58 encode a hexadecimal integer, used for making a Qtum address

* pubkey_to_base58()
  * convert a Qtum public key to base 58 address. Used to identify the Qtum address of the delegate winning a block reward.

* read_config_file()
  * Read the configuration file PPMConfig.txt

* payout_with_sendmany()
  * Read out the block number files to sum the poolshare for each delegate (current or past). 
  * Format a "sendmany" command (or commands) to pay out the pool.
  * Summed pool shares below a minimum are carried over to the next period.

* log()
  * write to the log file
    
* get_block()
  * get the blockhash and block data
    
* unlock_for_staking_only()
  * unlock the wallet for staking only
    
* unlock_for_sending()
  * fully unlock for sending coins, for payout
    
## Program Synopsis

```
read configuration file
read currentpoolshare.csv file
Initialize log file
make sure qtumd is running
    if not, send alert and wait for qtumd to start

main program loop
    qtum-cli -getinfo 
    qtum-cli getstakinginfo 
    make sure qtumd is staking 
        if not, send alert and wait for staking to be enabled
    format all the data
    send out alert if found:
        new block reward
        blocks getting stale (no new block in 30 minutes)
    send an hourly status email
        send queued messages if noNotDisturb == False
    for a new block
        log it
        check for a skipped block, backup and get it
    get the staker and delegates
    if a block reward for delegates of this staker
        get_delegates_for_staker
            get_weight_for_delegate
            identify any new delegates and add to the arrays
            update the pool share array
            write the currentpoolshare.csv file
            write the block number poolshare.csv file
    wait here, 4 seconds from last block        
    new block waiting loop
        qtum-cli getblockchainheight
        if new block, exit new block waiting loop
        Check for stale blocks
        Date and Hours waiting loop, after a new block wait 4, 8, 12... seconds
            wait 0.3 second
            check the time, if a new day (UTC)
                open new log file
                payout_with_sendmany()
            check the time, if xx:59:56 set to do hourly email and exit new block waiting loop# Offline Staking
```
# Error Message

2020-07-05T17:56:14Z : You need to rebuild the database using -reindex
to change -addrindex.

Please restart with -reindex or -reindex-chainstate to recover.

You need to rebuild the database using -reindex to change -addrindex.
Please restart with -reindex or -reindex-chainstate to recover.

