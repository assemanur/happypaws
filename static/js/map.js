'use strict';

const zipcode = document.querySelector('#zipcode').dataset.zipcode;

// Initializing map on animal_details page
function initMap() {

  fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${zipcode}&key=${googleGeoKey}`)
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    data.results[0].geometry.location;
    const animalCoords = {
        lat: data.results[0].geometry.location.lat,
        lng: data.results[0].geometry.location.lng,
      };

  const basicMap = new google.maps.Map(document.querySelector('#map'),{
    center: animalCoords,
    zoom: 12,
  });

  const animalMarker = new google.maps.Marker({
    position: animalCoords,
    title: 'animal',
    map: basicMap,
  });

  animalMarker.addListener('click', () => {
    alert('Hi!');
  });

  const animalInfo = new google.maps.InfoWindow({
    content: '<p>I am waiting for you!</p>',
  });

  animalInfo.open(basicMap, animalMarker);
});
}

// Initializing Map on organization_details page
function initOrgMap() {

  fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${zipcode}&key=${googleGeoKey}`)
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    data.results[0].geometry.location;
    const organizationCoords = {
        lat: data.results[0].geometry.location.lat,
        lng: data.results[0].geometry.location.lng,
      };

  const basicMap = new google.maps.Map(document.querySelector('#map'),{
    center: organizationCoords,
    zoom: 12,
  });
  
  const organizationMarker = new google.maps.Marker({
    position: organizationCoords,
    title: 'organization',
    map: basicMap,
  });

  organizationMarker.addListener('click', () => {
    alert('Hi!');
  });

  const organizationInfo = new google.maps.InfoWindow({
    content: '<p>We have the cutest animals.</p>',
  });

  organizationInfo.open(basicMap, organizationMarker);
});
}