pragma solidity 0.8.x;
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/SafeMath.sol";

contract ShroomMarket {

    address dai_address = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    ERC20 DAI = ERC20(dai_address);

    /*
      Fantasy magic shroom market, by Charlie and his clearly incompetent solidity elves.
      Warning! This code is not fit for purpose!
     */

    // keccak256(abi.encode(address _seller, bytes _offer_id, address _customer)) aka ask_id => total_in_DAI
    mapping (bytes32 => uint256) public asks;

    event Ask (
        bytes customer_pubk,
        address customer,
        address seller,
        uint256 total
    );

    event Confirm (
        bytes32 ask_id,
        bytes location
    );

    constructor() { }

    // add a new order (aka ask)
    function ask(bytes memory _customer_pubk, address _seller, bytes memory _offer_id, uint256 _total)
        public
    {
        require(DAI.transferFrom(msg.sender, address(this), _total));
        bytes32 ask_id = get_ask_id(_seller, _offer_id, msg.sender);
        require(asks[ask_id] == 0);
        asks[ask_id] = _total;
        emit Ask(_customer_pubk, msg.sender, _seller, _total);
    }

    // confirm the order, passing along the secret location
    function confirm(address _customer, bytes memory _offer_id, uint256 _total, bytes memory location)
        public
    {
        require(DAI.transfer(msg.sender, _total));
        bytes32 ask_id = get_ask_id(msg.sender, _offer_id, _customer);
        require(asks[ask_id] == _total);
        require(_total != 0);
        emit Confirm(ask_id, location);
        delete(asks[ask_id]);
    }

    function get_ask_id(address _seller, bytes memory _offer_id, address _customer)
        public
        pure
        returns (bytes32)
    {
        return keccak256(abi.encode(_seller, _offer_id, _customer));
    }
}