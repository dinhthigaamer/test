# tech
# Built with Seahorse v0.2.7

from seahorse.prelude import *

declare_id('B9kViFpeL3ShhoQkfCX8LKZsisZuPhCiabcpEG3nXPvV')

class HopDong(Account):
    owner: Pubkey # 32 bytes
    student: Pubkey # 32 bytes
    is_done: bool # 8 bytes
    price: u64 # 8 bytes
    message_u16_128_array: Array[u16, 128]

@instruction
def init_hopdong(
    # Account
    payer: Signer,
    owner: Signer,
    student: Signer,
    hopdong: Empty[HopDong],
    # Data
    seed_sha256: u128,
    price: u64,
    message_u16_128_array: Array[u16, 128]
):
    hopdong = hopdong.init(payer = payer, seeds = [owner, "hopdong", seed_sha256])
    hopdong.student = student.key()
    hopdong.price = price
    hopdong.message_u16_128_array = message_u16_128_array

    # Check if user have enough money
    # Transfer money to owner
    student.transfer_lamports(owner, hopdong.price)

@instruction
def xacnhan_done(
    # Account
    payer: Signer,
    owner: Signer,
    student: Signer,
    hopdong: HopDong
):
    assert owner.key() == hopdong.owner, "Hopdong owner not same!"
    assert student.key() == hopdong.student, "Hopdong student not same!"
    assert hopdong.is_done == False, "Hopdong already done!"

    hopdong.is_done = True

    # Check if user have enough money
    # Transfer money to owner
    payer.transfer_lamports(owner, hopdong.price)

class UserAccount(Account):
    name: str
    address_u16_64_array: Array[u16, 64]
    phone_number_u8_5_array: Array[u8, 5]
    public_key: Pubkey
    secret_key_u8_32_array: Array[u8,32]

@instruction
def UpdateUserAccount(
    #Account
    user: UserAccount,
    #Data
    address_u16_64_array: Array[u16, 64],
    phone_number_u8_5_array: Array[u8, 5],
    secret_key_u8_32_array: Array[u8,32]
):
    assert user.secret_key_u8_32_array == secret_key_u8_32_array, "Incorrect Secret_key"
    user.address_u16_64_array = address_u16_64_array
    user.phone_number_u8_5_array = phone_number_u8_5_array

@instruction
def RegisterClass(
    #Account
    student: Signer,    
    owner: Signer,
    class_price: Pubkey,
    #Data
    seed_sha256: u128,
    price: u64,
    message_u16_128_array: Array[u16, 128]
):

    init_hopdong(payer = student, 
                 owner = owner, 
                 student = student,
                 price = price,
                 seed_sha256 = seed_sha256,
                 message_u16_128_array = message_u16_128_array
                )

@instruction
def CancelClass(
    student: Signer,
    owner: Signer,
    hopdong: HopDong
):
    xacnhan_done(payer = owner, owner = owner, student = student, hopdong = hopdong)
