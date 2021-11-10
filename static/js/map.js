'use strict';
let map;
let userMarker;
function initMap() {
  const location = {
    lat: 40.000,
    lng: -79.000
  }

  const options = {
    center: location,
    zoom: 15
  }
  if(navigator.geolocation) {
    console.log('geolocation is here!');

    //this will ask user for permission to get their position
    navigator.geolocation.getCurrentPosition((loc) => {
      //gets lat/lng...updates location object...if user says yes
      location.lat = loc.coords.latitude;
      location.lng = loc.coords.longitude;

      // do ajax request with no event go to server route (middleman) to handle request to api
      //write the map
      ///callback will have the data, callback will do everything else....the  user marker, restroom markers
      $.get('/restrooms', location, resp => {
        
        for(let i = 0; i < resp['results'].length; i++){
        
          let restroomName = resp['results'][i]['name'];
          let restroomLocation = resp['results'][i]['geometry']['location'];
          let place_id = resp['results'][i]['place_id'];

          const restroomInfoContent = `
            <div class="window-content">
              <div class="restroom-thumbnail">
              
              </div>

              <ul class="restroom-info">
                <li><b>Name: </b>${restroomName}</li>
              </ul>
            </div>
          `;

          let restroomMarker = new google.maps.Marker({
              position: restroomLocation,
              title: `Restroom ${i}`,
              map: map,
              bathroom_id: place_id,
              name: restroomName
            });
            
            let restroomLocationInfo = new google.maps.InfoWindow({
              content: restroomInfoContent,
          });
    
          restroomMarker.addListener('click', () => {
            restroomLocationInfo.open(map, restroomMarker);
            console.log(restroomMarker.bathroom_id, restroomMarker.name);
            $('#review-menu').html(`
            <form action="/review_form" method="POST">
              <h2>${restroomMarker.name}</h2>
              <input type="hidden" id="bathroomID" name="bathroomID" value="${restroomMarker.bathroom_id}">
              <input type="hidden" id="bathroomName" name="bathroomName" value="${restroomMarker.name}">
              <button type="submit" value="Submit "id="leave-review" class="${restroomMarker.bathroom_id}"">Leave Review</button>
            </form>
            
            <form action="/all_user_reviews" method="POST">
              <input type="hidden" id="bathroomID" name="bathroomID" value="${restroomMarker.bathroom_id}">
              <input type="hidden" id="bathroomName" name="bathroomName" value="${restroomMarker.name}">
              <button type="submit" value="Submit "id="see-reviews" class="${restroomMarker.bathroom_id}">See Reviews</button>
            </form>
            `);
            
          });
        }
     
        
      })
    
     
      map = new google.maps.Map(document.getElementById("map"), options); 

      userMarker = new google.maps.Marker({
        position: location,
        title: 'You are Here!',
        map: map,
      });

      const userLocationInfo = new google.maps.InfoWindow({
        content: `<h1>You are here
        lat: ${location.lat}
        lng: ${location.lng}
        !</h1>`,
      });

      userMarker.addListener('click', () => {
        userLocationInfo.open(map, userMarker);
      });
    },
    //if they say no...handle/throw error
    (err) => {
      console.log('User denied permission.')
      //this will create basic map without user location
      map = new google.maps.Map(document.getElementById("map"), options);
    }
    )
  } 
  else {
    console.log('geolocation not supported');
    map = new google.maps.Map(document.getElementById("map"), options);
}
  //create new instance of autocomplete
  // Autocomplete takes two parameters...the element taking in the input 
  // and an object that contains the options we choose to for our input field..many available
  // three required: componentRestrcitions, fields(specific things about the place chosen). and type
   let autocomplete = new google.maps.places.Autocomplete(document.getElementById('input'), {
    componentRestrictions : {country: ['us']},
    //billed by how many fields you use...these two are free
    fields: ['geometry', 'name'],
    types: ['establishment']
  });

  //event listener
  //takes two arguments:
  //place_changed event happens when user selects from drop down
  //callback function:
  //this anon cb gets the place
  autocomplete.addListener("place_changed", () => {
    //becomes place object
    const place = autocomplete.getPlace();
    console.log(place.geometry)
    //adds marker
    //Marker takes an object as it's argument
    new google.maps.Marker({
      position: place.geometry.location,
      title: place.name,
      map: map

    })
  })


  $('#leave-review').on('click', () => {
    console.log('leave review has been clicked')
    const formInputs = {
      bathroom_id: $('#bathroomID').val(),
      bathroom_name: $('#bathroomName').val()
    }
    
    $.get('/review_form', formInputs, res => {
      console.log(res);
    });
  });

  

}

