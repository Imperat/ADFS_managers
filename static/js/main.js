import 'bootstrap/dist/js/bootstrap';
import 'antd/dist/antd.css';

import { renderSurvey } from './survey';
import { renderStadionForm } from './stadionReservation';
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
  if (window.location.pathname === '/logic/stadion/get/') renderStadionForm();
  renderLoginForm();
});
