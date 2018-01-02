import 'bootstrap/dist/js/bootstrap';
import 'antd/dist/antd.css';

import { renderSurvey } from './survey';
import { renderStadionForm } from './components/pages/stadionReservation';
import { renderLoginForm } from './login';
import store from './store';
import Alert from 'react-s-alert';
import configs from './config';

var $ = require('jquery');
window.jQuery = $;
window.$ = $;
window.store = store;
window.socket = new WebSocket("ws://193.124.188.199:8081");
window.moment = require('moment');

window.socket.onmessage = (event) => {
  Alert.info(event.data, configs.alertConfigs.defaultEffect);
};

$(document).ready(function(){
  const $loginForm = $('#login-form');
  if (window.location.pathname === '/survey') renderSurvey();
  if (window.location.pathname === '/logic/stadion/get/') renderStadionForm();
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
