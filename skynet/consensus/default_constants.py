from skynet.util.ints import uint64

from .constants import ConsensusConstants

testnet_kwargs = {
    "SLOT_BLOCKS_TARGET": 32,
    "MIN_BLOCKS_PER_CHALLENGE_BLOCK": 16,  # Must be less than half of SLOT_BLOCKS_TARGET
    "MAX_SUB_SLOT_BLOCKS": 128,  # Must be less than half of SUB_EPOCH_BLOCKS
    "NUM_SPS_SUB_SLOT": 64,  # Must be a power of 2
    "SUB_SLOT_ITERS_STARTING": 2 ** 27,
    # DIFFICULTY_STARTING is the starting difficulty for the first epoch, which is then further
    # multiplied by another factor of DIFFICULTY_CONSTANT_FACTOR, to be used in the VDF iter calculation formula.
    "DIFFICULTY_CONSTANT_FACTOR": 2 ** 60,
    "DIFFICULTY_STARTING": 7,
    "DIFFICULTY_CHANGE_MAX_FACTOR": 3,  # The next difficulty is truncated to range [prev / FACTOR, prev * FACTOR]
    # These 3 constants must be changed at the same time
    "SUB_EPOCH_BLOCKS": 384,  # The number of blocks per sub-epoch, mainnet 384
    "EPOCH_BLOCKS": 4608,  # The number of blocks per epoch, mainnet 4608. Must be multiple of SUB_EPOCH_SB
    "SIGNIFICANT_BITS": 8,  # The number of bits to look at in difficulty and min iters. The rest are zeroed
    "DISCRIMINANT_SIZE_BITS": 1024,  # Max is 1024 (based on ClassGroupElement int size)
    "NUMBER_ZERO_BITS_PLOT_FILTER": 9,  # H(plot signature of the challenge) must start with these many zeroes
    "MIN_PLOT_SIZE": 32,  # 32 for mainnet
    "MAX_PLOT_SIZE": 50,
    "SUB_SLOT_TIME_TARGET": 600,  # The target number of seconds per slot, mainnet 600
    "NUM_SP_INTERVALS_EXTRA": 3,  # The number of sp intervals to add to the signage point
    "MAX_FUTURE_TIME": 5 * 60,  # The next block can have a timestamp of at most these many seconds in the future
    "NUMBER_OF_TIMESTAMPS": 11,  # Than the average of the last NUMBER_OF_TIMESTAMPS blocks
    # Used as the initial cc rc challenges, as well as first block back pointers, and first SES back pointer
    # We override this value based on the chain being run (testnet_09, testnet_09, mainnet, etc)
    # Default used for tests is std_hash(b'')
    "GENESIS_CHALLENGE": bytes.fromhex("5a5a3495f3ebeed006fba3c540cfd0519164bad5783d174a276379cb08395362"),
    # Forks of skynet should change this value to provide replay attack protection. This is set to mainnet genesis chall
    "AGG_SIG_ME_ADDITIONAL_DATA": bytes.fromhex("af0037ce4927cd5212734a87bae07454580f2d9986734908bac2031fe852de79"),
    "GENESIS_PRE_FARM_POOL_PUZZLE_HASH": bytes.fromhex(
        "e9a8b36d5c84b96f39e5262980eacc193e597fc9d254417f806190de5e598bc4"
    ),
    "GENESIS_PRE_FARM_FARMER_PUZZLE_HASH": bytes.fromhex(
        "e9a8b36d5c84b96f39e5262980eacc193e597fc9d254417f806190de5e598bc4"
    ),
    "MAX_VDF_WITNESS_SIZE": 64,
    # Size of mempool = 50x the size of block
    "MEMPOOL_BLOCK_BUFFER": 50,
    # Max coin amount, fits into 64 bits
    "MAX_COIN_AMOUNT": uint64((1 << 64) - 1),
    # Max block cost in clvm cost units
    "MAX_BLOCK_COST_CLVM": 11000000000,
    # The cost per byte of generator program
    "COST_PER_BYTE": 12000,
    "WEIGHT_PROOF_THRESHOLD": 2,
    "BLOCKS_CACHE_SIZE": 4608 + (128 * 4),
    "WEIGHT_PROOF_RECENT_BLOCKS": 1000,
    "MAX_BLOCK_COUNT_PER_REQUESTS": 32,  # Allow up to 32 blocks per request
    "INITIAL_FREEZE_END_TIMESTAMP": 1626739201, # 20 07 2021 00:00:01 GMT+0000
    "NETWORK_TYPE": 0,
    "MAX_GENERATOR_SIZE": 1000000,
    "MAX_GENERATOR_REF_LIST_SIZE": 512,  # Number of references allowed in the block generator ref list
    "POOL_SUB_SLOT_ITERS": 37600000000,  # iters limit * NUM_SPS
    "TIMELORD_PUZZLE_HASH": bytes.fromhex(
        "e9a8b36d5c84b96f39e5262980eacc193e597fc9d254417f806190de5e598bc4"
    ),
}


DEFAULT_CONSTANTS = ConsensusConstants(**testnet_kwargs)  # type: ignore
