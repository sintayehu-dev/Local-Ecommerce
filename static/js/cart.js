var updatebtns=document.getElementsByClassName('update-cart')

for(i=0;i<updatebtns.length;i++){
    updatebtns[i].addEventListener('click', function(){
      var productId=this.dataset.product
      var action =this.dataset.action
      console.log('productId:', productId , 'Action:', action)
      console.log('USER:', user)

      if(user =='AnonymousUser'){
         addCookieItem(productId, action)
      }
      else{
        updateUserOrder(productId, action)
      }
    })
}

function addCookieItem(productId, action){
   
   if (action=='add'){
      if (cart[productId]== undefined){
         cart[productId]={'quantity':1}
      }else{
         cart[productId]['quantity'] += 1
      }
   }
   if (action=='remove'){
      cart[productId]['quantity'] -= 1
      if(cart[productId]['quantity'] <= 0){
         console.log('removed item')
          delete cart[productId]
      }

   }
   console.log('cart:', cart)
   document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
   location.reload()
   
}


function updateUserOrder(productId, action){
    console.log('user is authenticated , seading data...')
     var url='/updateItem/'
     fetch(url, {
        method:'POST',
        headers:{
            'X-CSRFToken':csrftoken,
            'content-Type':'application/json',},
         body:JSON.stringify({
            'productId':productId , 
            'action' : action})
     })
     .then((response)=> {
        return response.json();
     })
     .then((data)=>{
        console.log('data:', data)
        location.reload()
     })
}