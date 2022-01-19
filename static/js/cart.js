let updateBtns = document.getElementsByClassName("update-cart");

for(let i=0; i<updateBtns.length; i++) {
    
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action

        console.log("Product: ",productId,", action: ",action);
        console.log('User: ',user)

        // user was declared on main.html
        // AnonymousUser defined by django when the user not authentified
        if(user === 'AnonymousUser'){
            addCookieItem(productId, action);
            location.reload()
        }
        else{
            updateUserOrder(productId, action);
        }
    });
}

function addCookieItem(ProductId, Action) {
    console.log('Not logged in ...')

    if(Action == 'add') {
        if(cart[ProductId] == undefined ) {
            cart[ProductId] = {'quantity': 1}
        }
        else{
            cart[ProductId]['quantity'] += 1   
        }
    }

    if(Action == 'remove') {
        cart[ProductId]['quantity'] -= 1   

        if ( cart[ProductId]['quantity'] <= 0) {
            console.log('Remve item')
            delete cart[ProductId]  
        }
    }

    console.log("cart :", cart)
    document.cookie = "cart=" + JSON.stringify(cart) +";domain=;path=/"

}

// update the order with a promise using fetch API
function updateUserOrder(ProductId, Action) {

    console.log("user logged in, Loading data ...")

    let url = '/update_item/' 
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'productId': ProductId,
            'action': Action
        })
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data: ', data)
        location.reload()
    })
    
}
