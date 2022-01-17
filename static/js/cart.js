let updateBtns = document.getElementsByClassName("update-cart");

for(let i=0; i<updateBtns.length; i++) {
    
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action

        console.log("Product: ",productId,", action: ",action);
        console.log('User: ',user)

        // USER WAS DECLARED IN MAIN.HTML SCRIPT
        // AnonymousUser defined by django whenthe user not authentified
        if(user === 'AnonymousUser'){
            console.log("Not logged in ...")
        }
        else{
            updateUserOrder(productId, action);
        }
    });
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
