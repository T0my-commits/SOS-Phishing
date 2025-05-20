function openNav() {
  document.getElementById('myNav').classList.toggle('menu_width'),
  document.querySelector('.custom_menu-btn').classList.toggle('menu_btn-style')
}
function myMap() {
  var e = {
    center: new google.maps.LatLng(40.712775, - 74.005973),
    zoom: 18
  };
  new google.maps.Map(document.getElementById('googleMap'), e)
}

