'use strict';
let map;

function initMap() {
  const location = {
    lat: 40.000,
    lng: -79.000
  }

  const options = {
    center: location,
    zoom: 20
  }
  if(navigator.geolocation) {
    console.log('geolocation is here!');

    //this will ask user for permission to get their position
    navigator.geolocation.getCurrentPosition((loc) => {
      //gets lat/lng...updates location object...if user says yes
      location.lat = loc.coords.latitude;
      location.lng = loc.coords.longitude;

      //write the map
      map = new google.maps.Map(document.getElementById("map"), options); 
      const userMarker = new google.maps.Marker({
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
  //Autocomplete takes two parameters...the element taking in the input 
  //and an object that contains the options we choose to for our input field..many available
  //three required: componentRestrcitions, fields(specific things about the place chosen). and type
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

}


