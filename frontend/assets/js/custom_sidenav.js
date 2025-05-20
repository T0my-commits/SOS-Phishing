/**
 * Function that toggle the sidenav.
 */
export function toggleNav() {
  const isNavVisible = document.getElementById("mySidenav").offsetWidth > 0;
  if (isNavVisible) {
    closeNav();
  } else {
    openNav();
  };
}

/**
 * Function that close the sidenav.
 */
export function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("myHeader").style.paddingLeft = "0";
  document.getElementById("main").style.marginLeft = "0";
}

/**
 * Function that open the sidenav.
 */
export function openNav() {
  document.getElementById("mySidenav").style.width = 260px;
  document.getElementById("myHeader").style.paddingLeft = 260px;
  document.getElementById("main").style.marginLeft = 260px;
}

