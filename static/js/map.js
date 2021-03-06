'use strict';

// declare necessary variables in the global scope
let map;
let userMarker;
let restroomLocation;
let userLatLng;
let restroomLatLng;
let restroomLat;
let restroomLng;
let average_rating;

// overall function that initializes map object
function initMap() {

  //define object to store a default user lat/lng, in case geo location permission not given. 
  const userLoc = {
    lat: 40.000,
    lng: -79.000
  }

  //options object stores where map should center and how far in to zoom
  const options = {
    center: userLoc,
    zoom: 14,
    styles: MAPSTYLES
  }

  // checks if geo location is supported
  if(navigator.geolocation) {

    //ask user for permission to get their position
    navigator.geolocation.getCurrentPosition((loc) => {
      //get lat/lng...updates location object...if user says yes
      userLoc.lat = loc.coords.latitude;
      userLoc.lng = loc.coords.longitude;

      // create user latlng instance for use in getting route
      userLatLng = new google.maps.LatLng(userLoc.lat, userLoc.lng);

      // ajax request with no event go to server route (middleman) to handle request to api
      //write the map
      ///callback will have the data, callback will do everything else....the  user marker, restroom markers
      $.get('/restrooms', userLoc, response => {
        // console.log(response["resp1"]["results"])
        // let resp = response["resp1"]
        // let hours = response["hours"]
        console.log(response)
        let resp = response;
      
        //iterate over response
        //store necessary information
        for(let i = 0; i < resp['results'].length; i++){
          let restroomAddress = resp['results'][i]['vicinity'];
          let restroomName = resp['results'][i]['name'];
          restroomLocation = resp['results'][i]['geometry']['location'];
          restroomLat = resp['results'][i]['geometry']['location']['lat'];
          restroomLng = resp['results'][i]['geometry']['location']['lng'];
          let place_id = resp['results'][i]['place_id'];
          let restroomInfoContent;
          let restroomHourArray;
          let restroomHours;
          
          // if(hours[i]["result"]["opening_hours"]){
          //   // console.log(typeof hours[i]["result"]["opening_hours"])
          //   // console.log(hours[i]["result"]["opening_hours"])
          //   for(const key in hours[i]["result"]["opening_hours"])
          //   // console.log(hours[i]["result"]["opening_hours"][key])
          //     if(key === "weekday_text"){
          //       // console.log(key)
          //       restroomHourArray = hours[i]["result"]["opening_hours"][key]
          //     }
              
          // } else {
          //   restroomHours = 'Hours of Operation Unavailable';
          // }
          // what will be displayed when info window for restroom marker is clicked
          // if(restroomHours) {
          //   restroomInfoContent = `
          //   <div class="window-content">
          //     <div class="restroom-thumbnail">
              
          //     </div>
          //     <div class="restroom-info">
          //       <h3>${restroomName}</h3>
          //       <div id="average-rating${i}">
          //     </div>
          //       <p><b>Address: </b>${restroomAddress}</p>
          //       <p><b>Hours: </b></p>
          //         <li>${restroomHours}</li>
          //     </div>
              
          //   </div>
          // `;
          // }
          // else {
          //   restroomInfoContent = `
          //   <div class="window-content">
          //     <div class="restroom-thumbnail">
          //     </div>
              
          //     <div class="restroom-info">
          //       <h3>${restroomName}</h3>
          //       <div id="average-rating${i}">
                
          //     </div>
          //       <p><b>Address: </b>${restroomAddress}</p>
          //       <p><b>Hours: </b></p>
          //         <li>${restroomHourArray[0]}</li>
          //         <li>${restroomHourArray[1]}</li>
          //         <li>${restroomHourArray[2]}</li>
          //         <li>${restroomHourArray[3]}</li>
          //         <li>${restroomHourArray[4]}</li>
          //         <li>${restroomHourArray[5]}</li>
          //         <li>${restroomHourArray[6]}</li>
          //     </div>
              
          //   </div>
          // `;
          // }
          restroomInfoContent = `
            <div class="window-content">
              <div class="restroom-thumbnail">
              </div>
              
              <div class="restroom-info">
                <h3>${restroomName}</h3>
                <div id="average-rating${i}">
                
                </div>
                <p><b>Address: </b>${restroomAddress}</p>
              
              </div>
              
            </div>
          `;

          // create new instance of google maps marker
          let restroomMarker = new google.maps.Marker({
              position: restroomLocation,
              title: `Restroom ${i}`,
              map: map,
              bathroom_id: place_id,
              name: restroomName,
              restroomLat: restroomLat,
              restroomLng: restroomLng,
              icon: {
                url: '/static/img/toilet_blue.png',
                scaledSize: new google.maps.Size(50, 50),
              }
            });
            
            // create new instance of info window
            let restroomLocationInfo = new google.maps.InfoWindow({
              content: restroomInfoContent,
          });
          
          // add event listener to handle marker click event
          restroomMarker.addListener('click', () => {
            console.log("in click handler")
            const restroom = {
              bathroom_id : place_id 
            }
            restroomLocationInfo.open(map, restroomMarker);
            
            $.get('/average_rating', restroom, response => {
              console.log("get average rate")
              average_rating = response;
              $(`#average-rating${i}`).html(`<p><b>Average Rating: </b>${average_rating}</p>`);
            })
            

            // Create latlng instance for chosen restoom for directions
            restroomLatLng = new google.maps.LatLng(restroomLat, restroomLng);
            
            $('#review-menu').html(`
              <form action="/review_form" method="POST">
                <h2 style="text-align: center;"><strong>${restroomMarker.name}</strong></h2>
                <input type="hidden" id="bathroomID" name="bathroomID" value="${restroomMarker.bathroom_id}">
                <input type="hidden" id="bathroomName" name="bathroomName" value="${restroomMarker.name}">
                <button class="w-100 btn btn-outline-info btn-lg px-4 me-sm-3 fw-bold" type="submit" value="Submit "id="leave-review" class="${restroomMarker.bathroom_id}"">Leave Review</button>
              </form>

              <form action="/all_restroom_reviews" method="POST">
                <input type="hidden" id="bathroomID" name="bathroomID" value="${restroomMarker.bathroom_id}">
                <input type="hidden" id="bathroomName" name="bathroomName" value="${restroomMarker.name}">
                <button class="w-100 btn btn-outline-info btn-lg px-4 me-sm-3 fw-bold"  type="submit" value="Submit "id="see-restroom-reviews" class="${restroomMarker.bathroom_id}">Restroom Reviews</button>
              </form>
    
              
            `);
            // get both "get directions" and "reset" buttons and enable them
            // make them visible
            // this happens here, because buttons are added to html so that 
            // they exist before the "get directions" click event and that event can be bound to them
            const btn = document.getElementById('get-directions');
            btn.disabled = false;
            const resetBtn = document.getElementById('reset');
            resetBtn.disabled = false;

            // handles click event to get directions
            $('#get-directions').on('click', (evt) => {
              // create instance of DirectionsService
              const directionsService = new google.maps.DirectionsService();

              // The DirectionsRenderer object is in charge of drawing directions
              // on maps
              const directionsRenderer = new google.maps.DirectionsRenderer();

              //tell directions renderer which map to render directions on
              directionsRenderer.setMap(map);
              //places panel for text directions in directions panel div
              directionsRenderer.setPanel(document.getElementById('directionsPanel'));

              // object to be passed in to get route, includes: starting and ending points
              // and what mode user will be travelling by
              const startToEnd = {
                origin: {
                  lat: userLoc.lat,
                  lng: userLoc.lng,
                },
                destination: {
                  lat: restroomMarker.restroomLat,
                  lng: restroomMarker.restroomLng,
                },
                travelMode: 'WALKING',
              };
              
              // call route method with startToEnd object and a callback
              directionsService.route(startToEnd, (response, status) => {
                if (status === 'OK') {
                  // places directions on map
                  directionsRenderer.setDirections(response);
                } else {
                  alert(`Directions request unsuccessful due to: ${status}`);
                }
              });
            
            });

          });
        }
        
      })
      
    
      // create new instance of Map object
      map = new google.maps.Map(document.getElementById("map"), options);
      
      // create marker with user's location
      userMarker = new google.maps.Marker({
        position: userLoc,
        title: 'You are Here!',
        icon: {
          url: '/static/img/purpleman.svg',
          scaledSize: new google.maps.Size(50, 50),
        },
        map: map,
      });

      // create instance of info window attached to user location/marker
      const userLocationInfo = new google.maps.InfoWindow({
        content: `<h1>You are here
        lat: ${userLoc.lat}
        lng: ${userLoc.lng}
        !</h1>`,
      });
      
      // event listener to open info windo when user marker clicked
      userMarker.addListener('click', () => {
        userLocationInfo.open(map, userMarker);
      });
    },

    //if user denies permission to geo locate...handle/throw error
    (err) => {
      console.log('User denied permission.')
      //this will create basic map without user location
      map = new google.maps.Map(document.getElementById("map"), options);
    }
    )
  } 

  // if geo location not supported by browser, use default location
  else {
    console.log('geolocation not supported');
    map = new google.maps.Map(document.getElementById("map"), options);
}


    // handles reset, essentially refreshes page after running directions
    $('#reset').on('click', evt =>{
      location.reload();
    })
  
}

