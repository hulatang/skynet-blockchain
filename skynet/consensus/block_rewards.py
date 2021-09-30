from skynet.full_node.block_store import BlockStore
from skynet.util.ints import uint32, uint64

##################################################################
# Algo_rewards
##################################################################

# 1 Skynet coin = 1,000,000,000,000 = 1 trillion synt.
_synt_per_skynet = 1000000000000
_blocks_per_year = 1681920    # 32 * 6 * 24 * 365
_year_jolly_blocks = 99999    # n. of blocks with 5 XNT reward every years
_jolly_reward_mlt = 1         # jolly reward moltiplicator
_halving_factor = 2 / 5       # reward decreaser factor yrs<=10
_pool_reward_mlt = 7 / 8      # 87,5% of reward
_farmer_reward_mlt = 1 / 8    # 12.5% of reward
_timelord_fee_mlt = 0.1 / 100 # 0.1% of fee for block processed
block_store: BlockStore = BlockStore

def round_reward(num) -> int:
    return int(str(num)[:2] + "00000000000")

def calculate_pool_reward(height: uint32) -> uint64:
    """
    The base fee reward is 87.5% of total block reward
    If the farmer is solo farming, they act as the pool, and therefore earn the entire block reward.
    !! These halving events will not be hit at the exact times
    (3 years, etc), due to fluctuations in difficulty. They will likely come early, if the network space and VDF
    rates increase continuously.
    """
    if height == 0:
        return uint64(int(_pool_reward_mlt * 5000000 * _synt_per_skynet))
    else:
        year = 1

        _jolly_reward_mlt = block_store.get_block_reward_mlt(height)

        while True:
            if height < year * _blocks_per_year and height > (year * _blocks_per_year) - _year_jolly_blocks:
                return uint64(int(_pool_reward_mlt * 5 * _synt_per_skynet))
            elif height < year * _blocks_per_year:
                if year == 1:
                    return uint64(int(_pool_reward_mlt * (5*_jolly_reward_mlt) * _synt_per_skynet))
                elif year > 1 and year <= 10:
                    return uint64(int(_pool_reward_mlt * round_reward(((5 - (year * _halving_factor))*_jolly_reward_mlt) * _synt_per_skynet)))
                elif year > 10:
                    return uint64(int(_pool_reward_mlt * (0.5*_jolly_reward_mlt) * _synt_per_skynet))
            else: year += 1

def calculate_base_farmer_reward(height: uint32) -> uint64:
    """
    The base fee reward is 12.5% of total block reward
    !! These halving events will not be hit at the exact times
    (3 years, etc), due to fluctuations in difficulty. They will likely come early, if the network space and VDF
    rates increase continuously !!
    """
    if height == 0:
        return uint64(int(_farmer_reward_mlt * 5000000 * _synt_per_skynet))
    else:
        year = 1
    
        _jolly_reward_mlt = block_store.get_block_reward_mlt(height)

        while True:
            if height < year * _blocks_per_year and height > (year * _blocks_per_year) - _year_jolly_blocks:
                return uint64(int(_farmer_reward_mlt * 5 * _synt_per_skynet))
            elif height < year * _blocks_per_year:
                if year == 1:
                    return uint64(int(_farmer_reward_mlt * (5*_jolly_reward_mlt) * _synt_per_skynet))
                elif year > 1 and year <= 10:
                    return uint64(int(_farmer_reward_mlt * round_reward(((5 - (year * _halving_factor))*_jolly_reward_mlt) * _synt_per_skynet)))
                elif year > 10:
                    return uint64(int(_farmer_reward_mlt * (0.5*_jolly_reward_mlt) * _synt_per_skynet))
            else: year += 1

def calculate_base_timelord_fee(height: uint32) -> uint64:
    """
    The base fee reward is 0.1% of total block reward
    !! These halving events will not be hit at the exact times
    (3 years, etc), due to fluctuations in difficulty. They will likely come early, if the network space and VDF
    rates increase continuously !!
    """
    year = 1
    while True:
        if height < year * _blocks_per_year:
            if year == 1:
                return uint64(int(_timelord_fee_mlt * 5 * _synt_per_skynet))
            elif year > 1 and year <= 10:
                return uint64(int(_timelord_fee_mlt * round_reward((5 - (year * _halving_factor)) * _synt_per_skynet)))
            elif year > 10:
                return uint64(int(_timelord_fee_mlt * 0.5 * _synt_per_skynet))
        else: year += 1
