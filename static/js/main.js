import 'bootstrap/dist/js/bootstrap';
import 'antd/dist/antd.css';

import { renderSurvey } from './survey';
import { renderStadionForm } from './components/pages/stadionReservation';
import { renderProfileForm } from './components/pages/profile';
import { renderPermissions } from './components/pages/permissions';
import { renderLoginForm } from './login';
import store from './store';
import Alert from 'react-s-alert';
import configs from './config';
import toggleMenuTheme from './personalisation.js';
const page = require('page');

var $ = require('jquery');
window.jQuery = $;
window.$ = $;
window.store = store;
window.socket = new WebSocket("ws://193.124.188.199:8081");
window.moment = require('moment');

window.socket.onmessage = (event) => {
  Alert.info(event.data, configs.alertConfigs.defaultEffect);
};

const urlHandler = (ctx) => {
  const loader = document.querySelector('.loader-line');
  const minAnimationLength = 2000;
  const startAnimationFrame = (new Date()).valueOf();
  loader.style.width = '0%';
  loader.style.display = 'inline';
  setTimeout(() => (loader.style.width = '100%'), 10);
  $.get(ctx.canonicalPath, (data) => {
    const endAnimationFrame = (new Date()).valueOf();
    $('#root2').html(data);
    document.querySelector('body').scrollTop = 0;
    setTimeout(() => (loader.style.display = 'none'), Math.max(2000 - (endAnimationFrame - startAnimationFrame), 0));
  });
};

$(document).ready(() => {
  page.start({ click: true });
  page('/logic/stadion/get', renderStadionForm);
  page('/survey', renderSurvey);
  page('/login', renderProfileForm);
  page('/permissions', renderPermissions);
  page('/logic/team/:id', urlHandler);
  page('/logic/team', urlHandler);
  page('/logic', urlHandler);

  //View and styles
  toggleMenuTheme(localStorage.getItem('light-theme'));

  //Routes
  const $loginForm = $('#login-form');

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
