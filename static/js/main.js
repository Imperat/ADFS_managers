import 'bootstrap/dist/js/bootstrap';
import 'antd/dist/antd.css';

import { renderSurvey } from './survey';
import { renderStadionForm } from './components/pages/stadionReservation';
import { renderProfileForm } from './components/pages/profile';
import { renderCupDetail } from './components/pages/cupDetail';
import { renderLoginForm } from './login';
import store from './store';
import Alert from 'react-s-alert';
import configs from './config';
import toggleMenuTheme from './personalisation.js';

var $ = require('jquery');
window.jQuery = $;
window.$ = $;
window.store = store;
window.socket = new WebSocket("ws://193.124.188.199:8081");
window.moment = require('moment');

window.socket.onmessage = (event) => {
  Alert.info(event.data, configs.alertConfigs.defaultEffect);
};

$(document).ready(() => {
  //View and styles
  toggleMenuTheme(localStorage.getItem('light-theme'));

  //Routes
  const $loginForm = $('#login-form');
  if (window.location.pathname === '/survey') renderSurvey();
  if (window.location.pathname === '/logic/stadion/get/') renderStadionForm();
  if (window.location.pathname === '/login/') renderProfileForm();
  if (window.location.pathname.match('/logic/cup/[0-1]+/')) {
    const id = Number(window.location.pathname.split('/')[3]);
    renderCupDetail(id);
  }

  renderLoginForm();
});

function initApp() {
  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

  const csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
}

initApp();
