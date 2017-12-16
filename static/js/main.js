import 'bootstrap/dist/js/bootstrap';

import { renderSurvey } from './survey';
import { renderLoginForm } from './login';
import store from './store';
import Alert from 'react-s-alert';
import configs from './config';

var $ = require('jquery');
window.jQuery = $;
window.$ = $;
window.store = store;
window.socket = new WebSocket("ws://193.124.188.199:8081");

window.socket.onmessage = (event) => {
  Alert.info(event.data, configs.alertConfigs.defaultEffect);
};

$(document).ready(function(){
  const $loginForm = $('#login-form');
  if (window.location.pathname === '/survey') renderSurvey();
  renderLoginForm();

  $('#logOut').on('click', () => {
    const token = $('#logOut').closest('input').val();
    console.log(token);
    $.get( "/logout", () => {
      if (window.location.pathname !== '/login/') {
        location.reload();
      } else {
        window.location = '/logic/';
      }
    });
  });
});

function removeErrors(event){
  $(event.target).parent().removeClass('has-error');
}

function login(event){
  event.preventDefault();
  var $loginForm = $(event.target).first();
  var $login = $loginForm.find('input[name="login"]');
  var $passw = $loginForm.find('input[name="password"]');

  var login = $login.val();
  var passw = $passw.val();

  var valid = true;

  if (login.length == 0){
    $login.parent().addClass('has-error');
    valid = false;
  }

  if (passw.length == 0){
    $passw.parent().addClass('has-error');
    valid = false;
  }

  if (valid == false){
    return;
  }

  // Need implement promise that check login on server-side and
  // return true if login sucess, or false in user send invalid
  // credentials.
  loginRequest(login, passw);
}

function loginRequest(login, password){

};
