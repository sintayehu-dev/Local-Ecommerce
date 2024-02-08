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
   console.log('user not loggin...');
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