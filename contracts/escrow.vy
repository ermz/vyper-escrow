# @version ^0.2.0

# someone initiates the escrow and they become the one that holds all the information
# only they can distribute the money that is sent

admin: address

@external
def __init__():
    self.admin = msg.sender

# Takes the address of owner and returns an item and the price they expect
assets: HashMap[address, HashMap[bytes32, uint256]]

# the bytes32 of an item and the address that owns it
possessions: HashMap[bytes32, address]

bank: HashMap[address, uint256]

@external
@view
def viewAssetPrice(_seller: address, _asset: bytes32) -> uint256:
    return self.assets[_seller][_asset]

@external
@view
def myMoney() -> uint256:
    return self.bank[msg.sender]

@external
@view
def assetOwner(_asset: bytes32) -> address:
    return self.possessions[_asset]

@external
def addItemToEscrow(_asset: bytes32, _cost: uint256) -> bool:
    assert msg.sender != self.admin, "Admin can't add items"
    # There's probably a better way to check that msg.sender doesn't already have an asset in escrow
    assert self.assets[msg.sender][_asset] == 0
    assert self.possessions[_asset] == ZERO_ADDRESS
    self.assets[msg.sender][_asset] = _cost
    self.possessions[_asset] = msg.sender
    return True

@external
@payable
def buyItemFromEscrow(_seller: address, _asset: bytes32) -> bool:
    # Can improve this by returning ether, if buyer sen't too much
    assert msg.value >= self.assets[_seller][_asset], "There isn't enough to cover the cost of asset"
    amount_difference: uint256 = msg.value - self.assets[_seller][_asset]
    if amount_difference >= 0:
        send(msg.sender, amount_difference)
    self.bank[_seller] += self.assets[_seller][_asset]
    self.possessions[_asset] = msg.sender
    self.assets[_seller][keccak256('0')] = 0
    return True

@external
@payable
def getPaid() -> bool:
    # This function will both get the seller paid and remove the possesion away from escrow
    assert self.bank[msg.sender] > 0, "You have nothing to collect"
    send(msg.sender, self.bank[msg.sender])
    self.bank[msg.sender] = 0
    return True




