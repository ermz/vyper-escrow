import pytest
from brownie import Wei, ZERO_ADDRESS, accounts, escrow
from eth_hash.auto import keccak

@pytest.fixture
def _escrow():
    _escrow = escrow.deploy({'from': accounts[5]})
    return _escrow

def test_add_item_escrow(_escrow):
    _asset_key = keccak(b'Paintin_NFT')
    _asset_cost = 25
    assert _escrow.assetOwner(_asset_key) == ZERO_ADDRESS
    assert _escrow.viewAssetPrice(accounts[6], _asset_key) == 0
    _escrow.addItemToEscrow(_asset_key, _asset_cost, {'from': accounts[6]})
    assert _escrow.assetOwner(_asset_key) == accounts[6]
    assert _escrow.viewAssetPrice(accounts[6], _asset_key) == 25

# Could potentially also check address balance to make sure that overflow of ether was sent back
def test_buy_item(_escrow):
    _asset_key = keccak(b'PictureNFT')
    _asset_cost = 1
    assert _escrow.myMoney({'from': accounts[6]}) == 0
    _escrow.addItemToEscrow(_asset_key, _asset_cost, {'from': accounts[6]})
    assert _escrow.assetOwner(_asset_key) == accounts[6]
    _escrow.buyItemFromEscrow(accounts[6], _asset_key, {'from': accounts[7], 'value': '2 ether'})
    assert _escrow.myMoney({'from': accounts[6]}) == 1
    assert _escrow.assetOwner(_asset_key) == accounts[7]

# Have to come back and check how to check balance of smart contract
def test_get_paid(_escrow):
    _asset_key = keccak(b'KeyboardNFT')
    _asset_cost = 1
    _escrow.addItemToEscrow(_asset_key, _asset_cost, {'from': accounts[8]})
    _escrow.buyItemFromEscrow(accounts[8], _asset_key, {'from': accounts[9], 'value': '1 ether'})
    assert _escrow.myMoney({'from': accounts[8]}) == 1
    _escrow.getPaid({'from': accounts[8]})
    assert _escrow.myMoney({'from': accounts[8]}) == 0


