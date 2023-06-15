// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

contract VendingMachine {
    struct Product {
        uint productId;
        string name;
        uint balance;
        uint price;
        string description;
    }

    address public owner;
    mapping(address => mapping(uint => Product)) public productBalances;

    constructor() {
        owner = msg.sender;
        initializeProduct( 1, "headphones", 50, 0.02  ether, "Wireless headphones for immersive audio experience.");
        initializeProduct( 2, "microphone", 50, 0.025 ether, "Professional microphone for crystal-clear recordings.");
        initializeProduct( 3,   "keyboard", 40, 0.03  ether, "Ergonomic keyboard for enhanced typing experience.");
        initializeProduct( 4,   "polaroid", 25, 0.06  ether, "Instant camera capturing memories in a snap.");
        initializeProduct( 5,     "Switch", 10, 0.2   ether, "Versatile gaming console for endless entertainment.");
        initializeProduct( 6,        "PS5",  5, 0.3   ether, "Next-gen gaming powerhouse for immersive experiences.");
        initializeProduct( 7,    "earings", 45, 0.02  ether, "Elegant accessories for stylish adornment.");
        initializeProduct( 8,      "rings", 15, 0.1   ether, "Elegant symbol of eternal commitment.");
        initializeProduct( 9,      "watch", 10, 0.15  ether, "Timeless companion on your wrist.");
        initializeProduct(10,   "necklace",  5, 0.2   ether, "Timeless jewelry that complements any outfit.");
        initializeProduct(11,       "tote", 50, 0.015 ether, "Stylish carry-all for everyday essentials.");
        initializeProduct(12,   "backpack", 15, 0.02  ether, "Versatile backpack for on-the-go convenience.");
        initializeProduct(13,     "wallet", 25, 0.025 ether, "Sleek and compact wallet for your essentials.");
        initializeProduct(14,    "stachel",  5, 0.1   ether, "Stylish and practical stachel for all your daily needs.");
    }

    function initializeProduct(uint productId, string memory name, uint initialAmount, uint price, string memory description) private {
        Product memory product = Product(productId, name, initialAmount, price, description);
        productBalances[address(this)][productId] = product;
    }
    
    function checkStore(uint productId) public view returns (string memory, uint, uint, string memory) {
        Product memory store = productBalances[address(this)][productId];
        return (store.name, store.balance, store.price, store.description); // 回傳店內商品名稱、庫存量、價格及描述
    }

    function checkBuyer(address walletAddress, uint productId) public view returns (string memory, uint) {
        Product memory buyer = productBalances[walletAddress][productId];
        Product memory temp = productBalances[address(this)][productId];
        return (temp.name, buyer.balance); // 回傳買家商品名稱及數量
    }
    
    function restock(uint productId, uint amount) public {
        require(msg.sender == owner, "Only the owner can restock."); //僅限店家可以補貨
        productBalances[address(this)][productId].balance += amount;
    }

    function purchase(uint productId, uint amount) public payable {
        uint price = productBalances[address(this)][productId].price;
        require(msg.value >= amount * price, "Insufficient payment for the items"); //價格不足不予支付
        require(productBalances[address(this)][productId].balance >= amount, "Not enough items in stock to complete this purchase"); //庫存量不夠
        productBalances[address(this)][productId].balance -= amount;
        productBalances[msg.sender][productId].balance += amount;
    }
    /*
    function Inventory(uint productId) public view returns (uint) {
        return productBalances[address(this)][productId].balance; // 回傳店內商品庫存量
    }

    function Price(uint productId) public view returns (uint) {
        return productBalances[address(this)][productId].price; // 回傳店內商品價格
    }

    function Description(uint productId) public view returns (string memory) {
        return productBalances[address(this)][productId].description; // 回傳店內商品描述
    }

    function Name(uint productId) public view returns (string memory) {
        return productBalances[address(this)][productId].name; // 回傳店內商品名稱
    }
    */
}
