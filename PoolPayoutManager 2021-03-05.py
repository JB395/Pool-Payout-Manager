version = "2021-03-07"
'''
PoolPayoutManager.py (PPM)

Copyright (c) 2021 Jackson Belove
Proof of Concept beta software, use at your own risk
MIT License
          
PPM is a Proof of Concept program to monitor qtumd operating as a 100%
fee super staker (a pool), tracks and makes payouts, sends emails and
logs activity. PPM uses qtum-cli to send CLI queries to the qtumd server
application to identify staking events, and log various activities of
the super staker. PPM sends a query to check for a new block approx-
imately every 4 seconds, but will wait 5 confirmations before checking
a new block (to let orphans settle out). PPM will require qtumd to be
running and staking enabled (decrypted for staking only), or will stay
in an error loop until these two conditions are met.

As a Proof of Concept, PPM uses many global variables and simple
(linear search) arrays for data storage (the delegates and their
accumulated payout). Data responses from the node are typically stored
in the global variable data, which may then be parsed by the main
program or various functions. The principal arrays are delegateArray[]
which stores the delegates for this super staker, and poolShareArray[]
which stores the payout accrued by each block reward for each delegate.
Delegate payouts must reach a minimum of 0.001 QTUM (configurable),
or else they are carried over to accrue in the next period.

Pay Per Mature UTXO (PPMU)

Delegated addresses accrue payout for each pool block reward based on
their address’s mature UTXOs (weight) of minimum size accepted by the
pool, divided by the overall pool weight for that block reward.

Individual pool members may add or remove UTXOs from their delegated
address at any time, join or leave the pool at any time, and all pool
members are be treated fairly according to the mature UTXOs staking
for each block.

qtumd launch parameters (pool)

./qtumd -testnet -superstaking -stakingminfee=100 -stakingminutxovalue=25 -txindex -reservebalance=1500

Path and folders

qtumd and PPM do not require any path setup. These files should be
located in the same directory/folder, and both qtumd and PPM run from
that directory. PPM will write the log files and block number pool
share files to subdirectories as shown.

Directory configuration

└─┬─ thisDirectory                  # working dir for PoolPayoutManager
  ├─── qtumd                        # daemon wallet executable
  ├─── qtum-cli                     # command line interface executable
  ├─── PoolPayoutManager.py         # this Python script
  ├─── currentpoolshare.txt         # file with all the delegates and
  │                                 #   their curent pool share 
  ├─── PPMConfig.txt                # configuration file for PPM
  │ 
  ├──┬─ logs                        # new file name each day (GMT)
  │  ├─── PPM_Log_2020_Aug_04.csv
  │  ├─── PPM_Log_2020_Aug_05.csv
  │  ├─── PPM_Log_2020_Aug_06.csv
  │  └─── etc.
  │
  └─┬─ poolshare                    # block number pool share files
    ├─── 651302poolshare.csv        # the "current" pool share after
    ├─── 651352poolshare.csv        #   each pool block reward
    ├─── 651357poolshare.csv
    └─── etc.

A note on the terminology for "stake" and "staking". Strictly speaking,
the "stake" is the quantity of QTUM that your wallet selects to "send"
to the blockchain when the wallet is randomly chosen to receive a block
reward. The wallet will choose one or more UTXOs (previous discrete
transactions received by the wallet), to commit to the stake. This
amount of QTUM is "staked" for 501 blocks, and is subtracted from
the wallet's ongoing staking weight for the 501-block interval. At
the end of 501 blocks, the staked UTXO matures, and that stake ends.

The wallet can be "staking" and decrypted for "staking", but there is
only a "stake" defined during the block reward period. Just because the
wallet is staking doesn't mean it currently has a stake. In the code and
comments below, "stake" refers to the quantity of QTUM "staked" during
the block reward period, and "staking" refers to the mode of the wallet
to evaluate UTXOs for consensus and publish the next block, receiving
the block reward.

For the wallet configured as a super staker the wallet holds a set of
UTXOs to commit stakes when it finds a kernel (reaches consensus to
publish the next block and win the block reward) for either delegated
address UTXOs or its own UTXOs. 

While this code began for Qtum Skynet in summer 2017, command
responses show super staking version 0.19.1 from summer 2020.

Because of orphan blocks, the PPM looks at blocks "orphanDelay" late,
giving the blockchain time to resolve forks and valid headers that are
not accepted on mainnet. If immediately detecting each new block, the
staker will accept its new blocks even if they turn out to be orphans.
This could lead the pool to recognize more block reward payments than
the reality (because orphan blocks and block rewards are cancelled out).
PPM uses delayedBlock and delayedOldBlock to manage the delay and
various functions work with the delayedBlock.

Email alerts may be enabled for various events and hourly updates. The
PPM configuration file provides two emails addresses and selection
between them using "setDomestic" to select a domestic or international
email. These emails may be sent to an SMS gateway, depending on your
mobile provider. There is also an array doNotDisturb[] that allows
hourly stopping of emails (for overnight do not disturb). The email
account is from Gmail, with setup instructions provided.

To Add

Remove double pool block on startup
Remove delegates with zero weight from the arrays, unless they have
carrover value.

Config file add something about payout interval, day/time, etc.
Recovery if wallet is locked and then unlocked, recovery from error state
Have send_email() return a string of the actual email sent (or not if during
    a do not disturb period) so that the display is correct
Better recovery for loss of network connection (alerts on low connections now)

An Error Message

2020-07-05T17:56:14Z : You need to rebuild the database using -reindex
to change -addrindex.
Please restart with -reindex or -reindex-chainstate to recover.
: You need to rebuild the database using -reindex to change -addrindex.
Please restart with -reindex or -reindex-chainstate to recover.

Revisions

2020-09-17 Renamed log files YYYY_MMM_DD so they list sequentially
2020-09-16 Bug fixes, divide by zero check, currentpoolshare file to .txt
2020-09-14 Adding 4 trys for all CLI calls
2020-09-05 Fixed delegate address for public key
2020-08-25 Cleaned up emails
2020-08-23 Adding unlock_for_sending(), unlock_for_staking_only() and
             lock_wallet()
2020-08-19 Began adding parse_coinstake()
2020-08-17 Begin fixing orphans, adding orphanDelay = 5 and delayedBlock
2020-08-13 moved logging to a function
2020-08-11 added catchup mode, to read all blocks from currentpoolshare
             file, if desired
2020-08-10 added poolRevenue to track fees and self block rewards
2020-08-07 added payout_with_sendmany()
2020-08-06 moved write log file to "logs" subdirectory
2020-08-02 update arrays for new delegate
2020-07-31 Broke out read_config_file(), added more parameters and
             some error checking
2020-07-29 Adding delegates, updating delegateArray[]
2020-07-21 Added b58encode_int() and pubkey_to_base58() for pubkey
             addresses.
2020-07-20 Updated logging
2020-07-19 Added staker and delegate block rewards,
             get_delegate_count() (just a count)
2020-07-15 Added get_weight_for_delegate()
2020-07-15 Add get_delegations_for_staker()
2020-07-12 Identify miner, block reward, calculate delegatedWeight
             = weight - balance
2020-07-11 Added OSPrefix, OSDataIncr, testnet switch and
             encoding="latin-1" to read config file
2020-07-05 Added start parameter to parse_number()
2020-07-05 Repurposed from QtumMon

Logging

A log is written as comma separated values (.csv) for easy importing
into Excel. The log filename is changed daily at 0000 GMT, and has the
name PPM_Log_YYYY_MMM_DD.csv. The first column of the log file has
these reference numbers:

000 Startup and system messages
100 New block received
200 End of the day
300 Payouts
400 Block reward, staking actions
500 
600
700
800
900 Errors

Example
000,Program,start,or,restart,version,2020-08-06
000,Logging,start,_2232,hours,GMT,06_Aug2020
000,unix time, date time, block, balance, stake, weight, net weight, del weight, num del,
     connections, staking, expected Hours, staker, staker reward, delegate, delegate reward,
     percent, mypool, pool balance, debug extra
000,Program,start,or,restart,version,2020-08-06
000,Logging,start,_2243,hours,GMT,06_Aug2020
000,unix time, date time, block, balance, stake, weight, net weight, del weight, num del,
     connections, staking, expected Hours, staker, staker reward, delegate, delegate reward,
     percent, mypool, pool balance, debug extra
100,1596753827,18:43:47,650817,2487856.7,0.0, 2358532.5,4678088,-129324,57,10, yes,0.0,
     qYGvbBDDmYWcHXG2omsHoRDUheB4FN5CsR,4.000,qU12Fa5RHM535kSDvywxPjCmbL7gwkQJZ6,0.000,100,no,277.390,prevoutStakeN 1
100,1596753892,18:44:52,650818,2487856.7,0.0, 2358532.5,4667365,-129324,57,10, yes,0.0,
     qS3MvbBY8y8xNZx2GVyMEdnQJTCPWoPLUR,4.000,none,0.000,nan,no,277.390,

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

Program Summary

Functions

send_email()
    send if doNotDisturb = False, send queued messages
    else queue the message to send later

parse_number(), parse_alphanum() and parse_logical()
    decode various types of text data

get_weight_for_delegate()
    compute the mature weight of a delegate for UTXOs >= minimum size

get_delegations_for_staker()
    get the current delegations for the staker. Called if the pool wins 
    that block reward. Calls get_weight_for_delegate() to calculate the
    pool share for each delegate for that block reward.

get_delegate_count()
    lightweight version of get_delegations_for_staker(). Called at 
    program startup and with each new block to update delegates.

         1          2         3         4         5         6        7   
123456789012345678901234567890123456789012345678901234567890123456789012

read_current_pool_share_file()
    reads the current pool share file (the accrued payout for each
    delegate) ??? on startup.

write_current_pool_share_file()
    Writes the delegate array with the payout for each delegate based
    on their weight. Written after each block reward. Also writes the
    same data as a block     number file to the /poolshare subdirectory
    for archive.

b58encode_int()
    base 58 encode a hexadecimal integer, used for making a Qtum address

pubkey_to_base58()
    convert a Qtum public key to base 58 address. Used to identify the
    Qtum address of the delegate winning a block reward.

read_config_file()
    Read the configuration file PPMConfig.txt

payout_with_sendmany()
    Read out the block number files to sum the poolshare for each
    delegate (current or past). Format a "sendmany" command
    (or commands) to pay out the pool. Summed pool shares below a
    minimum are carried over to the next period.

log()
    write to the log file
    
get_block()
    get the blockhash and block data
    
unlock_for_staking_only()
    unlock the wallet for staking only
    
unlock_for_sending()
    fully unlock for sending coins, for payout

parse_coinstake()
    parse the coinstake transaction to find addresses and rewards
    
Program Synopsis

read configuration file
read currentpoolshare.txt file
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
            write the currentpoolshare.txt file
            write the block number poolshare.csv file
    wait here, 4 seconds from last block        
    new block waiting loop
        qtum-cli getblockchainheight
        if new block, exit new block waiting loop
        Date and Hours waiting loop, after a new block wait 4, 8, 12... seconds
            wait 0.3 second
            check the time, if a new day (UTC)
                open new log file
                payout_with_sendmany()
            check the time, if xx:59:56 set to do hourly email and exit new block waiting loop

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

oldBlock = 0            # the block last time it changed
stake = 0               # for startup
sendOneTimeQtumdOffline = False   # send an alert once if qtumd is offline
qtumdIsRunning = False  # set this on startup
labelsPrintedAtStartup = False  # print the label row once at startup
logNewBlock = False     # set to log new block
blocksToday = 0         # new blocks today, accurate if PPM running 24 hours+
savedUnixBlockTime = 0  # for time since last block
sendOneTimeNotStaking = False  # will check below if staking

didNewHour = False      # switch to allow a few seconds to detect the hour change
didNewLog = False       # did we just detect a UTC day change and opened a new log file
sendLowConnectionsAlert = False # send an alert for low connections
lowConnectionsAging = 0 # age the low connections alert to only send again after 7 blocks
staleBlockAging = 0     # age the stale block alert to only send again after 15 minutes
config_file_name = "PPMConfig.txt" # name of configuration file
firstTimeThrough = True # the first time through, do/don't do certain things
delayBlockWaiting = 3   # set on 10/14/2017, delay in seconds for the block waiting loop
                        # this parameter is critical for setting the delay until the next
                        # block check immediately after a new block is found
delayDateHours = 3.36   # set to 3.86 on 10/13/2017, 4 second delay, delay in seconds for the loop that detects date and hour change
                        # set to 3.36 on 10/15/2017 because still missing 4 second blocks

printBlockMod10 = True  # toggle to print the labels every 10 blocks
justOneTime = True      # toggle, just one time

from binascii import unhexlify         # for pubkey to base58
import hashlib                         # for pubkey to base58

arraySize = 5000                                    # size of arrays for delegates, weights and shares      

delegateArray = ["" for i in range(arraySize)]      # Qtum address
weightArray = [0 for i in range(arraySize)]         # integer Satoshis
poolShareArray = [0 for i in range(arraySize)]      # integer Satoshis

updateDelegateArray = ["" for i in range(arraySize)]    # to update delegateArray[]
updateWeightArray = [0 for i in range(arraySize)]       # to update weightArray[]
updatePoolShareArray = [0 for i in range(arraySize)]    # to update poolShareArray[]

orphanDelay = 5             # delay before reading blocks to allow orphans to be resolved
strBlockTime = ""           # time read from block

rightSideExtra = ''     # extra data to print on right side of row for debugging
stakerReward = 0.0          # to get started
isPoolBlockReward = False   # to get started
maturity = 500              # confirmations for maturity, used by get_weight_for_delegate()
intsatsPoolBalance = 0      # block reward balance of pool, integer Satoshis
delegateCount = 0           # on startup, set in read_current_pool_share_file()
intsatsSendmanyMinimum = -1 # on startup, set in the configuration file
block = 0                   # set on startup
delayedBlock = 0            # set on startup
intsatspoolRevenue = 0.0    # revenue for the pool, this payout interval
                            # = pool fee + self block rewards

currentpoolshareFilename = "currentpoolshare.txt"       # file name for the current pool shares

myWalletPassphrase = "insecurePassphrase"  # so insecure

MAINNETPREFIX = "3a"            # hexadecimal, for pubkey_to_base58
TESTNETREGTESTPREVIX = "78"     # hexadecimal, for pubkey_to_base58

# 58 character alphabet used, for b58encode_int()
'''
BITCOIN_ALPHABET = \
    b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
'''    
BITCOIN_ALPHABET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
# Retro compatibility, for b58encode_int()
alphabet = BITCOIN_ALPHABET

# labels for the display and log
#           123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
labelRow = "   time  │   block  │   balance   │   stake   │    weight   │ net weight │  del weight  │ # del │" +\
           " con │ stkg │ exphr │ staker │ stk rwd │ delgte │ del rwd │" +\
            " pct │ mypool │  pool bal │ debug extra"
           
logLabels = '000, unix time, date time, block, balance, stake, weight, net weight, del weight, num del, connections, staking, expected Hours, staker, staker reward, delegate, delegate reward, percent, mypool, pool balance, debug extra'

import subprocess
import time
from time import localtime, strftime, sleep
from datetime import datetime
import smtplib                          # email sending function
from email.mime.text import MIMEText    # for email formatting
import os, sys                          # for file operations
from timeit import default_timer as timer
from array import *                     # for arrays
from binascii import unhexlify          # for pubkey to base58
import hashlib                          # for pubkey to base58
import urllib.request                   # for reading Web sites, Python 3
from urllib.request import Request, urlopen
import urllib.request as urlRequest
from urllib.error import URLError, HTTPError    # for URL errors

# doNotDisturb[] gives the hours when emails will not be sent. 
# times given in GMT as follows, 0000 = 12 midnight, 2300 = 11:00 pm, etc.
# Enter the do not disturb hours here in GMT, and they will be
# converted to the local time zone by the configuration file parameter
# UTCTimeOffset. Enter a "1" in the array to suppress emails during
# that hour. For example, to suppress emails for 0800 hours, enter a "1"
# in the 9th element of the array, which is doNotDisturb[8]. UTCTimeOffset
# will convert this time to 0800 hours local time.
#
#  0000,  0100,  0200,  0300,  0400,  0500,  0600, 0700
#  0800,  0900,  1000,  1100,  1200,  1300,  1400, 1500
#  1600,  1700,  1800,  1900,  2000,  2100,  2200, 2300
#

doNotDisturb=array('b',\
    [1, 1, 1, 1, 1, 1, 1, 0,\
     0, 0, 0, 0, 0, 0, 0, 0,\
     0, 0, 0, 0, 0, 0, 0, 1])

# need to send email info in two pieces (subject and message), the subject will be truncated

def send_email(subjectText, messageText):

    "Send an email to an address which may be an email-to-text address for mobile operator"

    # if in a doNotDisturb hour, do not send this email
    # can get here up to 4 seconds early for the new hour, so make some adjustment here
    # to index into the current (or immediately upcoming) hour for doNotDisturb[]

    global doNotDisturbQueue

    unixTime = int(time.time())
    unixTimeEarly = unixTime + 4    # allow 4 seconds of being early

    UTCHour = int((unixTimeEarly % 86400) / 3600) # 0..23, no half hour time zones
    localHour = UTCHour + UTCTimeOffset
    
    if localHour > 23:
        localHour -= 24
    elif localHour < 0:
        localHour += 24

    # print("localHour =", localHour, "doNotDisturb =", doNotDisturb[localHour])

    if doNotDisturb[localHour] == 0:                # go ahead and send email

        '''
        example message sent from doNotDisturbQueue after do not disturb ends:

        1 of 9
        FRM:mygmail@gmail.com
        SUBJ:.REWARD
        MSG:..LD18 blk 792772 stk 7841.1 
        22:19:48.REWARD.LD18 blk 792555 stk 6286.8 
        22:28:37.REWARD.LD18
        (Con't) 2 of 9
        blk 792559 stk 6106.8 
        00:00:06.REWARD.LD18 blk 792601 stk 5534.0 
        00:15:03.REWARD.LD18 blk 792606 stk 5534.0 
        00:53:53.REWARD.LD18
        (Con't) 3 of 9
        blk 792622 stk 5650.2 
        01:01:25.REWARD.LD18 blk 792628 stk 6146.3 
        01:06:28.REWARD.LD18 blk 792629 stk 6146.3 
        01:14:59.REWARD.LD18
        (Con't) 4 of 9
        blk 792633 stk 6285.3 
        01:21:10.REWARD.LD18 blk 792636 stk 6285.3 
        01:40:37.REWARD.LD18 blk 792649 stk 6429.7 
        02:07:51.REWARD.LD18
        <snip>
        '''

        if len(doNotDisturbQueue) > 0:             # had some messages queued, add them
            messageText += '\n'
            messageText += doNotDisturbQueue 
            doNotDisturbQueue = ''                  # clear out for next time
       
        msg = MIMEText(messageText)                     # use as message

        server = smtplib.SMTP('smtp.gmail.com:587')
        msg['Subject'] = subjectText                    # email subject
        msg['From'] = emailAddress                       # from: email address
        msg['To'] = toAddress                           # to: email address
        server.starttls()
        time.sleep(0.05)
        server.login(emailUsername, emailPassword)
        time.sleep(0.05)
        # server.set_debuglevel(1)
        server.sendmail(emailAddress, toAddress, msg.as_string())
        time.sleep(0.05)
        server.quit()
        time.sleep(0.05)

    else:                 # queue up the message for when doNotDisturb is over
        if sendEmailForNewHour != True:   # but don't queue up hourly status messages
            now = datetime.now()
            current_timeHMS = now.strftime("%H:%M:%S")
            doNotDisturbQueue += current_timeHMS + subjectText + messageText + '\n'
            # print("doNotDisturbQueue =", doNotDisturbQueue)
            
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def parse_number(field, start, offset, lenData, periodAllowed):
    '''
    parse the global variable "data" which is the response from qtum-cli calls.
    Search for the text "field" from "start", then get the digit characters starting 
    "offset" characters from the start of the field, and search through at
    least "lenData" characters, and accept a period "." if "periodAllowed"
    is True.
    
    For example, to find the balance from the qtum-cli command -getinfo:
                       periodAllowed = True
                       v
    ..."balance": 14698.3456000, \r\n...
                  ^    
                  offset = 10 characters from start of balance
    '''
    global data
   
    temp = ''
	
    dataIndex = data.find(field, start, lenData)

    # print("dataIndex =", dataIndex)

    i = dataIndex + offset  	# point at the first digit
	
    if dataIndex > 0:  # found field
        
        while i <= lenData - 1:

            if data[i] >= "0" and data[i] <= "9":
                temp += data[i]
            elif data[i] == "." and periodAllowed == True:  # if period allowed
                temp += data[i]
            elif data[i] == ",":
                break
            elif (i == dataIndex + offset) and (data[i] == "-"):  # allow negative sign
                temp += data[i]                                   # first character only
            else:  # how to find \r at end of response, like for estimated time?
                # print("PPM error, bad character in ", field)
                break
                    
            i += 1	
            if i >= lenData:
                break
            
        return(temp)
            
    else:
        return(-1)      # an error

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# parse alphanumeric text like "True", "xyz@gmail.com" and "HP8200"

def parse_alphanum(field, offset, lenData):
    # parse against the global variable "data"
    
    global data
    
    temp = ''
    
    dataIndex = data.find(field, 0, lenData)
    
    i = dataIndex + offset  	# point at the first digit
	
    if dataIndex > 0:  # found field
        # allow characters 0..9, @..Z, a..z
        while i <= lenData - 1:

            # print("data[i] = ", data[i])
            
            if (data[i] >= 'a' and data[i] <= 'z') or +\
               (data[i] >= '@' and data[i] <= 'Z') or +\
               (data[i] >= '0' and data[i] <= '9') or +\
               (data[i] == '.') or +\
               (data[i] == '-'):
                temp += data[i]
            elif data[i] == "," or data[i] == "'\'":     # for -getinfo proof-of-stake
                break
            else:
                break
                    
            i += 1
                    
            if i >= lenData:
                break
        return(temp)
            
    else:
        return(-1)   # an error
        
def parse_logical(field, offset, lenData):
    # parse against the global variable "data"

    global data
    
    temp = ''
    
    dataIndex = data.find(field, 0, lenData)
    
    i = dataIndex + offset  	# point at the first digit

    if dataIndex > 0:  # found field
        while i <= lenData - 1:
            if data[i] >= 'a' and data[i] <= 'z':
                temp += data[i]
            elif data[i] == ",":
                break
            else:
                print("PPM error, bad character in ", field)
                break
                    
            i += 1
                    
            if i >= lenData:
                break    

        # print("field =", field, "temp =", temp)
        
        if temp == "true":
            return(True)
        elif temp == "false":	
            return(False)
 
    else:
        return(-1)   # an error

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_weight_for_delegate(delegate):
    # get the weight for a delegate, UTXOs that meet maturity and minimum size

    global maturity             # confirmations for maturity
    global orphanDelay          # lag for delayedBlock
    global minimumUTXOSize      # minimum UTXO size in QTUM to be staked

    start = timer()

    # print("  ")
    # print("delegate is ", delegate)

    # get the UTXOs for this delegate address

    # Use escape characters for \ \\ and " \", 
    # qtum-cli -testnet getaddressutxos "{\"addresses\":[\"qSniZkfaj9wrzPyFiDuabk723z76xYMNRg\",\"qeD75i7DWjXrd77PsyXKn1akv7RJqYAJ5m\"],\"chainInfo\":true}"

    params = OSPrefix + "qtum-cli " + testnet + "getaddressutxos \"{\\\"addresses\\\": [\\\"" + delegate + "\\\"],\\\"chainInfo\\\": true}\""

    # print(params) # qtum-cli -testnet getaddressutxos "{\"addresses\": [\"qMUR738THXBXABfx1Rk6iWtiStEPtQKWYK\"],\"chainInfo\": true}"

    # sys.exit()

    tryNo = 0

    while True:
        
        try:
            result = str(subprocess.check_output(params, shell = True))
            break
        
        except:
            print("ERROR, get_weight_for_delegate() - no response from qtumd, try =", tryNo + 1)
            tryNo += 1
            time.sleep(tryNo * 0.3)
            
            if tryNo >= 4:
                print("No response from qtumd, exiting")
                sys.exit()

    moreData = str(result)

    # print(moreData)

    lenMoreData = len(moreData)
    # print("lenMoreData =", lenMoreData)

    '''
    [
      {
        "address": "qMUR738THXBXABfx1Rk6iWtiStEPtQKWYK",
        "txid": "8a5215e6093d2fb416fb7672588a1bcdd5aa0a2dab61cce940367fb96b4c88ee",
        "outputIndex": 1,
        "script": "21039b33555fe9dcb13c8585034715555e4f40ad7bc12723c46d5e476dfebba345a2ac",
        "satoshis": 11873510800,
        "height": 633480,
        "isStake": true
      },
      {
        "address": "qMUR738THXBXABfx1Rk6iWtiStEPtQKWYK",
        "txid": "fca9618d3dbeb97a57ca2eea7b590b913d5e4fb18cbb08b9172e01776b930800",
        "outputIndex": 1,
        "script": "21039b33555fe9dcb13c8585034715555e4f40ad7bc12723c46d5e476dfebba345a2ac",
        "satoshis": 10320182956,
        "height": 633500,
        "isStake": true
      }
      <snip>
      ],
        "hash": "00b0b126368ec34040a285eccd9f050d8d1828c694f06f86b5b630eb0e687696",
        "height": 634785
      }
      
    '''

    # get the current height, get the last "height" in the response

    dataIndex = moreData.find("height", lenMoreData - 50, lenMoreData)

    # print("dataIndex =", dataIndex)

    currentHeight = ''       # current block height

    dataIndex += 9    # fixed offset to start of numbers

    while moreData[dataIndex] >= '0' and moreData[dataIndex] <= '9':  # a digit
        currentHeight += moreData[dataIndex]
        dataIndex += 1

    # print("currentHeight =", currentHeight)    

    # sys.exit()

    dataIndex = 0

    numTotalUTXOs = 0       # total number of UTXOs evaluated
    sumTotalUTXOs = 0       # total sum of all UTXOs evaluated, this is the only one that matters

    numValidUTXOs = 0       # number of UTXOs that are mature and big enough to stake
    sumValidUTXOs = 0       # delegate weight, sum value of UTXOs that are mature and big enough to stake

    sumTooSmallUTXOs = 0    # sum of UTXOs that are too small to stake (immature or mature)
    numTooSmallUTXOs = 0    # the number of too small UTXOs (immature or mature)

    sumImmatureUTXOs = 0    # sum of the immature UTXOs
    numImmatureUTXOs = 0    # number of immature UTXOs

    minimumSatsValue = minimumUTXOSize * 100000000                  # convert to Satoshis
    matureUTXOHeight = int(currentHeight) - maturity - orphanDelay  # get block height for maturity

    # print("currentHeight =", int(currentHeight), "matureUTXOHeight =", matureUTXOHeight)

    # sys.exit()

    dataIndex = 0           # start from the beginning of the data

    while dataIndex < lenMoreData:

        satoshis = ' '
        height = ' '
        blockHeight = ' '
            
        dataIndex = moreData.find("satoshis", dataIndex)

        # print("dataIndex satoshis =", dataIndex)


        if dataIndex > 0:       # found "satoshis"

            numTotalUTXOs += 1

            dataIndex += 11     # point at the first digit

            while moreData[dataIndex] != ',':
                satoshis += moreData[dataIndex]
                dataIndex += 1

        else:
            break

        # print("satoshis", satoshis)

        # sys.exit()

        # dataIndex should be very close to "height"

        dataIndex = moreData.find("height", dataIndex, lenMoreData)

        # print("dataIndex height =", dataIndex)

        if dataIndex > 0:       # found "height"

            dataIndex += 9      # point at the first digit

            while moreData[dataIndex] != ',':
                height += moreData[dataIndex]
                dataIndex += 1

        else:                   # should not get here
            break

        # print("height", height)

        # sys.exit()        

        sumTotalUTXOs += int(satoshis)
        
        # do not sum immature or too small UTXOs
        
        if int(height) <= matureUTXOHeight and int(satoshis) >= minimumSatsValue:    
                sumValidUTXOs += int(satoshis)
                numValidUTXOs += 1

        else:
            if int(satoshis) < minimumSatsValue:   # too small (immature or mature)
                sumTooSmallUTXOs += int(satoshis)
                numTooSmallUTXOs += 1
            else:                               # must be large enough but immature
                sumImmatureUTXOs += int(satoshis)
                numImmatureUTXOs += 1

        dataIndex += 200                        # advance to next UTXO

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # print("numValidUTXOs =", numValidUTXOs, "sumValidUTXOs =", sumValidUTXOs)
    # print("numImmatureUTXOs =", numImmatureUTXOs, "sumImmatureUTXOs =", sumImmatureUTXOs)
    # print("numTooSmallUTXOs =", numTooSmallUTXOs, "sumTooSmallUTXOs =", sumTooSmallUTXOs)
    # print("numTotalUTXOs =", numTotalUTXOs, "sumTotalUTXOs", sumTotalUTXOs)

    # print("Duration:", format(timer() - start, "0.2f"))

    return(sumValidUTXOs)   # in Satoshis

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_delegations_for_staker(localBlockReward):
    # get the current delegations for this staker

    global myMinerAddress                       # address of this staker
    global data
    global rightSideExtra                       # to print debug info on right side of line

    global delegateArray                        # delegate addresses, set here
    global weightArray                          # delegate weights, set here
    global poolShareArray                       # delegate current pool share, set here

    global updateDelegateArray                  # to update delegateArray[]
    global updateWeightArray                    # to update weightArray[]
    global delegateCount                        # count of delegates that have been active in the current
                                                # payment period, may include addresses that have
                                                # removed their delegation (but have some poolshare
                                                # to pay out

    start = timer()

    updateDelegateCount = 0                     # the number of updated delegates counted, 1 based
    delegatedWeightFromUTXOs = 0                # delegated weight from valid UTXOs
    needToUpdateArrays = False                  # flag for need to update the arrays because
                                                # of insertion or deletion of delegate(s)
    '''
    print("= = before = = = = = = = = = = = = = = = = = = = = =")

    for i in range(delegateCount):
        print("i", i, delegateArray[i], "- - -", poolShareArray[i])
    '''
        
    params = OSPrefix + "qtum-cli " + testnet + "getdelegationsforstaker " + myMinerAddress

    # print(params)
    # qtum-cli -testnet getdelegationsforstaker qPooLFFk2BT3i9yKApjeJhuYjYKWHmuCdq 

    delegate = ""       # clear to see bad response

    # get the delegates for staker - - - - - - - - - - - - - - - - - - - - - - - - - -

    tryNo = 0

    while True:
        
        try:
            result = str(subprocess.check_output(params, shell = True))
            break
        
        except:
            print("ERROR, get_delegates_for_staker() - no response from qtumd, try =", tryNo + 1)
            tryNo += 1
            time.sleep(tryNo * 0.3)
            
            if tryNo >= 4:
                print("No response from qtumd, exiting")
                sys.exit()
            
    # print(result)

    data = str(result)
    lenData = len(data)

    # print(data)

    ''' - - - - - - - delegate data - - - - - - - -
    [
      {
        "delegate": "qUXM5s6exwXZoUQQXSvVeyrGGhoo5ZKCE2",
        "staker": "qPooLFFk2BT3i9yKApjeJhuYjYKWHmuCdq",
        "fee": 100,
        "blockHeight": 633371,
        "PoD": "20a3969d64e0c8b0f3e097b23792f12af9a721e8651f3d5093c559643928158dd310b4f3986571903c450a3b9bc1a42cbd9853ad9b2359a0a8cb5d567a034730e0"
      },
      {
        "delegate": "qVhvEFRtpnaRQbuJiQERQ9zi5N9HxkswQX",
        "staker": "qPooLFFk2BT3i9yKApjeJhuYjYKWHmuCdq",
        "fee": 100,
        "blockHeight": 633325,
        "PoD": "20ffff29890116e539119cd5ce1e374f75c4b93fb235cc6c26a7fa8bd2cbea187f603a11d91a01792c5613571158c7209232ef6d2d4915c6bb379d9f4bb09f366e"
      }, <snip>
    '''    

    # sys.exit(0)

    # get the delegates and fees

    dataIndex = 0
    arrayIndex = 0

    while dataIndex < lenData:

        delegate = ''

        dataIndex = data.find("delegate", dataIndex, lenData)

        # print("dataIndex delegate =", dataIndex)

        if dataIndex > 0:  # found a delegate

            updateDelegateCount += 1

            dataIndex += 12             # fixed offset to start of delegate address

            for i in range(34):
                delegate += data[dataIndex]
                dataIndex += 1

            # print("delegate =", delegate)

        else:
            break                       # done

        # get the fee for this delegate

        fee = ''

        dataIndex = data.find("fee", dataIndex, lenData)

        # print("dataIndex fee =", dataIndex)

        if dataIndex > 0:  # found a fee

            dataIndex += 6              # fixed offset to start of fee

            while data[dataIndex] != ',':
                fee += data[dataIndex]
                dataIndex += 1

            # print("fee =", fee)

        # must meet minimum fee
        # note this summation is for current delegates, not some historical delegates that would
        # presist with values in poolShareArray[]

        if int(fee) >= requiredFee:   # fee is good for this delegate, update weight and share
            delegateWeight = get_weight_for_delegate(delegate) # get the current weight for this delegate
        else:
            delegateWeight = 0   # is this right, or:

            # else skip updating weight and pool share, since the staker may have changed its fee
            # leave any previous pool share (don't zero it out)

        # print(delegateWeight)    

        # check if < 5000
        
        if delegateWeight > 0.0:

            # print("writing array, arrayIndex =", arrayIndex, "delegate =", delegate, "weight =", delegateWeight)
            
            updateDelegateArray[arrayIndex] = delegate              # Qtum address

            updateWeightArray[arrayIndex] = delegateWeight          # integer Satoshis

            # here a delegate was added, or a previous delegate had it's weight change
            # because they added/removed coins or corrected their fee
            # but won't be in the same sequence because of additions, deletions, and carryovers

            if updateDelegateArray[arrayIndex] != delegateArray[arrayIndex] or updateWeightArray[arrayIndex] != delegateArray[arrayIndex]:
                needToUpdateArrays = True   # need to update the arrays, maybe multiple changes
                # print("Found a delegate array change at index =", arrayIndex)

            if updateWeightArray[arrayIndex] != weightArray[arrayIndex]:
                needToUpdateArrays = True   # need to update the arrays, maybe multiple changes
                # print("Found a weight array change at index =", arrayIndex)
                
            arrayIndex += 1

            delegatedWeightFromUTXOs += delegateWeight

        # print("delegate", delegate, "weight", delegateWeight, "delegatedWeightFromUTXOs =", delegatedWeightFromUTXOs)

    updateCount = arrayIndex

    # print("arrayIndex =", arrayIndex)    

    # compute the pool share for each delegate = delegate Weight / delegatedWeightFromUTXOs

    if needToUpdateArrays == True:
        # print("Updating arrays")

        # could get here if the pool got a block reward with a change in delegates

        '''
        Find any added delegates, and add them as the last element to delegateArray[]
        Do not remove any removed delegates because they may have some payout accumulated
        delegateArray[] will be zeroed out and repopulated when by the pool payout
        '''

        for i in range(updateCount):
            try:
                j = delegateArray.index(updateDelegateArray[i])
            except:
                # print("didn't find")
                j = -1

            # print("i =", i, "j =", j, "updateDelegateArray[i] =", updateDelegateArray[i])

            if j < 0:                       # didn't find an update delegate
                print("Adding new delegate =", updateDelegateArray[i])
                # append on end of delegateArray[]
                delegateArray[delegateCount] = updateDelegateArray[i]
                weightArray[delegateCount] = updateWeightArray[i]
                poolShareArray[delegateCount] = 0
                delegateCount += 1
                print("delegateCount =", delegateCount)

            else:
                weightArray[j] = updateWeightArray[i]

        # assumes this update was on a block reward

        # sanity check for divide by zero

        if delegatedWeightFromUTXOs == 0:
            print("ERROR, delegatedWeightFromUTXOs = 0, skipping poolshare update")

        else:
            for i in range(delegateCount):
                poolShareArray[i] += int(round( 100000000 * localBlockReward * weightArray[i] / delegatedWeightFromUTXOs, 0))
                i += 1

        # for i in range(delegateCount):
        #    print("i =", i, delegateArray[i], weightArray[i], poolShareArray[i])

        # print("updateDelgateCount =", updateDelegateCount)

        # write_current_pool_share_file(delayedBlock) # temp 

        duration = timer() - start

        # rightSideExtra = " " + str(delegateCount) + " " + str(delegatedWeightFromUTXOs) + " " + "{:,f}".format(round(duration, 3))[:5]
        # rightSideExtra += " " + str(delegateCount) + " " + "{:,f}".format(round(duration, 3))[:5]

    # print(rightSideExtra)

    '''
    if needToUpdateArrays == True:
        
        print("= = after = = = = = = = = = = = = = = = = = = = = =")

        for i in range(delegateCount):
            print("i", i, delegateArray[i], weightArray[i], poolShareArray[i])
    '''
    
    # sys.exit()    
    
    return()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_delegate_count():
    # count the current delegations for this staker
    # this is a "lite" version of get_delegations_for_staker() for use on program startup and with new blocks
    # and does not compute the weight of each delegate, just counts them. Note that this will could all the delegates
    # assigned to the super staker, even those with fees below the minimum (that would not be currently staking).

    global myMinerAddress                       # address of this staker
    global data

    delegateCount = 0                           # the number of delegates counted, 1 based

    params = OSPrefix + "qtum-cli " + testnet + "getdelegationsforstaker " + myMinerAddress

    # print(params)
    # qtum-cli -testnet getdelegationsforstaker qPooLFFk2BT3i9yKApjeJhuYjYKWHmuCdq 

    delegate = ""       # clear to see bad response

    # get the delegates for staker - - - - - - - - - - - - - - - - - - - - - - - - - -

    tryNo = 0

    while True:

        try:
            result = str(subprocess.check_output(params, shell = True))
            break
        
        except:
            print("ERROR, get_delegate_count() - no response from qtumd, make sure qtumd is fully synced, try =", tryNo + 1)
            tryNo += 1
            time.sleep(tryNo * 0.3)
            
            if tryNo >= 4:
                print("No response from qtumd, exiting")
                sys.exit()

    # print(result)

    data = str(result)
    lenData = len(data)

    # print(data)

    ''' - - - - - - - delegate data - - - - - - - -
    [
      {
        "delegate": "qUXM5s6exwXZoUQQXSvVeyrGGhoo5ZKCE2",
        "staker": "qPooLFFk2BT3i9yKApjeJhuYjYKWHmuCdq",
        "fee": 100,
        "blockHeight": 633371,
        "PoD": "20a3969d64e0c8b0f3e097b23792f12af9a721e8651f3d5093c559643928158dd310b4f3986571903c450a3b9bc1a42cbd9853ad9b2359a0a8cb5d567a034730e0"
      },
      {
        "delegate": "qVhvEFRtpnaRQbuJiQERQ9zi5N9HxkswQX",
        "staker": "qPooLFFk2BT3i9yKApjeJhuYjYKWHmuCdq",
        "fee": 100,
        "blockHeight": 633325,
        "PoD": "20ffff29890116e539119cd5ce1e374f75c4b93fb235cc6c26a7fa8bd2cbea187f603a11d91a01792c5613571158c7209232ef6d2d4915c6bb379d9f4bb09f366e"
      }, <snip>
    '''    

    # sys.exit(0)

    # get the delegates and fees

    dataIndex = 0

    while dataIndex < lenData:

        delegate = ''

        dataIndex = data.find("delegate", dataIndex, lenData)

        # print("dataIndex delegate =", dataIndex)

        if dataIndex > 0:  # found a delegate

            delegateCount += 1

            dataIndex += 12             # fixed offset to start of delegate address

        else:
            break                       # done

    # print("delegateCount =", delegateCount)    
    
    return(delegateCount)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def read_current_pool_share_file():
    # read current pool share file

    global delegateArray
    global poolShareArray
    global intsatsPoolBalance           # integer Satoshis
    global delegateCount
    global intsatspoolRevenue
    global block                        # used in catchupMode
    global delayedBlock                 # used in catchupMode

    '''
    block,674468,poolbalance,475031280,
    poolrevenue,12345678,
    delegate,qHd3raPTT2cbzZUVZUooxSTPNkV6ucRZRc,poolshare,23778728469,
    delegate,qJQfsCpyyZCdvdhNbFcbE2ANm7RxsnuLXZ,poolshare,0,
    delegate,qJTsgyGJ2ez5y5qAMJh3Tk5qTcmNPu3RgC,poolshare,472744239,
    delegate,qJUxKRzm2mfsZEa3u3CTu4UfMdQ1EzVW83,poolshare,14505678469,
    delegate,qJVBqYE4s6hD6WoGt8WjTXBMPSHjPjWRP5,poolshare,972915534,
    '''

    try:
        currentPoolShare = open(currentpoolshareFilename, 'r', encoding="latin-1")  # check for success, if available
        
    except:
        print('Unable to find the current pool file "currentpoolfile.txt", may be initial startup')
        print('The current pool file must be in the same directory with PPM, qtumd and qtum-cli')
        # print("block =", block, "delayedBlock =", delayedBlock)
        return()
        
    fileData = currentPoolShare.read()
    lenData = len(fileData)
    # print("lenData =", lenData)

    currentPoolShare.close()

    # print(fileData)

    # sys.exit()

    # parse the data

    strBlock = ''               # local block
    strsatsPoolBalance = ''     # string Satoshis
    strsatsPoolRevenue = ''     # string Satoshis

    arrayIndex = 0

    dataIndex = fileData.find("block", 0, lenData)

    if dataIndex >= 0:   # found "block"

        dataIndex += 6 # + OSDataIncr1  # fixed offset to start of block digits

        while fileData[dataIndex] != ",":

            strBlock += fileData[dataIndex]
            dataIndex += 1

    delayedBlock = int(strBlock)                # if in catchupMode, start from the next block
    block = delayedBlock + orphanDelay    
    
    # print("delayedBlock", delayedBlock)

    dataIndex = fileData.find("poolbalance", 0, lenData)  

    if dataIndex > 0:   # found "poolbalance"

        dataIndex += 12 # + OSDataIncr1  # fixed offset to start of pool balance

        while fileData[dataIndex] != ",":

            strsatsPoolBalance += fileData[dataIndex]  
            dataIndex += 1

    # print("strsatsPoolBalance =", strsatsPoolBalance)        

    intsatsPoolBalance = int(strsatsPoolBalance)    # convert to int      

    # print("strsatsPoolBalance", strsatsPoolBalance, "intsatsPoolBalance", intsatsPoolBalance)

    dataIndex = fileData.find("poolrevenue", 0, lenData)  

    if dataIndex > 0:           # found "poolrevenue"

        dataIndex += 12         # fixed offset to start of poolrevenue

        while fileData[dataIndex] != "," and fileData[dataIndex] != ".":  # sometimes has a period

            strsatsPoolRevenue += fileData[dataIndex]  
            dataIndex += 1

    # print(strsatsPoolRevenue)

    intsatspoolRevenue = int(strsatsPoolRevenue)    # convert to int

    # print("intsatspoolRevenue", intsatspoolRevenue)

    # loop through and get each delegate and pool share

    while dataIndex < lenData:

        delegate = ''
        poolShare = ''

        dataIndex = fileData.find("delegate", dataIndex, lenData)

        if dataIndex > 0:                   # found a delegate

            dataIndex += 9 # + OSDataIncr1    # fixed offset to start of address

            for i in range(34):
                
                delegate += fileData[dataIndex]

                dataIndex += 1

        else:
            # exits loop from here
            break           # reached the end of the file

        # print("delegate", delegate)

        dataIndex = fileData.find("poolshare", dataIndex, lenData)

        # print("dataIndex =", dataIndex)

        if dataIndex > 0:                   # found a pool share

            dataIndex += 10 # + OSDataIncr1   # fixed offset to start of digits

            while fileData[dataIndex] != ",":

                # print("dataIndex =", dataIndex, "char =", fileData[dataIndex])

                poolShare += fileData[dataIndex]

                if dataIndex < lenData:  # read to EOF

                    dataIndex += 1

        # print("poolShare", poolShare)            

        delegateArray[arrayIndex] = delegate
        poolShareArray[arrayIndex] = int(poolShare)

        # print(delegateArray[arrayIndex], poolShareArray[arrayIndex])
                    
        arrayIndex += 1

    delegateCount = arrayIndex

    # print("read_current_pool_share_file() delegateCount =", delegateCount)

    # sys.exit()

    return()    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -   

def write_current_pool_share_file(localDelayedBlock):
    # write (overwrite) current pool share file
    # and write a block number named pool share file for archive

    global delegateArray
    global poolShareArray

    # global block
    global intsatsPoolBalance
    global delegateCount
    global isLinux
    global rightSideExtra

    # for a new block reward, overwrite the currentpoolshare file and save a
    # block_number named copy in the /poolshares subdirectory (FUTURE)

    # Windows, can set the Z drive, as an Administrator, go to System - Disk Management - All Tasks -
    # Change Drive Letter and Paths

    # print("Not writing curentpoolshare.csf file")
    # return()
        
    try:
        # create or open pool file for writing (overwriting)
        currentPoolShare = open(currentpoolshareFilename, 'w', encoding="latin-1")
        # print("current pool share file open for writing")
        # print("Opening file", currentpoolshareFilename)
        
    except IOError:   # NOT WORKING
        print("ERROR: currentpoolshareFilename file didn't exist, open for appending")

    try:
        # create a block number named pool share file

        thisDirectory = os.path.dirname(os.path.realpath(__file__))

        blockNumberPoolShareFilename = str(localDelayedBlock) + "poolshare.csv"

        if isLinux:
            poolshareSubdirectoryFilename = thisDirectory + "/poolshare/" + blockNumberPoolShareFilename
        else:           # Windows    
            poolshareSubdirectoryFilename = thisDirectory + "poolshare\\" + blockNumberPoolShareFilename

        # print("poolshareSubdirectoryFilename =", poolshareSubdirectoryFilename)

        blockNumberPoolShare = open(poolshareSubdirectoryFilename, 'w', encoding="latin-1")
        # print("block number pool share file open for writing")
        # print("Opening file", poolshareSubdirectoryFilename)
        
    except IOError:   # NOT WORKING
        print("ERROR: poolshareSubdirectoryFilename file didn't exist, open for appending")

    tempStr = ''

    tempStr = "block," + str(delayedBlock) + "," + "poolbalance," + str(intsatsPoolBalance) + ","
    currentPoolShare.write(tempStr)
    currentPoolShare.write('\n')

    blockNumberPoolShare.write(tempStr)
    blockNumberPoolShare.write('\n')

    tempStr = ''

    tempStr = "poolrevenue," + str(intsatspoolRevenue) + ","
    # print("write_current_poolshare_file() ", tempStr)
    currentPoolShare.write(tempStr)
    currentPoolShare.write('\n')

    # rightSideExtra += str(intsatspoolRevenue)  # FFFFF

    blockNumberPoolShare.write(tempStr)
    blockNumberPoolShare.write('\n')

    arrayIndex = 0

    # sys.exit()

    for i in range(delegateCount):   
        tempStr = "delegate," + delegateArray[arrayIndex] + "," + "poolshare," + str(poolShareArray[arrayIndex]) + ","
        # print("writing i", i, tempStr)
        currentPoolShare.write(tempStr)
        currentPoolShare.write('\n')

        blockNumberPoolShare.write(tempStr)  # write the payout for this block for each delegate
        blockNumberPoolShare.write('\n')
        arrayIndex += 1

    currentPoolShare.close()
    blockNumberPoolShare.close()
    
    # poolFileOpen = False

    return()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

'''
pubkey to Qtum base58 address

References

https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses#How_to_create_Bitcoin_Address
https://stackoverflow.com/questions/59782364/sha256-giving-unexpected-result
https://docs.python.org/3/library/hashlib.html
'''

# from https://github.com/keis/base58/blob/master/base58/__init__.py

def b58encode_int(
    i: int, default_one: bool = True, alphabet: bytes = BITCOIN_ALPHABET
) -> bytes:
    """
    Encode an integer using Base58
    """
    if not i and default_one:
        return alphabet[0:1]
    string = b""
    while i:
        i, idx = divmod(i, 58)
        string = alphabet[idx:idx+1] + string
    return string

# - - - - - - - - - - - - - - - - - - - - - - - - 

def pubkey_to_base58(pubkey):
    # get the base58 address for a pubkey

    global isMainnet

    # 1. Get the SHA256 hash of the bytestring pubkey

    # pubkey = "03eb7062315dd132fb1c6cea6b629be85e6df23f40adc284b83db3a7fdc3d41d6d"
    # pubkey = "02ed405ca296cfed31cc47d563ef9850782a3dd746c5497fd9a96b5dc1844db506"
    bytestringPubkey = unhexlify(pubkey) # convert ASCII string to bytestring
    hashSHA256_step_1 = hashlib.sha256(bytestringPubkey).hexdigest() # get hexadecimal hash result
    # print("1. hashSHA256_step_1 =", hashSHA256_step_1) # hashSHA256_step_1 = 333ab721b27acc6222276e7f259a7be5397ac720801208bda0868afd07d600ac


    # 2. Get the RIPEMD-160 hash of #1

    bytestringhashRIPEMD160 = unhexlify(hashSHA256_step_1)
    hashRIPEMD160 = hashlib.new('ripemd160')
    hashRIPEMD160.update(bytestringhashRIPEMD160)
    hashRIPEMD160result = hashRIPEMD160.hexdigest()
    # print("2. hashRIPEMD160 =", hashRIPEMD160result) # hashRIPEMD160result = 992d80f76e627e59e210a9c9f2f0b448cd7178af

    # 3. Add network version byte in front of RIPEMD-160 hash, 0x31 for Qtum mainnet and 0x78 for Qtum testnet and regtest

    if isMainnet == True:
        networkPrefix = MAINNETPREFIX           # mainnet
    else:
        networkPrefix = TESTNETREGTESTPREVIX    # testnet & regtest

    extendedRIPEMD160result = networkPrefix + hashRIPEMD160result

    # print("3. extendedRIPEMD160result =", extendedRIPEMD160result) # extendedRIPEMD160result = 78992d80f76e627e59e210a9c9f2f0b448cd7178af

    # 4. Get the SHA256 hash on the extended RIPEMD160 result

    bytestringExtendedRIPEMD160result = unhexlify(extendedRIPEMD160result)
    hashSHA256_step_4result = hashlib.sha256(bytestringExtendedRIPEMD160result).hexdigest()
    # print("4. hashSHA256_step_4result =", hashSHA256_step_4result) # hashSHA256_step_4result = 027e49cce69598b5b34a4be785684c40f3051e7c2dc95b758bb86618fcca0b3c

    #5. Get the SHA256 hash on the result step 4

    bytestringSHA256_step_4result = unhexlify(hashSHA256_step_4result)
    hashSHA256_step_5result = hashlib.sha256(bytestringSHA256_step_4result).hexdigest()
    # print("5. hashSHA256_step_5result =", hashSHA256_step_5result) # hashSHA256_step_5result = 56cfb19b6d6f1bae6be931bc199b7d4eb4fae96c3fbec1b70c896250f7352dcb

    # 6. Take the first 4 bytes (8 characters) of step 4 as the checksum

    checksum = hashSHA256_step_5result[:8]  # get first 8 characters

    # print("6. checksum =", checksum)           # checksum = 56cfb19b

    # 7. Append the checksum to extendedRIPEMD160result from step 3. This is the 25-byte hex Qtum address.

    hexQtumAddress = "0" + extendedRIPEMD160result + checksum
    # print("7. hexQtumAddress =", hexQtumAddress) # hexQtumAddress = 0x78992d80f76e627e59e210a9c9f2f0b448cd7178af56cfb19b

    # 8. Convert hexQtumAddress from step 7 to decimal and base58 encode

    decimalQtumAddress = int(hexQtumAddress, 16)

    byteQtumAddress = b58encode_int(decimalQtumAddress, BITCOIN_ALPHABET)

    # print("8. byteQtumAddress =", byteQtumAddress)  # byteQtumAddress = b'qXXK43DpmWY6R8kFpdTZPS3aeKLhL7b2e6'

    # 9. Convert byteQtumAddress to string

    QtumAddress = byteQtumAddress.decode("utf-8")

    # print("9. QtumAddress =", QtumAddress)      # QtumAddress = qXXK43DpmWY6R8kFpdTZPS3aeKLhL7b2e6

    return(QtumAddress)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def read_config_file():
    # read in parameters from the configuration file
    # print configuration at startup

    global hostName                 # name of this computer
    global sendEmail                # Boolean to send emails
    global sendHourlyEmail          # Boolean to send hourly emails
    global setDomestic              # Boolean to use domestic cell phone for texts
    global enableLogging            # Boolean to enable logging
    global emailAddress             # Email from address
    global emailUsername            # Email account username
    global emailPassword            # Email account password
    global UTCTimeOffset            # local time offset from UTC (GMT)
    global myMinerAddress           # address of this staker
    global requiredFee              # required minimum delegation fee, 100 for pool
    global poolFee                  # the fee the pool charges
    global minimumUTXOSize          # required minimum UTXO to stake
    global intsatsSendmanyMinimum   # minimum size payout to send, in Satoshis
    global isMainnet                # Boolean for mainnet or testnet
    global isLinux                  # Boolean for Linux or Windows
    global forceTest                # force a test for immature coins or zero balance
    global catchupMode              # on startup, process all blocks from currentpoolshare forward

    global testnet                  # extra "-testnet" for parameters on testnet
    global OSPrefix                 # "./" prefix ./ to commands on Linux
    global OSDataIncr4              # no carriage return line feeds on Linux data
    global OSDataIncr2              # no extra bytes on Linux
    global OSDataIncr1              # no extra character on Linux

    global data                     # data from the config file
    global toAddress                # email address
    
    '''
    "hostName": LD18,
    "sendEmail": true,
    "sendHourlyEmail": true,
    "setDomestic": true,
    "domesticAddress": 9876543210@txt.att.net,
    "internationalAddress": 87954321@starhubenterprisemessaging.com,
    "enableLogging": true,
    "emailAddress": mygmail@gmail.com,
    "emailUsername": mygmail,
    "emailPassword": apgzvyhmeneljjlr,
    "UTCTimeOffset": 8,
    "myMinerAddress": QPooLGGp2FodAN1PpqvB7iLNK7kD3gSeko,
    "requiredFee": 100,
    "poolFee": 12,
    "minimumUTXOSize": 25,
    "intsatsSendmanyMinimum": 100000,
    "isMainnet": true,
    "isLinux": true,
    "forceTest": false,
    "catchupMode": true,
    '''

    try:
        configFile = open(config_file_name, 'r', encoding="latin-1")  # check for success, or exit
    except:
        print("ERROR opening configuration file")
        print('The configuration file "PPMConfig.txt" must be in the same directory with PPM, qtumd and qtum-cli')
        sys.exit()
        
    data = configFile.read()
    lenData = len(data)
    configFile.close()
    # print(data)

    # parse the configuration values

    hostName = parse_alphanum("hostName", 11, lenData)

    if hostName == -1:
        print("ERROR reading configuration file: hostName")
        sys.exit()
    else:
        print("hostName =", hostName)

    sendEmail = parse_logical("sendEmail", 12, lenData) # set to control sending of alert emails

    if sendEmail == -1:
        print("ERROR reading configuration file: sendEmail")
        sys.exit()
        
    sendHourlyEmail = parse_logical("sendHourlyEmail", 18, lenData)

    if sendHourlyEmail == -1:
        print("ERROR reading configuration file: sendHourlyEmail")
        sys.exit() 

    setDomestic = parse_logical("setDomestic", 14, lenData)  # set for domestic vs. international

    if setDomestic == -1:
        print("ERROR reading configuration file: setDomestic")
        sys.exit()
        
    '''
    email addresses can send a text to mobile phone, check your carrier
    domestic email address, could be a mobile number text address
    see http://www.makeuseof.com/tag/email-to-sms/
    '''
    
    domesticAddress = parse_alphanum("domesticAddress", 18, lenData)

    if domesticAddress == -1:
        print("ERROR reading configuration file: domesticAddress")
        sys.exit() 

    # international email address, could be a mobile number text address
    internationalAddress = parse_alphanum("internationalAddress", 23, lenData)

    if internationalAddress == -1:
        print("ERROR reading configuration file: internationalAddress")
        sys.exit() 

    if setDomestic == True:
        toAddress = domesticAddress
    else:    
        toAddress = internationalAddress

    # print("toAddress =", toAddress)

    if sendEmail == True:
        print("Email enabled, sending to", toAddress)
        
        if sendHourlyEmail == True:
            print("Sending hourly emails")
        else:
            print("But not sending hourly emails")
    else:
        print("Not sending emails")

    enableLogging = parse_logical("enableLogging", 16, lenData)

    if enableLogging == -1:
        print("ERROR reading configuration file: enableLogging")
        sys.exit() 

    if enableLogging == True:
        print("Logging enabled")
    else:
        print("Logging not enabled")

    # emails are sent from this email account, Gmail log in credentials
    # See https://support.google.com/accounts/answer/185833?hl=en
    # for Gmail, turn on 2FA and assign app password, make new device "Python"

    emailAddress = parse_alphanum("emailAddress", 15, lenData)
    # print("emailAddress =", emailAddress)

    if emailAddress == -1:
        print("ERROR reading configuration file: emailAddress")
        sys.exit() 

    emailUsername = parse_alphanum("emailUsername", 16, lenData)
    # print("emailUsername =", emailUsername)

    if emailUsername == -1:
        print("ERROR reading configuration file: emailUsername")
        sys.exit() 

    # Application Specific password from Python
    emailPassword = parse_alphanum("emailPassword", 16, lenData)
    # print("emailPassword =", emailPassword)

    if emailPassword == -1:
        print("ERROR reading configuration file: emailPassword")
        sys.exit() 

    UTCTimeOffset = int(parse_number("UTCTimeOffset", 0, 16, lenData, False))
    # print("UTCTimeOffset =", UTCTimeOffset)

    if UTCTimeOffset == -1:
        print("ERROR reading configuration file: UTCTimeOffset")
        sys.exit() 

    myMinerAddress = parse_alphanum("myMinerAddress", 17, lenData)
    print("myMinerAddress =", myMinerAddress)

    if myMinerAddress == -1:
        print("ERROR reading configuration file: myMinerAddress")
        sys.exit()

    if len(myMinerAddress) != 34:
        print("ERROR reading configuration file: myMinerAddress not 34 characters")
        sys.exit()
   
    requiredFee = int(parse_number("requiredFee", 0, 14, lenData, False))
    print("requiredFee =", requiredFee)

    if requiredFee < 0 or requiredFee > 100:
        print("ERROR reading configuration file: requiredFee not 0 to 100")
        sys.exit()        

    if requiredFee == -1:
        print("ERROR reading configuration file: requiredFee")
        sys.exit()

    poolFee = int(parse_number("poolFee", 0, 10, lenData, False))
    print("poolFee =", poolFee)

    if poolFee < -100 or poolFee > 100:
        print("ERROR reading configuration file: requiredFee not -100 to 100")
        sys.exit()        

    if poolFee == -101:
        print("ERROR reading configuration file: requiredFee")
        sys.exit()

    minimumUTXOSize = int(parse_number("minimumUTXOSize", 0, 18, lenData, False))
    print("minimumUTXOSize =", minimumUTXOSize)

    if minimumUTXOSize == -1:
        print("ERROR reading configuration file: minimumUTXOSize")
        sys.exit()

    intsatsSendmanyMinimum = int(parse_number("intsatsSendmanyMinimum", 0, 25, lenData, False))
    print("intsatsSendmanyMinimum =", intsatsSendmanyMinimum)

    if intsatsSendmanyMinimum == -1:
        print("ERROR reading configuration file: intsatsSendmanyMinimum")
        sys.exit()

    isMainnet = parse_logical("isMainnet", 12, lenData)

    if isMainnet == -1:
        print("ERROR reading configuration file: isMainnet")
        sys.exit()

    if isMainnet == True:
        testnet = ""            # for mainnet CLI commands
        print("On mainnet")
          
    else:
        testnet = "-testnet "   # for testnet CLI commands
        print("On testnet")

    isLinux = parse_logical("isLinux", 10, lenData)    

    if isLinux == -1:
        print("ERROR reading configuration file: isLinux")
        sys.exit()
        
    if isLinux == True:
        OSPrefix = "./"     # prefix ./ to commands on Linux
        OSDataIncr4 = 0     # no carriage return line feeds on Linux data
        OSDataIncr2 = 0     # no extra bytes on Linux
        OSDataIncr1 = 0     # no extra 1 space on Linux data
        print("On Linux")
        
    else:
        OSPrefix = ""       # no prefix on Windows
        OSDataIncr4 = 4     # skip over 2 carriage return line feeds on Windows
        OSDataIncr2 = 2     # skip over 2 bytes on Windows
        OSDataIncr1 = 1     # skip over 1 space on Windows
        print("On Windows")

    forceTest = parse_logical("forceTest", 12, lenData)

    if forceTest == True:   # for testing, force staking = True to override immature coins or
                            # zero balance
        print("forceTest = True, do not alert on staking status")
          
    else:
        print("forceTest = False, alert on staking status")
    
    if forceTest == -1:
        print("ERROR reading configuration file: forceTest")
        sys.exit()

    catchupMode = parse_logical("catchupMode", 14, lenData)

    if catchupMode == True:     # process all the blocks from currentpoolshare file to current
                                
        print("catchupMode = True, process all blocks from currentpoolshare file to catch up")
          
    else:
        print("catchupMode = False, process from current block")
    
    if catchupMode == -1:
        print("ERROR reading configuration file: catchupMode")
        sys.exit()

    # sys.exit()    

    return()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

'''
This function will create a "sendmany" command by looping through delegateArray
and poolShareArray to format the command to send the accrued payout to each delegate address.

The "sendmany" command is limited to about 500 addresses (by maximum fees), and requires
a minimum payment amount of 0.001 QTUM for all the addresses. Delegates that do not meet
the minimum amount intsatsSendmanyMinimum as set from the configuration file (because they
had recently joined the pool, or perhaps they are very small and the pool did not win many
block rewards in the payout interval) would not be paid, but instead moved to a
updateDelegateArray and updateWeightArray (for the share). After payment, the delegate
and poolshare arrays are zeroed out and carryover delegates/poolshares are copied back to the
arrays, and a new currentpoolshare.txt file is written (with the carryover delegates, if any).

Some representative fees (testnet July 2020, 40 sats/kB):

500 addresses 0.001 size 17,193 bytes, fee 0.508 QTUM
500 addresses 10.0  size 17,928 bytes, fee 0.530 QTUM

The sendmany command has the form (newlines added) with backslash escape characters:

sendmany "" "{
\"qHZYCwMdxudDtkHXjwrkcmpCbVjJ6skxAd\":0.001,
\"qHaTJMs8mogf7kA5bUdcXy47W3iZHj6GGR\":0.001,
\"qHaopUAYKmFXEJMfmnT7YaPYfynjQXKoTS\":0.001,
\"qHiiPfeeoM1XJpstWoAGbbrXrPoJKK7SuH\":0.001,
\"qL4HyUpYK4u7LoXyGAkvTBK5reQ3NwWQf9\":0.001}

After payout, the zeroed out current pool share file with no carryovers would look like

- - - - - - - - - - - - - - - - - - - - - -

block, 680050, poolBalance, 00000000,

- - - - - - - - - - - - - - - - - - - - - -

Function Logic

get fee, could be positive (staker keeps the fee), zero, or negative (staker pays out more).
calculate intsatsMinumumPayout, the minimum poolshare amount to be paid

while still elements in array
    while <= 500 elements this sendmany
        if poolShareArray >= intsatsMinimumPayment
           add delegate address and fee-adjusted poolShare to sendmany string
       else
           copy address and poolShare to update arrays to carryover
    # sanity check, avaliable balance, some max check, FUTURE
    send transaction
    if error, send alert
    log transaction details
log totals

zero out delegateArray and poolShareArray    
if there are elements in carryoverArray
    copy updateArrays to delegateArray & poolShareArray
log the carrover number and total amount

'''

def payout_with_sendmany(localFee):
    # make the payout with sendmany

    '''
    Get fee, could be positive (staker keeps the fee), zero, or negetave (staker pays out more)
    Use global intsatsSendmanyMinimum, the minimum to send after the fee is applied. For example, if the fee were
    10%, and intsatsSendmanyMinimum was 100000, the poolShare minimum would be 100000 / 0.9 = 111111 sats,
    because when the fee was applied this delegate would receive 100000. If the fee were -10%
    (a 10% bonus) the poolShare minimum would be 100000 / 1.1 = 90909 sats.
    If a delegate's poolshare value is >= intsatsMinimumPayout then pay out using sendmany, else
    carry over to accrue for future payouts.
    '''

    global intsatsSendmanyMinimum    # the minimum poolshare to be paid out
    global delegateCount
    global block                    # potential filename conflict if block reward on new day block, etc.
    global intsatsPoolBalance
    global fileOpenPPM
    
    global delegateArray
    global poolShareArray           # in Satoshis
    global updateDelegateArray      # for delegate carryovers
    global updateWeightArray        # in Satochis, for poolshare carryovers
    global intsatspoolRevenue       # for information and logging
    global delayedBlock
    global myWalletPassphrase
    global forceTest

    # sanity check for divide by zero error
    
    if 1 - (localFee / 100) == 0:
        print("ERROR: payout_with_sendmany() divide by zero")
        intsatsMinimumPayout = 100000   # set default

    else:    
        intsatsMinimumPayout = int(round(intsatsSendmanyMinimum / (1 - (localFee / 100)), 0))    # in Satoshis

    # print(intsatsMinimumPayout)

    sendmanyString = ''
    carryoverIndex = 0
    arrayIndex = 0
    totalNumPayouts = 0             # total number of delegates paid all sendmanys
    totalPayout = 0.0               # sum the total payout all sendmanys
    sendmanysSent = 0               # cound of the number of sendmanys sent

    # print(len(delegateArray[arrayIndex]))

    # print("before payout and carryover - - - - - - - - - - - - -")

    # for i in range(delegateCount): 
    #     print(i, delegateArray[i], poolShareArray[i])

    while len(delegateArray[arrayIndex]) == 34: # not the best

        # initialize sendmany string

        sendmanyString = OSPrefix + "qtum-cli "     # ./qtum-cli or qtum-cli
        sendmanyString += testnet                   # -testnet, if needed

        if isLinux == True:
            sendmanyString += 'sendmany \"\" '      # sendmany ""
            sendmanyString += "'{"                  # '{"
        else:    
            sendmanyString += 'sendmany \"\" \"{'   # sendmany "" "{
        
        sendmanyCount = 0
        sendmanyPayoutSubtotal = 0.0                # subtotal payout for this sendmany
        sendmanysSent += 1

        firstTimeThrough = True                     # to skip a comma first time though

        # while <= 500 elements this sendmany - - - - - - - - - - - - - - - - - - - - -
        
        while sendmanyCount < 500 and len(delegateArray[arrayIndex]) == 34:

            # print(poolShareArray[arrayIndex])
            # print("arrayIndex", arrayIndex)
            
            if poolShareArray[arrayIndex] >= intsatsMinimumPayout:  # enough to send

                sendmanyCount += 1          # count for this sendmany
                totalNumPayouts += 1        # total number for all sendmanys
                
                if firstTimeThrough == True:
                    firstTimeThrough = False
                else:
                    sendmanyString += ","   # comma after amount, but not first time

                # for Windows, use escape characters the terminal (qtum-cli) for \ \\ and " \", 


                if isLinux == True:
                    sendmanyString += '\"'          # |"
                else:    
                    sendmanyString += '\\\"'        # \"
                    
                sendmanyString += delegateArray[arrayIndex]     # delegate address

                if isLinux == True:
                    sendmanyString += '\":'         # \":
                else:
                    sendmanyString += '\\\":'       # \":

                # convert intsats to float

                strPayAmount = str(round((poolShareArray[arrayIndex] * ((100 - localFee) / 100) / 100000000), 8))
                sendmanyPayoutSubtotal += float(strPayAmount)
                totalPayout += float(strPayAmount)

                # print(strPayAmount)

                sendmanyString += strPayAmount                  # 1.23456789
                # sendmanyString += "0.00123456"                # for testing

                # print(sendmanyString)

            elif poolShareArray[arrayIndex] > 0:    # make a copy to carry over if a non-zero poolshare

                updateDelegateArray[carryoverIndex] = delegateArray[arrayIndex]
                updateWeightArray[carryoverIndex] = poolShareArray[arrayIndex]

                print("carryover", updateDelegateArray[carryoverIndex], updateWeightArray[carryoverIndex])

                carryoverIndex += 1

                # sys.exit()

            arrayIndex += 1  

        if isLinux == True:
             sendmanyString += "}'"                             # }'
        else:    
            sendmanyString += "}"                               # }

        # ready to send out this batch of up to 500 payouts
        # sanity check, avaliable balance, some max check, FUTURE

        if sendmanyCount > 0:   # found some payments, all in this batch weren't carried over

            # print(sendmanyString)  

            # send transaction, will return excess on change address

            unlock_for_sending(myWalletPassphrase)
            
            print("unlock for sending")

            time.sleep(0.1)

            params = OSPrefix + sendmanyString

            # print(params)

            tryNo = 0

            result = ""

            while forceTest == False:

                try:
                    result = str(subprocess.check_output(params, shell = True))
                    break
                
                except:
                    print("ERROR, payout_with_sendmany() - no response from qtumd, try =", tryNo + 1)
                    tryNo += 1
                    time.sleep(tryNo * 0.3)
                    
                    if tryNo >= 4:
                        print("No response from qtumd, exiting")
                        sys.exit()
                    
            moreData = str(result)

            if forceTest == False:
                print("Transaction ID, moreData =", moreData)
            else:
                print("Transaction ID, moreData = none - forceTest is True")

            # lenMoreData = len(moreData)
            # print("lenMoreData =", lenMoreData)

            '''

            # if error, send alert

            {\"qHZYCwMdxudDtkHXjwrkcmpCbVjJ6skxAd\":0.00111111,
             \"qHaTJMs8mogf7kA5bUdcXy47W3iZHj6GGR\":0.002,
             \"qHaopUAYKmFXEJMfmnT7YaPYfynjQXKoTS\":0.003,
             \"qHiiPfeeoM1XJpstWoAGbbrXrPoJKK7SuH\":0.004,
             \"qL4HyUpYK4u7LoXyGAkvTBK5reQ3NwWQf9\":0.005}
         
            9680fc5c54348a94989ede373e16475bc7c321b818d1c5ff324547627f4751b7
            '''

            # if not error
      
            # log payment, number of delegates paid, fee, total amount sent (amount + fees), and transaction IDs

            print("delegates paid ", sendmanyCount, "subtotal paid ", totalPayout)
            
            intsatspoolRevenue += (intsatsPoolBalance - totalPayout * 100000000)     # the pool fee

    unlock_for_staking_only(myWalletPassphrase)
    print("unlock for staking only")

    time.sleep(0.1)
            
    # zero out delegateArray and poolShareArray, should be function call

    for i in range(arrayIndex):
        delegateArray[i] = ''
        poolShareArray[i] = 0

    intsatsPoolBalance = 0      # zero out unless we have some carryovers below
    delegateCount = 0           # zero out unless we count some carryovers below
    arrayIndex = 0

    if carryoverIndex > 0:      # if there are elements the update arrays
        
        # copy updates to delegateArray & poolShareArray

        carryoverIndexNow = 0
 
        for i in range(carryoverIndex):
            
            delegateArray[i] = updateDelegateArray[carryoverIndexNow]
            poolShareArray[i] = updateWeightArray[carryoverIndexNow]
            intsatsPoolBalance += poolShareArray[i]    # sum for new pool balance
            
            arrayIndex += 1
            carryoverIndexNow += 1

        delegateCount = carryoverIndexNow    # reset delegate count after carryover    
    
        # log the carrover number and subtotal for this sendmany
                                                                    # "{:,f}".format(round(balance, 1)))[:-5]
        print("number of carryovers", carryoverIndex, "sendmany amount", "{:.8f}".format(sendmanyPayoutSubtotal))

        if enableLogging == True:
            log("300,payout,carryovers," + str(carryoverIndex) +",sendmanyAmount," + str("{:.8f}".format(sendmanyPayoutSubtotal)))

    print("after payout and carryover - - - - - - - - - - - - -")

    if arrayIndex == 0:
        print("arrayIndex = 0, arrays are empty")

    for i in range(arrayIndex):
        print(i, delegateArray[i], poolShareArray[i])        
              
    write_current_pool_share_file(delayedBlock)   # write new currentpoolshare file and block number file

    # log results from all the sendmanys

    print("Payout completed. sendmanys sent", sendmanysSent, "number delegates paid", totalNumPayouts, "total paid", "{:.8f}".format(totalPayout), "revenue", "{:.8f}".format(intsatspoolRevenue / 100000000))

    # # 300,total,sendmanys,1,numDelegatesPaid,63,totalPaid,211.20079246,intsatspoolRevenue,26000089788.799206

    if enableLogging == True:  
        # tempStr = "300,total,sendmanys," + str(sendmanysSent) +",numDelegatesPaid," + str(totalNumPayouts) +\
        #           "totalPaid," + str("{:.8f}".format(totalPayout)) + ",intsatspoolRevenue," + str(intsatspoolRevenue)
        log("300,total,sendmanys," + str(sendmanysSent) +",numDelegatesPaid," + str(totalNumPayouts) +\
            ",totalPaid," + str("{:.8f}".format(totalPayout)) + ",intsatspoolRevenue," + str(intsatspoolRevenue))

    if sendEmail == True:
        tempMessage =  str(totalNumPayouts) + "paid " + str("{:.2f}".format(totalPayout)) + "revenue " + str("{:.2f}".format(intsatspoolRevenue / 100000000))
        tempSubject = "." + hostName + " stk " + stakeWithCommas                
        send_email(tempSubject, tempMessage)
        
    intsatspoolRevenue = 0       # zero out for next pay interval    

    return()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def log(logString):
    # write to the log file

    global logsSubdirectoryFilename
   
    logFilePPM = open(logsSubdirectoryFilename, 'a')    # open log file
    # print("Opening file") 
    logFilePPM.write(logString)
    logFilePPM.write('\n')
    # print(logString)
    time.sleep(0.01)
    logFilePPM.close()                                  # close the log file
    return()

def get_block(blockNo):
    # get the blockhash and block data

    global OSPrefix
    global testnet
    global data
    
    strBlock = str(blockNo) 
    
    params = OSPrefix + "qtum-cli " + testnet + "getblockhash " + strBlock

    # print(params)                             # Windows and Linux shown
    # qtum-cli -testnet getblockhash 633000
    # ./qtum-cli -testnet getblockhash 633000

    blockHashRaw = ""  # clear it to see bad response

    # get the block hash for a block number

    tryNo = 0

    while True:
    
        try:
            blockHashRaw = str(subprocess.check_output(params, shell = True))
            break
        
        except:
            print("ERROR, get_block()1 - no response from qtumd, make sure qtumd is fully synced, try =", tryNo + 1)
            tryNo += 1
            time.sleep(tryNo * 0.3)
            
            if tryNo >= 4:
                print("No response from qtumd, exiting")
                sys.exit()

    # print(blockHashRaw)
    # Windows: b'fe19e3dac760d3addb6d2358f75c85b47ced77bc2705a750ee762d1345be7a5d\r\n'
    # Linux:   b'fe19e3dac760d3addb6d2358f75c85b47ced77bc2705a750ee762d1345be7a5d\n'

    blockHash = blockHashRaw[2:66]
    
    # print("blockHash =", blockHash)
    # fe19e3dac760d3addb6d2358f75c85b47ced77bc2705a750ee762d1345be7a5d

    params = OSPrefix + "qtum-cli " + testnet + "getblock " + blockHash
    
    # print(params)
    # qtum-cli -testnet getblock fe19e3dac760d3addb6d2358f75c85b47ced77bc2705a750ee762d1345be7a5d
    # ./qtum-cli -testnet getblock fe19e3dac760d3addb6d2358f75c85b47ced77bc2705a750ee762d1345be7a5d

    output = ""  # clear it to see bad response

    # get the block data - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    tryNo = 0

    while True:

        try:
            output = str(subprocess.check_output(params, shell = True))
            break
        
        except:
            print("ERROR, get_block()2 - no response from qtumd, make sure qtumd is fully synced, try =", tryNo + 1)
            tryNo += 1
            time.sleep(tryNo * 0.3)
            
            if tryNo >= 4:
                print("No response from qtumd, exiting")
                sys.exit()
                
    data = str(output)
    lenData = len(data)
    
    # print(data)
    
    ''' - - - - - - - block data - - - - - - - - Windows has many additional \r\n 
    b'{  
    "hash": "fe19e3dac760d3addb6d2358f75c85b47ced77bc2705a750ee762d1345be7a5d", 
    "confirmations": 249,  "strippedsize": 535,  "size": 571,  "weight": 2176,  
    "height": 633000,  "version": 536870912,  "versionHex": "20000000",  
    "merkleroot": "14d8214926b0d38bc2a0b19bf910ba1a11310550836efc417d9eb5d130630f3b",  
    "hashStateRoot": "1a0f52cefdae6ca0d532ce76000111ee26e91896bccff67c5ba31ff01d83124d",  
    "hashUTXORoot": "a707496b3935006500fa3ec7103450443a247908dfdb9265e5a593c138fbc763",  
    "prevoutStakeHash": "5688f00f935b7126bd880c7d0ade8018704664f560bc5f912e527b3eeee84b90",  
    "prevoutStakeVoutN": 1,  
    "tx": [    
    "49e211d74629aa68f7f12461fe1f9d50c382d4f009494927b01eee0364ad8807",    
    "04c44efdd428cf4458d6753a8245134362f055b884192033c02e4f9bc1110a60"  ],  
    "time": 1594459776,  "mediantime": 1594458928,  "nonce": 0,
    <snip>
    }
    '''    

    return

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def parse_coinstake(localLenData):
    # parse the coinstake transaction to find staker address and rewards

    global isSuperStaker                # set by proofOfDelegation in block header
    global rightSideExtra               # debug string
    global data
    global myMinerAddress               # from config file
    global intsatsPoolBalance
    global intsatspoolRevenue 
    global isMyMiner                    # set here
    global isPoolBlockReward            # set here

    # set all these here
    global valueVin
    global stakerAddress
    global valueCoinstakeVout1
    global valueCoinstakeVout2
    global stakerReward
    global delegateAddress
    global delegateReward
    global percentFee
    global delayedBlock
    global sendNewSingleBlockReward
    global numDelegates

    # print("entering, isSuperStaker =", isSuperStaker, "localLenData =", localLenData)

    ''' - - - - - - - - - coinstake data - - - - - - - - - - - - - - - - - - -

    {
      "hex": "0200000001d6d7c6cdbed9887e32740c9bacb93c32f797ebd09f58247396d697ce48c2b20f010000004847304402202b695d624dd2d4075140cea456e18866baaef763ffba89d9a98ce1c9e7e1e4d30220242391cc452414a4a6bf4da5470887613ce345430a1d624dd84d4e9397d3092e01ffffffff03000000000000000000006a1ac4020000002321039b33555fe9dcb13c8585034715555e4f40ad7bc12723c46d5e476dfebba345a2ac002a7515000000002321031f48b26481bea513a84573de5f62b4b23d2989a823158e897ce85f755818f04fac00000000",
      "txid": "87e954462840af6bf1f2d98bb814963e40980caf6f9f89d82f1323cfe97535a3",
      "hash": "87e954462840af6bf1f2d98bb814963e40980caf6f9f89d82f1323cfe97535a3",
      "version": 2,
      "size": 220,
      "vsize": 220,
      "weight": 880,
      "locktime": 0,
      "vin": [
        {
          "txid": "0fb2c248ce97d6967324589fd0eb97f7323cb9ac9b0c74327e88d9becdc6d7d6",
          "vout": 1,
          "scriptSig": {
            "asm": "304402202b695d624dd2d4075140cea456e18866baaef763ffba89d9a98ce1c9e7e1e4d30220242391cc452414a4a6bf4da5470887613ce345430a1d624dd84d4e9397d3092e[ALL]",
            "hex": "47304402202b695d624dd2d4075140cea456e18866baaef763ffba89d9a98ce1c9e7e1e4d30220242391cc452414a4a6bf4da5470887613ce345430a1d624dd84d4e9397d3092e01"
          },
          "value": 118.40000000,
          "valueSat": 11840000000,
          "address": "qMUR738THXBXABfx1Rk6iWtiStEPtQKWYK",
          "sequence": 4294967295
        }
      ],
      "vout": [
        {
          "value": 0.00000000,
          "valueSat": 0,
          "n": 0,
          "scriptPubKey": {
            "asm": "",
            "hex": "",
            "type": "nonstandard"
          }
        },
        {
          "value": 118.80000000,
          "valueSat": 11880000000,
          "n": 1,
          "scriptPubKey": {
            "asm": "039b33555fe9dcb13c8585034715555e4f40ad7bc12723c46d5e476dfebba345a2 OP_CHECKSIG",
            "hex": "21039b33555fe9dcb13c8585034715555e4f40ad7bc12723c46d5e476dfebba345a2ac",
            "type": "pubkey"
          }
        },
        {
          "value": 3.60000000,
          "valueSat": 360000000,
          "n": 2,
          "scriptPubKey": {
            "asm": "031f48b26481bea513a84573de5f62b4b23d2989a823158e897ce85f755818f04f OP_CHECKSIG",
            "hex": "21031f48b26481bea513a84573de5f62b4b23d2989a823158e897ce85f755818f04fac",
            "type": "pubkey"
          }
        }
      ],
      "blockhash": "e66a6a8ce9b264e44bb520f2986a650798e6ecd17b98599e9a5c524c612d6c8e",
      "height": 660890,
      "confirmations": 6,
      "time": 1598046640,
      "blocktime": 1598046640
    }
        
    Here the vin gives the address of the miner.
    
    '''

    # print(data)

    # get the value of the block reward - - - - - - - - - - - - - - - - - -
    # get the value of the vins, such as testnet block 637,884

    # there could be multiple vins, loop through all to get total stake input

    i = data.find("value", 0)

    voutIndex = data.find('"vout": [', i)   # get the start of the vouts

    valueVin = 0.0

    numVins = 0

    while i < voutIndex:            # loop through all the vins, up to 100

        numVins += 1

        strValueVin = ''

        i += 8                      # fixed offset to numbers

        while data[i] != ",":               # get this vin value
            strValueVin += data[i]
            i += 1

        valueVin += float(strValueVin)    
            
        # print("valueVin = ", valueVin)

        i = data.find("value", i + 50)      # skip over "valueSat"

    # get the stakerAddress - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    i = data.find("address", 1000)
    
    stakerAddress = ''

    start = i + 11                  # fixed offset to staker address
    end = start + 34                # address 34 characters in length

    for i in range(start, end):     # get the address
        stakerAddress += data[i]    # if get "IndexError: string index out of range" here
                                    # make sure to launch qtumd with "-txindex

    # print("delayedBlock", delayedBlock, "stakerAddress", stakerAddress)

    if myMinerAddress == stakerAddress:       # this pool staker

        isMyMiner = True
        sendNewSingleBlockReward = True

        if isSuperStaker == True:       
            
            isPoolBlockReward = True    # pool block reward for a delegate

        else:
            isPoolBlockReward = False  # pool staker block reward with its own UTXOs, don't pay pool

    else:

        isMyMiner = False
        
        isPoolBlockReward = False      # another miner, no pool reward

    # temp = str(isMyMiner) + " " + str(isPoolBlockReward)

    # rightSideExtra += temp

    # get the coinstake vouts - - - - - - - - - - - - - - - - - - - - - - -
    # this is the first vout, there may be more

    # print(data)

    delegateReward = 0.0
    percentFee = -1                         # -1 = no precentFee found (not a super staker)

    i = voutIndex                           # the start of the vouts

    i += 60                                 # skip over the coinbase vout0, which is always 0

    i = data.find("value", i)       # find the 1st coinstake vout (there may be more)

    # print("i vout value = ", i)

    valueCoinstakeVout1 = ''

    i += 8                          # fixed offset to numbers

    while data[i] != ",":           # get the value
        valueCoinstakeVout1 += data[i]
        i += 1
        
    # print("valueCoinstakeVout1 = ", valueCoinstakeVout1)

    # voutBlockReward = float(valueCoinstakeVout1)
    # stakerReward = voutBlockReward - float(valueVin)  # stakerReward if no split or delegates

    # print("voutBlockReward, 1st one", voutBlockReward, "stakerReward", stakerReward)

    # get 3 more vouts, if available
    
    valueCoinstakeVout2 = '0'
    valueCoinstakeVout3 = '0'
    valueCoinstakeVout4 = '0'

    # is this a split block reward with a 2nd half? For example, testnet block 634,002

    i += 40      # skip over "valueSat"

    i = data.find("value", i, localLenData)       # is there a "value" for a "n": 2 vout in this coinstake?

    # print("i 2nd vout =", i)

    tempAddress = "" 

    if i > 0:               # found a 2nd Vout

        valueCoinstakeVout2 = ''        

        i += 8                          # fixed offset to address

        while data[i] != ",":           # get the value
            valueCoinstakeVout2 += data[i]
            i += 1
                    
        # print("valueCoinstakeVout2 = ", valueCoinstakeVout2)

        # check if there is an address for vout2, which would be different from
        # the delegate address if this is a gas refund

        iSaved = i

        i = data.find("addresses", i, localLenData)

        # print("i addresses =", i)

        if i > 0:
            
            start = i + 28                  # fixed offset to vout2 address
            end = start + 34                # address 34 characters in length

            for i in range(start, end):     # get the address
                tempAddress += data[i]    

            # print("tempAddress =", tempAddress)

        else:

            # print("iSaved =", iSaved)
            
            i = data.find("pubkey", iSaved, localLenData)  # is this a pubkey address?

            if i > 0:

                i = data.find("asm", iSaved, localLenData)

                if i > 0:

                    pubkey = ""
                    
                    start = i + 7                   # fixed offset to pubkey
                    end = start + 66                # pubkey 66 characters in length

                    for i in range(start, end):     # get the pubkey
                        pubkey += data[i]    

                    # print("pubkey =", pubkey)

                    tempAddress = pubkey_to_base58(pubkey)

                    # print("tempAddress =", tempAddress)

        # check for a 3rd vout
        
        # i += 40 # ?????

        i = data.find("value", i, localLenData)       # is there a vout3?

        # print("i 3nd vout =", i)

        if i > 0:               # found a 3rd Vout

            valueCoinstakeVout3 = ''

            i += 8                          # fixed offset to numbers

            while data[i] != ",":           # get the value
                valueCoinstakeVout3 += data[i]
                i += 1
                        
            # print("valueCoinstakeVout3 = ", valueCoinstakeVout3)

            # check for a 4th vout
            
            i += 40 

            i = data.find("value", i, localLenData)       # is there a vout4?

            # print("i 4th vout =", i)

            if i > 0:               # found a 4th Vout

                valueCoinstakeVout4 = ''

                i += 8                          # fixed offset to numbers

                while data[i] != ",":           # get the vin value
                    valueCoinstakeVout4 += data[i]
                    i += 1
                            
                # print("valueCoinstakeVout4 = ", valueCoinstakeVout4)     

    # fix for block 639,536 with delegate pubkeyhash and address listed

    '''
    if float(valueCoinstakeVout1) > 0:
        rightSideExtra += str(valueCoinstakeVout1) + " "
        
    if float(valueCoinstakeVout2) > 0:
        rightSideExtra += str(valueCoinstakeVout2) + " "

    if float(valueCoinstakeVout3) > 0:
        rightSideExtra += str(valueCoinstakeVout3) + " "

    if float(valueCoinstakeVout4) > 0:
        rightSideExtra += str(valueCoinstakeVout4) + " "
    '''    

    if isSuperStaker == False:

        if float(valueCoinstakeVout1) + float(valueCoinstakeVout2) == 0:
            print("ERROR: parse_coinstake() 1 divide by zero")        # set default value of subsidy?

        else:
            if float(valueCoinstakeVout2) >= 100.0 and float(valueCoinstakeVout1) / (float(valueCoinstakeVout1) + float(valueCoinstakeVout2)) > 0.48:
                voutBlockReward = float(valueCoinstakeVout1) + float(valueCoinstakeVout2)   # split block reward
                stakerReward = voutBlockReward - float(valueVin)
            else:
                voutBlockReward = float(valueCoinstakeVout1)                                # not a split block reward 
                stakerReward = voutBlockReward - float(valueVin)
        
        fee = 0   # is this needed?

    else:   # this is a super staker

        # check for a stake > 200.0 split in two

        # sanity check for divide by zero

        if valueCoinstakeVout1 + valueCoinstakeVout2 == 0:
            print("ERROR: parse_coinstake() 2 divide by zero")        # set default value of subsidy?

        else:       
            if float(valueCoinstakeVout2) >= 100.0 and float(valueCoinstakeVout1) / (float(valueCoinstakeVout1) + float(valueCoinstakeVout2)) > 0.48:
                voutBlockReward = float(valueCoinstakeVout1) + float(valueCoinstakeVout2)   # split block reward
                stakerReward = voutBlockReward - float(valueVin)
                delegateReward = float(valueCoinstakeVout3)                                 # but gas problem
                
            else:
                voutBlockReward = float(valueCoinstakeVout1)                                # not a split block reward 
                stakerReward = voutBlockReward - float(valueVin)

                # print("tempAddress =", tempAddress, "delegateAddress =", delegateAddress)

                # delegateReward =  float(valueCoinstakeVout2)        # not a gas refund for a 100% fee delegation

                # print("tempAddress =", tempAddress, "delegateAddress =", delegateAddress)

                if tempAddress == delegateAddress:                  # not a gas refund for a 100% fee delegation
                    delegateReward = float(valueCoinstakeVout2)

                else:                                               # a gas refund
                    delegateReward = 0.0

                # print("delegateReward =", delegateReward)

        # sanity check, prevent divide by zero

        if stakerReward + delegateReward == 0.0:        # shouldn't happen
            print("ERROR: stakerReward + delegateReward - 0.0, forcing stakerReward = 4.0")
            stakerReward = 4.0
            
        percentFee = int(round(100 * (stakerReward / (stakerReward + delegateReward)), 0))

        # print("percentFee =", percentFee)

        # get the delegateAddress from pubkey (if exists)
        
    '''
    i = data.find("asm", i)  # find the "asm" start of the pubkey

    start = i + 7                   # fixed offset to start of pubkey characters
    end = start + 66                # pubkey 66 characters in length
    
    pubkey = ''

    for i in range(start, end):     # get the pubkey
        pubkey += data[i]

    print("pubkey =", pubkey)

    delegateAddress = pubkey_to_base58(pubkey)   # get the base58 address for this pubkey

    print("delegateAddress =", delegateAddress)

    '''

    # print("stakerReward =", stakerReward)
    
    # formattedStakerReward = "{:6.3f}".format(round(stakerReward, 3))            

    # rightSideExtra = " vins: " + str(numVins)

    if isMyMiner == True and isSuperStaker == False:   # block reward for self
        intsatspoolRevenue += int(round(100000000 * stakerReward))

    if isPoolBlockReward == True:
        
        intsatsPoolBalance += int(round(100000000 * stakerReward))

        # print("intsatsPoolBalance ", intsatsPoolBalance, "stakerReward ", stakerReward)

        get_delegations_for_staker(stakerReward)        # update the delegates and weights
        write_current_pool_share_file(delayedBlock)     # save to disk

    elif isMyMiner == True:
        # intsatspoolRevenue += int(round(100000000 * stakerReward))    # block reward for self (not the pool) DUPLICATE
        # print("intsatspoolRevenue =", intsatspoolRevenue)
        numDelegates = get_delegate_count()  # update the delegate count to see new delegations for this block

    else:                               # block is not for this miner 
        numDelegates = get_delegate_count()  # update the delegate count to see new delegations for this block

    # print("stakerReward =", stakerReward)
    
    return

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def unlock_for_staking_only(localMyWalletPassphrase):
    # unlock the wallet for staking only

    global OSPrefix
    global testnet
    global forceTest

    params = OSPrefix + "qtum-cli " + testnet + "walletpassphrase " + '\"' + localMyWalletPassphrase + '\"' + " 99999999 true"

    # print(params)

    tryNo = 0

    while forceTest == False:
    
        try:
            output = subprocess.check_output(params, shell = True)
            break

        except:
            print("NO RESPONSE from qtumd - unlock_for_staking_only(), try =", tryNo + 1)
            tryNo += 1
            time.sleep(tryNo * 0.3)
            
            if tryNo >= 4:
                print("No response from qtumd, exiting")
                sys.exit()

    # print("unlock_for_staking_only() output =", output)
    
    return

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def unlock_for_sending(localMyWalletPassphrase):
    # fully unlock for sending coins, for payout

    global OSPrefix
    global testnet
    global forceTest

    # unlock for 20 seconds

    params = OSPrefix + "qtum-cli " + testnet + "walletpassphrase " + '\"' + localMyWalletPassphrase + '\"' + " 20"

    # print(params)

    tryNo = 0

    while forceTest == False:
    
        try:
            output = subprocess.check_output(params, shell = True)
            break

        except:
            print("NO RESPONSE from qtumd - unlock_for_sending(), try =", tryNo + 1)
            tryNo += 1
            time.sleep(tryNo * 0.3)
            
            if tryNo >= 4:
                print("No response from qtumd, exiting")
                sys.exit()

    # print("output for unlock_for_sending() =", output)    

    return    
        
 # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        
def payout_with_sendmany_stub():
    # stub sendmany() for testing

    global myWalletPassphrase
    global sendEmail
    global hostName
    global stakeWithCommas
    global OSPrefix
    global testnet

    unlock_for_sending(myWalletPassphrase)

    time.sleep(0.1)

    if isLinux == True:
        params = OSPrefix + "qtum-cli -testnet sendmany \"\" '{\"qLHuSYRtbmq4cBnrULQyXV9adV3Qk26jVS\":0.001,\"qUm2rSUPKWr7KqumSRkS5jzMop94n92W2T\":0.001}'"
    else:    
        params = OSPrefix + 'qtum-cli -testnet sendmany \"\" \"{\\\"qLHuSYRtbmq4cBnrULQyXV9adV3Qk26jVS\\\":0.001,\\\"qUm2rSUPKWr7KqumSRkS5jzMop94n92W2T\\\":0.001}'

    # print(params)

    # sys.exit()

    tryNo = 0

    while True:
        
        try:
            result = str(subprocess.check_output(params, shell = True))
            break
        
        except:
            print("ERROR, payout_with_sendmany_stub() - no response from qtumd, try =", tryNo + 1)
            tryNo += 1
            time.sleep(tryNo * 0.3)
            
            if tryNo >= 4:
                print("No response from qtumd, exiting")
                sys.exit()

    moreData = str(result)

    # print("result from payout_with_sendmany_stub() moreData =", moreData)

    time.sleep(0.1)

    unlock_for_staking_only(myWalletPassphrase)

    time.sleep(0.1)

    if sendEmail == True:   
        tempMessage =  " sendmany_stub()"
        tempSubject = "." + hostName + " stk " + stakeWithCommas                
        send_email(tempSubject, tempMessage)

    # lenMoreData = len(moreData)

    # print("lenMoreData =", lenMoreData)

    # if error, send alert

    return()

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# MAIN PROGRAM STARTS HERE  = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

print("PoolPaymentManager version", version)

testPass = 0                      # for testing
sendNewSingleBlockReward = False  # send an alert when have all the info, new single reward
# sendNewMultiBlockReward = False   # send and alert for a new overlapping reward
# sendBlockStaleAlert = False       # blocks are getting stale > 1/2 hours
doNotDisturbQueue = ''            # alert messages queued up during doNotDisturb times
numDelegates = 0                  # number of delegates discovered

PPMStartTime = int(time.time())   # time program started, after 30 minutes look for stale blocks
                                  # and low connections

start = timer()                   # for timing block loop below, first time through
start2 = timer()                  # kludge, for loop timing
lastBlockCheckTime = timer()      # for startup

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# configuration file parameters - - - - - - - - - - - - - - - - - - - - - - - - - -
# these parameters are all set from the configuration file

hostName = ""
sendEmail = False
enableLogging = False
sendEmailForNewHour = False
setDomestic = False
domesticAddress = ""
internationalAddress = ""
enableLogging = False
emailAddress = ""
emailUsername = ""
emailPassword = ""
UTCTimeOffset = -1
myMinerAddress = ""
requiredFee = -1
minimumUTXOSize = -1
intsatsSendmanyMinimum = -1
isMainnet = False
isLinux = False
forceTest = False

read_config_file()   # read configuration file parameters

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

read_current_pool_share_file()   # read the current pool share file

# print("block =", block, "delayedBlock =", delayedBlock)

# initialize log file - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Windows, can set the Z drive, as an Administrator, go to System - Disk Management - All Tasks - 
# Change Drive Letter and Paths


if enableLogging == True:    

    GMT = strftime("%a, %Y %m %d %H:%M:%S", time.gmtime())  # Sat, 2020 09 19 00:59:49
    
    # open log file in the format "PPMLog_YYYY_MMM_DD.csv"
    log_file_name_PPM = 'PPM_Log_'+GMT[5]+GMT[6]+GMT[7]+GMT[8]+'_'+GMT[10]+GMT[11]+\
                    '_'+GMT[13]+GMT[14]+'.csv'
    
    print("PPM log file name =", log_file_name_PPM)
        
    try:
        thisDirectory = os.path.dirname(os.path.realpath(__file__))

        if isLinux:
            logsSubdirectoryFilename = thisDirectory + "/logs/" + log_file_name_PPM
        else:          # Windows
            logsSubdirectoryFilename = thisDirectory + "logs\\" + log_file_name_PPM

        print("logsSubdirectoryFilename =", logsSubdirectoryFilename)
        
        logFilePPM = open(logsSubdirectoryFilename, 'a')   # create or open log file for appending
        print("PPM log file open for appending")
        log("000,Program,start,or,restart,version," + version)
        
        # log starting time:
        log("000,Logging,start,"+GMT[16]+GMT[17]+GMT[18]+GMT[19]+GMT[20]+GMT[21]+GMT[22]+GMT[23]+',GMT,'\
            +GMT[5]+GMT[6]+GMT[7]+GMT[8]+'_'+GMT[10]+GMT[11]+'_'+GMT[13]+GMT[14])
        log(logLabels)
        
    except IOError:   # NOT WORKING
        print("PPM ERROR: File didn't exist, open for appending")

fileOpenPPM = False

# check that qtumd is running - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# look for a response from qtum-cli getblockcount

while True:  # wait here if qtumd is not running

    blockResult = -1    # error condition, unless set by qtumd

    params = OSPrefix + "qtum-cli " + testnet + "getblockcount"
            
    # print("params =", params)

    tryNo = 0

    while True:

        try:
            blockResult = int(subprocess.check_output(params, shell = True))
            break
        
        except:
            print("ERROR, main() check that qtumd is running - no response from qtumd, try =", tryNo + 1)
            tryNo += 1
            time.sleep(tryNo * 0.3)
            
            if tryNo >= 4:
                print("No response from qtumd, exiting")
                sys.exit()
            
    # print("In qtumd check, blockResult =", blockResult)

    if blockResult > 0:
        
        if qtumdIsRunning == False:   # on startup or restart
            qtumdIsRunning = True
            print("qtumd is running")
        sendOneTimeQtumdOffline = False # reset to find next qtumd offline
        
        # the first time through, set oldBlock so don't get double row print
        
        if firstTimeThrough == True:
            
            oldBlock = block
        break
    
    else:
        print("qtumd is NOT RUNNING. Standby")
        qtumdIsRunning = False

        if sendOneTimeQtumdOffline == False:  # send an alert and log once for this problem
            sendOneTimeQtumdOffline = True

            tempMessage = " on" + hostName
            tempSubject = " QTUMD NOT RUNNING"

            if sendEmail == True:
                send_email(tempSubject, tempMessage)  
                print("Sending email" + tempSubject + tempMessage)

            if enableLogging == True:
                log("900, QTUMD OFFLINE")

        time.sleep(15) # give some time to start/restart qtumd     

numDelegates = get_delegate_count()     # get delegates on startup

# print("block =", block, "delayedBlock =", delayedBlock)

# pubkey = "02ed405ca296cfed31cc47d563ef9850782a3dd746c5497fd9a96b5dc1844db506"
# addr = pubkey_to_base58(pubkey)

# print("addr =", addr)

while True:
    if labelsPrintedAtStartup == False:  # print the label row once during startup
        labelsPrintedAtStartup = True
        if delayedBlock % 10 != 0:     # because if delayedBlock % 10 == True at startup, it will print below
            print(labelRow)

    # print("Top of loop")
    startTimer = timer()

    isSuperStaker = False       # is this block mined by a super staker, False unless set True below
    isMyMiner = False           # is this block mined by my miner
    prevoutStakeHash = ''       # unless entered below for pool
    prevoutStakeVoutN = ''      # unless entered below for pool
    poolDelegate = ''           # set for pool super stakers
    rightSideExtra = ''         # for right side debugging message

    # check "getinfo" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    '''  Typical response from v0.19.1 2020-07-05 - Windows format
    b'{\r\n  "version": 190100,\r\n
    "protocolversion": 70018,\r\n
    "blocks": 629480,\r\n
    "timeoffset": 0,\r\n
    "connections": 9,\r\n
    "proxy": "",\r\n
    "difficulty": {\r\n
      "proof-of-work": 1.52587890625e-005,\r\n
      "proof-of-stake": 780919.515238123\r\n  },\r\n
      "chain": "test",\r\n
      "moneysupply": 102497920,\r\n
      "walletversion": 169900,\r\n
    "balance": 4788.35542735,\r\n
    "stake": 3532.94762951,\r\n
    "keypoololdest": 1577775197,\r\n
    "keypoolsize": 1000,\r\n
    "paytxfee": 0.00000000,\r\n
    "relayfee": 0.00400000,\r\n
    "warnings": ""\r\n}\r\n'

    '''
    
    if firstTimeThrough == True:     # for the display, otherwise use -getinfo data from the block waiting loop below

        params = OSPrefix + "qtum-cli " + testnet+ "-getinfo"
        
        tryNo = 0

        while True:

            try:
                output = subprocess.check_output(params, shell = True)
                break
            
            except:
                print("firstTimeThrough, no response from qtumd, try =", tryNo + 1)
                tryNo += 1
                time.sleep(tryNo * 0.3)
                
                if tryNo >= 4:
                    print("No response from qtumd, exiting")
                    sys.exit()

        # print(output)

        data = str(output)
        lenData = len(data)

        # print("lenData top of main =", lenData)     # lenData = 568

        if block == 0:   # initial startup with no currentpoolshare.txt file to set block number

            block = int(parse_number("blocks", 0, 9, lenData, False))  # get block
            oldBlock = block - 1
            delayedBlock = block - orphanDelay 
            
            # print("Startup block = ", block, "delayedBlock =", delayedBlock)

    '''
    # for testing
    if testPass == 0:
        print("Test data 1")
        data = '{"balance": 0.00000000,"stake": 0.00000000, "blocks": 13765, "timeoffset": 0"}'
        testPass = 1
    elif testPass == 1:
        print("Test data 2")
        data = '{"balance": 0.00000000,"stake": 549.87654321, "blocks": 13766, "timeoffset": 0"}'
    '''    

    # print(data)

    # parse getinfo data to get various values  - - - - - - - - - - - - - - - - - - - - - -
        
    balance = float(parse_number("balance", 0, 10, lenData, True))  # get balance
    # print("balance = ", balance)

    # find "stake to skip over "proof-of-stake"
    stake = float(parse_number('"stake', 0, 9, lenData, True))  # get stake
    # print("stake = ", stake)

    # if firstTimeThrough == True:   # otherwise block & delayedBlock set at the bottom of the loop   
    #     block = int(parse_number("blocks", 0, 9, lenData, False)) # get the current block
    #     delayedBlock = block - orphanDelay

    connections = int(parse_number("connections", 0, 14, lenData, False))  # get connections

    if connections == -1:
        print("connections = -1")
        print(data)

    # get_delegations_for_staker(4.0)       # for testing only

    '''
    Regression test - testnet
    
    Block   Issue
    678092  100% fee with gas refund
    646832
    646831
    648290  block reward + add delegate
    650003
    650325
    650936
    650937
    654246
    677826  split block reward + gas refund
    681459  100% fee two gas refunds
    695383  0% fee to pubkey delegate
    
    '''

    # delayedBlock = 694681                   # single block check, for testing ZZZZZ

    get_block(delayedBlock) 
    
    lenData = len(data)

    # print(data)

    # sys.exit(0)
    
    # print("lenData =", lenData)     # lenData = 1536

    # using block data, get the 2nd transaction for the coinstake tx - - - - - - - - - - - - - - 

    i = data.find("[")              # get the location of the opening brace

    # print("i =", i)
    
    start = i + 81 + OSDataIncr4    # fixed offset to 2nd transaction, adjust for Linux
    end = start + 64                # tx id 64 characters in length

    tx = ''

    for i in range(start, end):     # get the coinstake tx id
        tx += data[i]        

    # print("coinstake tx =", tx)
    # coinstake tx = 04c44efdd428cf4458d6753a8245134362f055b884192033c02e4f9bc1110a60

    strBlockTime = ""

    i = data.find("time")              # get the location of the opening brace

    i += 7

    while data[i] >= "0" and data[i] <= "9":

        strBlockTime += data[i]

        i += 1   
    
    # print("strBlockTime =", strBlockTime)
    
    # if this block mined by a super staker there will be a "proofOfDelegtion" field in the block

    i = data.find("proofOfDelegation", 0, lenData)

    # print("i PoD =", i)

    delegateAddress = ""

    if i > 0:
        
        isSuperStaker = True                    # use for sorting the block rewards below

        # print("isSuperStaker = True")

        # get the prevoutStakeHash, for determining delegate - - - - - - - - - - - - -

        i = data.find("prevoutStakeHash")

        # print("i prevoutStakeHash =", i)

        start = i + 20                  # fixed offset to start of hash
        end = start + 64                # tx id 64 characters in length

        for i in range(start, end):     # get the prevoutStakeHash, the UTXO kernel solution
            prevoutStakeHash += data[i]       

        # print("prevoutStakeHash =", prevoutStakeHash)

        # get the prevoutStakeVoutN, the vout number for the kernel solution - - - - - - - -

        i = data.find("prevoutStakeVoutN")

        # print("i prevoutStakeVoutN =", i)

        i += 20                         # fixed offset to number of Vout

        while data[i] != ",":           # get the digits
            prevoutStakeVoutN += data[i]
            i += 1

        # print("prevoutStakeVoutN =", prevoutStakeVoutN)

        # get the prevoutStakeHash transaction - - - - - - - - - - - - - - - - - - - - -

        params = OSPrefix +  "qtum-cli " + testnet + "getrawtransaction " + prevoutStakeHash + " true"
    
        # print(params)

        output = ""                     # clear it to see bad response

        tryNo = 0

        while True:
                
            try:
                output = str(subprocess.check_output(params, shell = True))
                break
            
            except:
                print("ERROR, get the prevoutStakehash transaction - no response from qtumd, try =", tryNo + 1)
                tryNo += 1
                time.sleep(tryNo * 0.3)
                
                if tryNo >= 4:
                    print("No response from qtumd, exiting")
                    sys.exit()

        data = str(output)
        lenData = len(data)

        # print("len data =", lenData)

        # print(data)

        i = data.find('vout\": [', 0)     # find the start of the vouts 'vout": ['

        # print("i start of vouts =", i)

        # loop through the vouts and find prevoutStakeVoutN

        # need to pubkey_to_base58(asm) in some cases       

        while i < lenData:

            i = data.find('\"n\":', i)

            if i > 0:           # found an output

                number = ''

                i += 5          # fixed offset to start of number digit(s)

                while data[i] != ",":
                    number += data[i]
                    i += 1
                    
                # print("number =", number, "prevoutStakeVoutN =", prevoutStakeVoutN)

                if int(number) == int(prevoutStakeVoutN):  # found it

                    # print("to here, i=", i)

                    # get next "value" if there is one

                    nextValue = data.find("value", i)

                    # print("nextValue =", nextValue)

                    addressesStart = data.find("addresses", i)

                    # print("addressesStart =", addressesStart)
                    
                    if addressesStart < nextValue or nextValue < 0:

                        # print("found an addressStart")

                        if addressesStart > 0:
                            
                            # print(data)

                            ''' Windows data shown
                            "value": 39999.89378253,\r\n      "valueSat": 3999989378253,\r\n      
                            "address": "qMmbHnEDDXBcmRq7e4JiFXTMzLWVptNjKD",\r\n      "sequence": 4294967294\r\n    }\r\n  ],\r\n  "vout": [\r\n    {\r\n
                            "value": 100.00000000,\r\n      "valueSat": 10000000000,\r\n      "n": 0,\r\n
                            "scriptPubKey": {\r\n        "asm": "OP_DUP OP_HASH160 2e2f9f90c84be1bcfa76670e1bd474edac8b4d00 OP_EQUALVERIFY OP_CHECKSIG",\r\n
                            "hex": "76a9142e2f9f90c84be1bcfa76670e1bd474edac8b4d0088ac",\r\n        "reqSigs": 1,\r\n        "type": "pubkeyhash",\r\n
                            "addresses": [\r\n          "qMmbHnEDDXBcmRq7e4JiFXTMzLWVptNjKD"\r\n        ]\r\n      }\r\n    },\r\n    {\r\n
                            '''
                            
                            start = addressesStart + 26 + OSDataIncr2         # fixed offset to start of address characters

                            end = start + 34   # get 34 character address

                            delegateAddress = ""

                            for i in range(start, end):
                                
                                delegateAddress += data[i]

                            # print("delegateAddress A =", delegateAddress)

                            break

                        else:    # some will have "address" for the delegate

                            # print(data)

                            '''
                            "txid": "3f051a<snip>04cff3",\r\n      "vout": 1,\r\n      "scriptSig": {\r\n      
                            "asm": "304402<snip>d854a58[ALL]",\r\n
                            "hex": "473044<snip>4a5801"\r\n      },\r\n 
                            "value": 143.62442508,\r\n      "valueSat": 14362442508,\r\n
                            "address": "qMkxbdz4kLXe4cMUn7vhhz2BPLXyCmMKn6",\r\n  
                            '''

                            addressStart = data.find("address")

                            # print("addressStart =", addressStart)

                            if addressStart > 0:
                                
                                start = addressStart + 11           # fixed offset to start of address characters

                                end = start + 34                    # get 34 character address

                                delegateAddress = ""

                                for i in range(start, end):
                                    
                                    delegateAddress += data[i]

                                # print("delegateAddress B =", delegateAddress)

                                break
                            
                    else:       # need to get "asm" which give public key for delegate

                        ''' 
                        "value": 169.60534469,\r\n      "valueSat": 16960534469,\r\n      "n": 1,\r\n
                        "scriptPubKey": {\r\n
                        "asm": "03428e0b878b2e06537aaf35f9b04ddf23157c9bb816c6661e8b6c068355c355bd OP_CHECKSIG",\r\n
                        "hex": "21034<snip>355bdac",\r\n        "type": "pubkey"\r\n      }\r\n    },\r\n    {\r\n
                        "value": 0.40000000,\r
                        '''

                        asmStart = data.find("asm", i)
                        
                        start = asmStart + 7 # + OSDataIncr2         # fixed offset to start of public key

                        end = start + 66   # get 55 character public key

                        publicKey = ""

                        for i in range(start, end):
                            
                            publicKey += data[i]

                        # print("publicKey =", publicKey)

                        delegateAddress = pubkey_to_base58(publicKey)

                        # print("delegateAddress from public key =", delegateAddress)

                        break

            else:
                break           # no more vouts 

    # get the coinstake transaction - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    '''
    to use getrawtransaction, qtumd must be started with "-txindex" command line
    parameter to maintain a full transaction index for use by getrawtransaction.
    will get "Syncing txindex with block chain from height nnnnnn" in debug log.
    '''

    params = OSPrefix +  "qtum-cli " + testnet + "getrawtransaction " + tx + " true"
    
    # print(params)
    # qtum-cli -testnet getrawtransaction 04c44efdd428cf4458d6753a8245134362f055b884192033c02e4f9bc1110a60 true
    # ./qtum-cli -testnet getrawtransaction 04c44efdd428cf4458d6753a8245134362f055b884192033c02e4f9bc1110a60 true

    # get the coinstake transaction for this block

    output = ""  # clear it to see bad response

    tryNo = 0

    while True:

        try:
            output = str(subprocess.check_output(params, shell = True))
            break
        
        except:
            print("ERROR, get coinstake transaction - no response from qtumd, try =", tryNo + 1)
            tryNo += 1
            time.sleep(tryNo * 0.3)
            
            if tryNo >= 4:
                print("No response from qtumd, exiting")
                sys.exit()
            
    data = str(output)
    lenData = len(data)

    # prevoutStakeHash, prevoutStakeVoutN set by here

    parse_coinstake(lenData)
    
    unixTime = int(time.time())

    # low connections checked with every new block. If low connections is discovered
    # which may be triggered if the network connection to the wallet PC is lost, or partially
    # lost, wait 7 blocks (about 15 minutes) before resending, using lowConnectionsAging
            
    if (unixTime - PPMStartTime) >= 1800:                # 30 minutes after PPM start
        if connections <= 5 and lowConnectionsAging <= 0:   # is this a good error quantity?
            print("ALERT: low connections, only", connections)
            sendLowConnectionsAlert = True              # send alert below
            lowConnectionsAging = 6                     # set for aging process

        elif connections <= 5:      # still in low connections situation
            lowConnectionsAging -= 1

        elif connections >= 6:
            lowConnectionsAging = 0  # reset it, no more low connections

    # print("connections = ", connections)

    # check "getstakinginfo"  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    ''' Typical response from Testnet v0.20.1
    {
      "staking": true,
      "errors": "",
      "currentblocktx": 0,
      "pooledtx": 0,
      "difficulty": 1862477.302164854,
      "search-interval": 2464,
      "weight": 7161665982933,
      "delegateweight": 60782006576365,
      "netstakeweight": 710952093708961,
      "expectedtime": 1339
    }

    '''

    params = OSPrefix + "qtum-cli " + testnet + "getstakinginfo"

    tryNo = 0

    while True:
  	
        try:
            output = subprocess.check_output(params, shell = True)
            break
           
        except:
            print("getstakinginfo, NO RESPONSE from qtumd, try =", tryNo + 1)
            tryNo += 1
            time.sleep(tryNo * 0.3)
            
            if tryNo >= 4:
                print("No response from qtumd, exiting")
                sys.exit()

    # print(output)

    data = str(output)

    # print(data)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # parse output to get enabled, staking, weight and netstakeweight, calculate immature

    '''
    # for testing
    if testPass == 0:
        print("Test data 1")
        data = '{"balance": 0.00000000,"stake": 0.00000000, "blocks": 13765, "timeoffset": 0"}'  
        testPass = 1
    elif testPass == 1:
        print("Test data 2")
        data = '{"balance": 0.00000000,"stake": 549.87654321, "blocks": 13766, "timeoffset": 0"}'
    '''

    temp = ''
    lenData = len(data)
    # print("lenData =", lenData)     # lenData = 297

    enabled = parse_logical("enabled", 10, lenData)  # get enabled     
    # print("enabled =", enabled)

    # confirm that staking is enabled, or send alert and wait here  - - - - - - - - - - - - - -

    while True:
        
        staking = parse_logical("staking", 10, lenData)       # get staking
        
        if forceTest == True:
            staking = True   # force for testing, with no mature coins or 0.0 balance
        
        if staking == True:
            sendOneTimeNotStaking = False   # reset to detect problem below, next pass
            # print("staking is True")
            break
        
        else:                       # not staking  :-(
            if sendOneTimeNotStaking == False:
                if sendEmail == True:
                    tempMessage = ".on " + hostName      
                    tempSubject = ".NOT STAKING"                                                    
                    send_email(tempSubject, tempMessage)
                    print("Sending email", tempSubject, tempMessage)
                sendOneTimeNotStaking = True

            if enableLogging == True:
                log("900, NOT STAKING")

            print('ERROR: qtumd not set for staking. Run qtum-cli walletpassphrase "passphrase" 99999999 true')
            time.sleep(15)  # give some time to fix this

    # weight is the mature UTXOs staking by this wallet           
    weight = float(parse_number("weight", 0, 9, lenData, False)) / 100000000  # get weight in QTUM
    # print("weight =", weight)

    # calculate delegatedWeight

    # print("weight =", weight, "balance =", balance)

    delegatedWeight = float(parse_number("delegateweight", 0, 17, lenData, False)) / 100000000  # get weight in QTUM ZZZZZ

    # print("delegatedWeight =", int(delegatedWeight))

    # delegatedWeight = weight - balance  # this is total wallet weight minus staker weight

    # print("delegatedWeight =", delegatedWeight, "weight =", weight, "balance =", balance)

    # calculate immature since qtumd doesn't seem to provide it
    # immature = balance - weight                     # coins that will mature after 500 blocks, but don't use it

    # get netstakeweight in millions, the calculated estimate of all QTUM currently being staked
    longNetworkWeight = float(parse_number("netstakeweight", 0, 17, lenData, False)) / 100000000
    networkWeight = int(longNetworkWeight)
    # print("networkWeight = ", networkWeight)

    # get expectedtime in hours, average time until the next block reward
    expectedTimeHours = float(parse_number("expectedtime", 0, 15, lenData, False)) / 3600
    # print("expectedTimeHours = ", expectedTimeHours)


    # format for display - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    '''
    Format the data for printing on a display. Add commas and calculate the pads to keep 
    the columns aligned. Numbers are right justified:

      time   |   block  |  balance |   stake   |   weight   | net weight | del weight | # del | con | stkg | exphr | staker | stk rwd | delgte | del rwd | pct | mypool |  pool bal | debug extra
    12:03:05 |  639,206 |  8,915.3 |   1,574.5 |  118,727.3 |  4,250,778 |    109,812 |     7 |  10 |  yes |   1.3 | qMYemS |   4.000 | q12345 |         |     |        |   176.072 | vins: 1
    12:03:35 |  639,207 |  8,915.3 |   1,574.5 |  118,727.3 |  4,245,527 |    109,812 |     7 |  10 |  yes |   1.3 | qMDYc9 |   4.000 | q12345 |         |     |        |   176.072 | vins: 1
    12:04:22 |  639,208 |  8,658.6 |   1,835.2 |  118,470.7 |  4,239,861 |    109,812 |     7 |  10 |  yes |   1.3 | qPooLF |   4.000 | q12345 |         |     | =YES=> |   180.072 | vins: 1
    12:06:13 |  639,209 |  9,019.3 |   1,470.5 |  118,831.3 |  4,236,148 |    109,812 |     7 |  10 |  yes |   1.3 | qMkxbd |   4.000 | q12345 |         |     |        |   180.072 | vins: 1
      time   |   block  |  balance |   stake   |   weight   | net weight | del weight | # del | con | stkg | exphr | staker | stk rwd | delgte | del rwd | pct | mypool |  pool bal | debug extra               
              \pad3      \pad1      \pad2      \pad4        \pad5        \pad9        \pad10  \pad7        \pad9                                         \pad11
    
    '''

    timestamp = int(strBlockTime)
    value = datetime.fromtimestamp(timestamp)
    orphanDelayedTime = f"{value:%H:%M:%S}"
                    
    # orphanDelayTime = strBlockTime.strftime("%H:%M:%S")  
    # print(orphanDelayTime)

    # unixTime = int(time.time())
    # now = datetime.now()
    # current_time2 = now.strftime("%H:%M:%S")

    if delayedBlock <= 999999:                              
        blockWithCommas = "{:,d}".format(int(delayedBlock))
        pad3 = " " * (8 - len(blockWithCommas))
        blockPadCommas = pad3 + blockWithCommas
    else:
        blockPadCommas = "xxxxxxxxx"        

    if balance <= 9999999.9:
        balanceWithCommas = ("{:,f}".format(round(balance, 1)))[:-5]
        pad1 = " " * (11 - len(balanceWithCommas))
        balancePadCommas = pad1 + balanceWithCommas
    else:
        balancePadCommas = "xxxxxxxxxxx"

    if stake <= 999999.9:
        stakeWithCommas = ("{:,f}".format(round(stake, 1)))[:-5]
        pad2 = " " * (9 - len(stakeWithCommas))
        stakePadCommas = pad2 + stakeWithCommas
    else:
        stakePadCommas = "xxxxxxxxx"

    if weight <= 99999999.9:
        weightWithCommas = ("{:,f}".format(round(weight, 1)))[:-5]
        pad4 = " " * (11 - len(weightWithCommas))
        weightPadCommas = pad4 + weightWithCommas
    else:
        weightPadCommas = "xxxxxxxxxxx"

    if networkWeight <= 99999999:
        networkWeightWithCommas =  "{:,d}".format(int(networkWeight))
        pad5 = " " * (10 - len(networkWeightWithCommas))
        networkWeightPadCommas = pad5 + networkWeightWithCommas
    else:
        networkWeightPadCommas = "xxxxxxxxxx"

    if delegatedWeight <= 99999999:
        delegatedWeightWithCommas =  ("{:,f}".format(round(delegatedWeight, 1)))[:-5]
        pad9 = " " * (12 - len(delegatedWeightWithCommas))
        delegatedWeightPadCommas = pad9 + delegatedWeightWithCommas
    else:
        delegatedWeightPadCommas = "xxxxxxxxxx"

    if numDelegates <= 9999:
        numDelegatesWithComma =  "{:,d}".format(int(numDelegates))
        pad10 = " " * (5 - len(numDelegatesWithComma))
        numDelegatesPadComma = pad10 + numDelegatesWithComma
    else:
        numDelegatesPadComma = "xxxxx"              

    # connections is a low range integer, say 0 to 120, and doesn't need commas
    if connections <= 999:
        strConnections = str(connections)
        pad7 = " " * (3 - len(strConnections))
        connectionsPad = pad7 + strConnections
    else:
        connectionsPad = "xxx"

    if staking == True:
        stakingForEmail = " yes"  # yes
    else:
        stakingForEmail = " NOT"  # no, but get blocked above, should never get here

    if expectedTimeHours <= 999:
        exphrsWithCommas = ("{:,f}".format(round(expectedTimeHours, 1)))[:-5]
        pad8 = " " * (5 - len(exphrsWithCommas))
        exphrsPadCommas = pad8 + exphrsWithCommas
    else:
        exphrsPadCommas = "xxxxx"

    stakerFirst6 = stakerAddress[:6]       # qMkxbD

    if stakerReward < 99.9994:
        formattedStakerReward = "{:7.3f}".format(round(stakerReward, 3))
    else:
        formattedStakerReward = "xxxxxx"

    if len(delegateAddress) != 34:                      # not a delegate address
        delegateAddressFormatted = "none"
        delegateAddressFirst6 = "      "
    else:
        delegateAddressFormatted = delegateAddress
        delegateAddressFirst6 = delegateAddress[:6]     # get the first 6 characters

    if isSuperStaker == False:
        formattedDelegateReward = "       "  
    else:    
        if delegateReward == 0:
            formattedDelegateReward = "  0.000"   # for 100% fee the delegate reward would be 0.0   
        elif delegateReward <= 99.9994:
            formattedDelegateReward = "{:7.3f}".format(round(delegateReward, 3))  # 4.456
        else:
            formattedDelegateReward = "xxxxxx"

    # percent fee is 0 to 100, and doesn't need commas

    divider1 = "│"         # divider character for most fields, non-super stakers
    divider2 = "│"

    if isSuperStaker == True:   # should be same logic as for logging

        if isPoolBlockReward == False:
            divider1 = "▌"      # divider char left half block for super staker
            divider2 = "▐"      # divider char right half block for super staker
        else:                   # mySuperStaker
            divider1 = "█"      # divider char full block for my super staker
            divider2 = "█"      # divider char full block for my super staker            
        
        if percentFee >= 0 and percentFee <= 100:
            strPercentFee = str(percentFee)
            pad11 = " " * (3 - len(strPercentFee))
            percentFeePad = pad11 + strPercentFee

        else:
            percentFeePad = "xxx"
    else:
        percentFeePad = "   "        

    if isMyMiner == True:
        if isPoolBlockReward == True:
            poolBlockRewardText = "=YES=>"  # miner staked from delegated UTXOs
        else:
            poolBlockRewardText = " self "  # miner staked from its own UTXOs
            divider1 = "░"                  # divider character for self
            divider2 = "░"

    else:
        poolBlockRewardText = "      "

    poolBalanceUnits = float(intsatsPoolBalance / 100000000)

    if poolBalanceUnits == 0:
        strPoolBalanceUnitsPad = "      0.0"    # no pool balance yet
        
    elif poolBalanceUnits <= 999.9994:
        strPoolBalanceUnits = "{:.3f}".format(round(poolBalanceUnits, 3))  # 4.456
        pad12 = " " * (9 - len(strPoolBalanceUnits))
        strPoolBalanceUnitsPad = pad12 + strPoolBalanceUnits
        
    else:
        strPoolBalanceUnitsPad = "xxxxxxxxx"        

    rightSideExtraFormatted = rightSideExtra

    # format for log and emails - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # unixTimeFormatted = str(unixTime)
    unixTimeFormatted = strBlockTime
    
    blockFormatted = str(delayedBlock)
    
    balanceFormatted = format(balance, ".1f")
    
    balanceForEmail = format(balance, "0.1f")
    
    stakeFormatted = format(stake, ".1f")
    
    # stakeForEmail = format(stake, "0.1f")
    stakeForEmail = format(12345.678, "0.1f")
    
    weightFormatted = format(weight, " 08.1f")
    
    weightForEmail = format(weight, " 0.1f")
    
    networkWeightFormatted = format(networkWeight, "1d")
    
    networkWeightForEmail = format(networkWeight, "1d")
    
    delegatedWeightFormatted = format(int(delegatedWeight), "1d")

    numDelegatesFormatted = str(numDelegates)
    
    connectionsFormatted = str(connections)

    # stakingForEmail set above

    expectedTimeHoursFormatted = format(expectedTimeHours, ".1f")

    staker = stakerAddress              # rename this to miner or smth?
    
    stakerRewardFormatted = format(stakerReward, ".3f")

    # delegateAddressFormatted set above
        
    delegateRewardFormatted = format(delegateReward, ".3f")

    if percentFee == -1:   # did't find a super staker and set the fee
        percentFeeFormatted = "nan"         # not a number
    else:
        percentFeeFormatted = str(percentFee)

    if isPoolBlockReward == False:          # is this the best for Excel sorting?
        myPoolFormatted = "no"
    else:
        myPoolFormatted = "yes"

    poolBalanceFormatted = format(poolBalanceUnits, ".3f")

    # rightSideFormatted set above


    # send email if alerts have been set  - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if sendNewSingleBlockReward == True:  # found a new block reward above
        sendNewSingleBlockReward = False  # reset it

        stakeForEmail = format(stake, "0.1f") + " "
        tempMessage = "." + hostName + " blk " + str(delayedBlock) + " stk " + stakeForEmail
        tempSubject = ".REWARD"
                    
        if sendEmail == True:
            send_email(tempSubject, tempMessage)
            print("Sending email", tempSubject, tempMessage)

        # if enableLogging == True:
        #     log("400, REWARD")
            
    if sendLowConnectionsAlert == True:
        sendLowConnectionsAlert = False

        tempMessage = "." + hostName + " only " + str(connections)
        tempSubject = ".LOW CONNECTIONS"

        if sendEmail == True:
            send_email(tempSubject, tempMessage)
            print("Sending email", tempSubject, tempMessage)  

        if enableLogging == True:
            log("900, LOW CONNECTIONS")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    if delayedBlock % 10 == 0:          # print the labels every 10 blocks (rows)
        if printBlockMod10 == True:
            printBlockMod10 = False     # protect against multiple prints when block % 10 is true
            print(labelRow)
    else:
        printBlockMod10 = True          # arm for next block % 10 is true
      
    if sendEmailForNewHour == False:    # avoids double print if coming through here for new hour 
        
        print(orphanDelayedTime, "\u2502", blockPadCommas, "\u2502", balancePadCommas, "\u2502", stakePadCommas, "\u2502", weightPadCommas,\
              "\u2502", networkWeightPadCommas, "\u2502", delegatedWeightPadCommas, "\u2502", numDelegatesPadComma, "\u2502",\
              connectionsPad, "\u2502", stakingForEmail, "\u2502", exphrsPadCommas, divider1, stakerFirst6, divider2,\
              formattedStakerReward, "\u2502", delegateAddressFirst6, "\u2502", formattedDelegateReward, "\u2502", percentFeePad,\
              "\u2502", poolBlockRewardText, "\u2502", strPoolBalanceUnitsPad, "\u2502" + rightSideExtra)

    if logNewBlock == True:  # found a new block below, log it
        logNewBlock = False

        if enableLogging == True:  # for log (and Excel) no commas, Excel ingnores leading zeros 
            
            log("100," + unixTimeFormatted +"," + orphanDelayedTime + "," + blockFormatted + "," + balanceFormatted + "," + stakeFormatted +\
                      "," + weightFormatted + "," + networkWeightFormatted + "," + delegatedWeightFormatted + "," + numDelegatesFormatted + "," +\
                      connectionsFormatted + "," + stakingForEmail + "," + expectedTimeHoursFormatted + "," + staker + "," + stakerRewardFormatted +\
                      "," + delegateAddressFormatted + "," + delegateRewardFormatted + "," + percentFeeFormatted + "," + myPoolFormatted + "," +\
                      poolBalanceFormatted + "," + rightSideExtraFormatted)

    # send hourly status email  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if sendEmailForNewHour == True:
        
        if sendHourlyEmail == True:          # okay to send hourly status email
            tempMessage =  " bal " + balanceWithCommas + " blk " + blockWithCommas + " mwt " + weightWithCommas + " dwt " + delegatedWeightFormatted + " stking " +  stakingForEmail
            tempSubject = "." + hostName + " stk " + stakeWithCommas
                          
            if sendEmail == True:
                send_email(tempSubject, tempMessage)

    sendEmailForNewHour = False

    # print("new block loop slack", lastBlockCheckTime + delayBlockWaiting - timer())
    # typical: new block loop slack 1.470697567243377

    # this is the delay that runs a single time after each new block is detected
    # set to 4.0 on 10/13/2017, but finding a 4 second block
    # set to 3.0 on 10/14/2017

    while True:         # wait here until we get to 4 seconds from the last block check
        if timer() > lastBlockCheckTime + delayBlockWaiting:
            break
        else:
            time.sleep(0.1)

    # new block waiting loop  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    breakOut = False  # kludge to allow break from 2 levels

    while breakOut == False:
        end = timer()
        # print("Loop =", format(end - startTimer, "0.2f")) 

        lastBlockCheckTime = timer()
        
        params = OSPrefix + "qtum-cli " + testnet + "getblockcount"

        tryNo = 0

        while True:
            
            try:
                output = subprocess.check_output(params, shell = True)
                break
                
            except:
                print("new block waiting loop, NO RESPONSE from qtumd, try =", tryNo + 1)
                tryNo += 1
                time.sleep(tryNo * 0.3)
                
                if tryNo >= 4:
                    print("No response from qtumd, exiting")
                    sys.exit()

        # print(output)

        data = str(output)
        lenData = len(data)

        # print(data)

        strBlock = ""

        for i in range(2, lenData):

            if data[i] >= "0" and data[i] <= "9":
                strBlock += data[i]
            else:
                break

        # print(strBlock)    
        
        block = int(strBlock)
            
        if block != oldBlock:  # found a new block
            # print("found a new block =", block)
            
            delayedBlock = block - orphanDelay      # process a previous block to avoid orphans
            
            # print("block C = ", block, "delayedBlock =", delayedBlock)
            
            end2 = timer()
            newDuration = int(end2 - start2) # saves the time since the last block
            start2 = timer()

            # print("block =", block, "oldBLock =", oldBlock, "firstTimeThrough =", firstTimeThrough)
                  
            if int((block) != int(oldBlock) + 1): #  and firstTimeThrough == False:
                # print("MISSED BLOCK", oldBlock + 1, "going back for it")
                block = oldBlock + 1    # go read previous block and process
                                        # then get the next one right away

                delayedBlock = block - orphanDelay
                # print("block D = ", block, "delayedBlock =", delayedBlock)

            oldBlock = block                 # save for check next block
            firstTimeDontMissBlock = False   # allow check for missing block next time
            now = datetime.now()
            blockTime = now.strftime("%H:%M:%S") # save for use in stale block alert

            unixFoundBlockTime = int(time.time())
            
            # on average, subtract half of delayDateHours, but this understates the
            # superfast blocks, e.g., a 4 second block was logged as 3 seconds
            # so don't correct if the newDuration is under one minute
            
            savedUnixBlockTime = int(time.time()) 	 # save for determining stale blocks
            blocksToday += 1        # count the blocks today, accurate if PPM runs 24x7
            logNewBlock = True      # set to log the new block above

            staleBlockAging = 0     # reset to catch stale block below
            break

        else:
            unixBlockTime = int(time.time())

        firstTimeThrough = False  # reset (and keep resetting) after first time through

        # date and hours waiting loop  - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # print("date and hours loop, slack ", lastBlockCheckTime + delayDateHours - timer())
        # typical: date and hours loop, slack  2.6042726875139124
        
        while timer() <= lastBlockCheckTime + delayDateHours:

            # print("timer =", timer(), "sum =", lastBlockCheckTime + delayDateHours)

            time.sleep(0.3)

            unixTime = int(time.time())

            # unixTime += 13800   # used to force end of day at other times, for testing

            # print("unixTime % 86400 =", unixTime % 86400)

            # End of day - payout the pool and make a new log file  - - - - - - - - - - - - - - - - - - - - - -

            # do not break out of the date hours waiting loop for a new day

            # testUnixTime = unixTime - 4380

            # print("testUnixTime = ", testUnixTime, "testUnixTime % 86400 =", testUnixTime % 86400)

            if (unixTime % 86400) < 4 and didNewLog == False:  # catch the first four seconds of a new GMT day

                payout_with_sendmany(poolFee)   # pay out the pool, on a daily basis

                didNewLog = True            # toggle to only do one time for each new day
          
                if enableLogging == True:

                    blocksTodayFormatted = str(blocksToday)         # the number of blocks today, if PPM running all day
                    
                    log("200, blocks," + blocksTodayFormatted)

                    blocksToday = 0     # reset for new day

                print("Making new log file, new day")

                # initialize log file for new day
                if enableLogging == True:
                    GMT = strftime("%a, %d %m %Y %H:%M:%S", time.gmtime())  # GMT
                    # open log file in the format "PPM_Log_YYYY_MMM_DD.csv"

                    log_file_name_PPM = 'PPM_Log_'+GMT[11]+GMT[12]+GMT[13]+GMT[14]+'_'+GMT[8]+GMT[9]+\
                                    '_'+GMT[5]+GMT[6]+'.csv'

                    thisDirectory = os.path.dirname(os.path.realpath(__file__))

                    if isLinux:
                        logsSubdirectoryFilename = thisDirectory + "/logs/" + log_file_name_PPM
                    else:     # Windows    
                        logsSubdirectoryFilename = thisDirectory + "logs\\" + log_file_name_PPM

                    print("PPM log file name new day =", logsSubdirectoryFilename)

                    try: # create or open log file for appending
                        logFilePPM = open(logsSubdirectoryFilename, 'a')
                        print("PPM file open for appending")
                        # print("Opening file", logsSubdirectoryFilename, "on", GMT)
                        log("000,Program,start,or,restart,version," + version)
                        # tempStr = '000,Logging,start,' + '_' + GMT[17]+GMT[18]+GMT[20]+GMT[21]+\
                        #           ',hours,GMT,'+GMT[5]+GMT[6]+'_'+\
                        #           GMT[8]+GMT[9]+GMT[10]+'_'+GMT[12]+GMT[13]+GMT[14]+GMT[15]
                        log('000,Logging,start,' + '_' + GMT[17]+GMT[18]+GMT[20]+GMT[21]+\
                            ',hours,GMT,'+GMT[5]+GMT[6]+'_'+\
                            GMT[8]+GMT[9]+GMT[10]+'_'+GMT[12]+GMT[13]+GMT[14]+GMT[15])
                        log(logLabels)  # write a row of column labels

                    except IOError:   # NOT WORKING
                        print("PPM ERROR: File didn't exist, open for appending")
            elif didNewLog == True and (unixTime % 86400) >= 15:
                didNewLog = False   # kludge?

            # detect a new hour - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

            # start 4 seconds early because it takes some time to read process and process qtum-cli calls above

            unixTimeEarly = unixTime + 4    # go 4 seconds early, but compare to delayDateHour also
                                            # that is, if delayDateHour is reduced, consider
                                            # reducing this go early value too
                                            
            # print("unixTimeEarly =", unixTimeEarly)

            # catch the first four seconds of a new hour
            if (unixTimeEarly % 3600) <= 4 and didNewHour == False:
                didNewHour = True                              # block for the next few seconds
                sendEmailForNewHour = True
                breakOut = True         # break out of new block waiting loop, back to the top
                # print("breakOut, hour change, unixTime =", unixTime)
                break

            elif didNewHour == True and (unixTimeEarly % 3600) >= 10:
                didNewHour = False    # reset it for the next hour transtion
                # print("didNewHour set to False")

        # end of date hours waiting loop

    # print(unixTime)

    params = OSPrefix + "qtum-cli " + testnet + "-getinfo"

    tryNo = 0

    while True:

        try:
            output = subprocess.check_output(params, shell = True)
            break
           
        except:
            print("bottom of waiting loop, NO RESPONSE from qtumd, try =", tryNo + 1)
            tryNo += 1
            time.sleep(tryNo * 0.3)
            
            if tryNo >= 4:
                print("No response from qtumd, exiting")
                sys.exit()

    # print(output)
    
    data = str(output)
    lenData = len(data)
    # print("lenData -getinfo bottom of main =", lenData)

    # end of while True, MAIN PROGRAM LOOP
