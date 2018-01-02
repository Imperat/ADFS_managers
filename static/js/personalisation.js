const toggleMenuTheme = (val) => {
  if (val) {
    $('nav.navbar').removeClass('navbar-inverse');
    $('nav.navbar').addClass('navbar-default');
  } else {
    $('nav.navbar').removeClass('navbar-default');
    $('nav.navbar').addClass('navbar-inverse');
  }
}

export default toggleMenuTheme;
