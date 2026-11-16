
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mini E-Commerce Store</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Arial;background:#f3f5f9;color:#182338}
header{background:#101d35;color:white;padding:20px 6%;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}
.logo{font-size:24px;font-weight:bold;color:#ff9d35}
button{border:0;padding:11px 16px;border-radius:8px;cursor:pointer;font-weight:bold}
.primary{background:#ff922e;color:#fff}
.dark{background:#172943;color:white}
nav{display:flex;gap:10px;flex-wrap:wrap}
.hero{background:linear-gradient(120deg,#142b50,#2765a0);color:white;padding:55px 7%}
.hero h1{font-size:36px;margin:0 0 12px}
.container{padding:30px 6%}
.toolbar{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:20px}
input{padding:12px;border:1px solid #d5dce7;border-radius:8px;width:100%;margin:7px 0}
#search{max-width:350px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:20px}
.card{background:white;border-radius:14px;padding:18px;box-shadow:0 4px 16px #18233812}
.product-icon{height:130px;background:#edf3fa;border-radius:10px;display:grid;place-items:center;font-size:65px}
.price{color:#e87920;font-size:22px;font-weight:bold}
.small{color:#69768b;font-size:13px}
.panel{background:white;padding:22px;border-radius:14px;margin:20px 0}
.hidden{display:none!important}
.row{display:flex;justify-content:space-between;align-items:center;gap:10px}
footer{text-align:center;padding:25px;background:#101d35;color:white}
</style>
</head>
<body>

<header>
<div class="logo">MINI STORE.</div>
<nav>
<button class="dark" onclick="showPage('shop')">Shop</button>
<button class="dark" onclick="showPage('cart')">Cart (<span id="count">0</span>)</button>
<button class="primary" onclick="showPage('admin')">Admin</button>
</nav>
</header>

<section class="hero">
<h1>Welcome to Mini Store</h1>
<p>Discover products. Shop smarter. Enjoy a simple shopping experience.</p>
<button class="primary" onclick="showPage('shop')">Explore Products →</button>
</section>

<main class="container">

<section id="shop">
<div class="toolbar">
<h2>Our Products</h2>
<input id="search" placeholder="Search products..." oninput="renderProducts()">
</div>
<div class="grid" id="products"></div>
</section>

<section id="cart" class="hidden">
<h2>Shopping Cart</h2>
<div class="panel" id="cartItems"></div>
</section>

<section id="admin" class="hidden">
<h2>Admin Dashboard</h2>
<div class="panel">
<h3>Add New Product</h3>
<input id="pname" placeholder="Product name">
<input id="pprice" type="number" placeholder="Price">
<input id="pstock" type="number" placeholder="Stock quantity">
<button class="primary" onclick="addProduct()">Add Product</button>
</div>
<div class="panel">
<h3>Manage Products</h3>
<div id="adminProducts"></div>
</div>
</section>

</main>

<footer>Mini E-Commerce System | Python 3 Project Frontend Demo</footer>

<script>
let products=[
{id:"P101",name:"Laptop",price:50000,stock:5,icon:"💻"},
{id:"P102",name:"Smartphone",price:15000,stock:8,icon:"📱"},
{id:"P103",name:"Headphones",price:1200,stock:10,icon:"🎧"},
{id:"P104",name:"Keyboard",price:800,stock:6,icon:"⌨️"}
];

let cart={};

function save(){
localStorage.setItem("miniProducts",JSON.stringify(products));
localStorage.setItem("miniCart",JSON.stringify(cart));
}

function load(){
try{
const p=JSON.parse(localStorage.getItem("miniProducts"));
const c=JSON.parse(localStorage.getItem("miniCart"));
if(Array.isArray(p))products=p;
if(c && typeof c==="object")cart=c;
}catch(e){}
}

function showPage(page){
["shop","cart","admin"].forEach(id=>{
document.getElementById(id).classList.toggle("hidden",id!==page);
});
if(page==="cart")renderCart();
if(page==="admin")renderAdmin();
}

function renderProducts(){
let q=document.getElementById("search").value.toLowerCase();
document.getElementById("products").innerHTML=products
.filter(p=>p.name.toLowerCase().includes(q))
.map(p=>`
<div class="card">
<div class="product-icon">${p.icon}</div>
<h3>${escapeHTML(p.name)}</h3>
<div class="small">Product ID: ${escapeHTML(p.id)}</div>
<p class="price">₹${p.price.toLocaleString("en-IN")}</p>
<p>${p.stock>0?"Stock: "+p.stock:"Out of Stock"}</p>
<button class="primary" ${p.stock===0?"disabled":""} onclick="addCart('${p.id}')">Add to Cart</button>
</div>`).join("");
}

function escapeHTML(value){
return String(value).replace(/[&<>"']/g,c=>({
"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
}[c]));
}

function addCart(id){
let p=products.find(x=>x.id===id);
if(!p||p.stock<=0)return alert("Out of stock!");
if((cart[id]||0)>=p.stock)return alert("Not enough stock!");
cart[id]=(cart[id]||0)+1;
save();updateCount();
alert("Product added to cart!");
}

function updateCount(){
document.getElementById("count").textContent=
Object.values(cart).reduce((a,b)=>a+b,0);
}

function renderCart(){
let total=0;
let html="";
Object.keys(cart).forEach(id=>{
let p=products.find(x=>x.id===id);
if(!p)return;
let amount=p.price*cart[id];total+=amount;
html+=`<div class="row">
<div><b>${escapeHTML(p.name)}</b><p>Quantity: ${cart[id]} | ₹${amount.toLocaleString("en-IN")}</p></div>
<button onclick="removeCart('${id}')">Remove</button>
</div><hr>`;
});
document.getElementById("cartItems").innerHTML=html+
`<h3>Total: ₹${total.toLocaleString("en-IN")}</h3>
<button class="primary" onclick="checkout()">Checkout</button>`;
if(!html)document.getElementById("cartItems").innerHTML="Your cart is empty.";
}

function removeCart(id){
delete cart[id];save();updateCount();renderCart();
}

function checkout(){
if(!Object.keys(cart).length)return alert("Cart is empty!");
for(let id in cart){
let p=products.find(x=>x.id===id);
if(!p||cart[id]>p.stock)return alert("Insufficient stock!");
}
let total=0;
for(let id in cart){
let p=products.find(x=>x.id===id);
total+=p.price*cart[id];
p.stock-=cart[id];
}
cart={};save();updateCount();renderProducts();renderCart();
alert("Order successful! Total: ₹"+total);
}

function addProduct(){
let name=document.getElementById("pname").value.trim();
let price=Number(document.getElementById("pprice").value);
let stock=Number(document.getElementById("pstock").value);
if(!name||!Number.isFinite(price)||price<=0||
!Number.isInteger(stock)||stock<0){
return alert("Enter valid product details!");
}
let number=101;
while(products.some(p=>p.id==="P"+number))number++;
products.push({id:"P"+number,name,price,stock,icon:"📦"});
save();renderProducts();renderAdmin();
alert("Product added successfully!");
document.getElementById("pname").value="";
document.getElementById("pprice").value="";
document.getElementById("pstock").value="";
}

function renderAdmin(){
document.getElementById("adminProducts").innerHTML=products.map(p=>`
<div class="row">
<div><b>${escapeHTML(p.name)}</b><br><small>${p.id} | ₹${p.price} | Stock ${p.stock}</small></div>
<div>
<button onclick="editProduct('${p.id}')">Edit</button>
<button onclick="deleteProduct('${p.id}')">Delete</button>
</div></div><hr>`).join("");
}

function editProduct(id){
let p=products.find(x=>x.id===id);
let name=prompt("New product name:",p.name);
if(name===null)return;
let price=Number(prompt("New price:",p.price));
let stock=Number(prompt("New stock:",p.stock));
if(!name.trim()||!Number.isFinite(price)||price<=0||
!Number.isInteger(stock)||stock<0)return alert("Invalid details!");
p.name=name.trim();p.price=price;p.stock=stock;
save();renderAdmin();renderProducts();
}

function deleteProduct(id){
if(!confirm("Delete this product?"))return;
products=products.filter(p=>p.id!==id);
delete cart[id];
save();updateCount();renderAdmin();renderProducts();
}

load();renderProducts();renderAdmin();updateCount();
</script>
</body>
</html>

