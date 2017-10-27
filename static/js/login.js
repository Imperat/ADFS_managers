import React from 'react';
import ReactDOM from 'react-dom';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';
import Alert from 'react-s-alert';
import 'react-s-alert/dist/s-alert-default.css';
import 'react-s-alert/dist/s-alert-css-effects/slide.css';
const FontAwesome = require('react-fontawesome');

export const renderLoginForm = () => {
  class App extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        loggedIn: document.getElementById('login-app').dataset.auth,
        username: document.getElementById('login-app').dataset.username,
      };

      this.handleLoginRequest = this.handleLoginRequest.bind(this);
      this.handleLogoutRequest = this.handleLogoutRequest.bind(this);
    }

    handleLoginRequest(event) {
      event.persist();
      const data = $('#login-form').serializeArray();
      if (!data[0].value || !data[1].value) {
        Alert.error('Логин либо пароль не могут быть пустыми!', { effect: 'scale' });
        return;
      }

      $.ajax({
        type: 'POST',
        url: '/login/',
        data: {
          login: data[0].value,
          password: data[1].value,
        },
        success: (data) => {
          data = JSON.parse(data);
          Alert.info(`Мы рады, что вы вернулись, ${data.login}.`, {  effect: 'scale' });
          this.setState(prevState => Object.assign({}, prevState, {
            loggedIn: true,
            username: data.login,
          }));
        },
        error: (data) => {
          if (data.status === 500) {
            Alert.error('Возникли небольшие трудности. Произошла ошибка сервера!', { effect: 'scale' });
          }

          if (data.status === 403) {
            Alert.error('Неверные логин, либо пароль!', { effect: 'scale' });
          }
        },
      });
    }

    handleLogoutRequest(event) {
      event.persist();
      $.get('/logout', () => {
        Alert.info('Удачи, играйте в футбол!', { effect: 'scale' });
        this.setState(prevState => Object.assign({}, prevState, {
          loggedIn: false,
          username: null,
        }));
      });
    }

    render () {
      let component = null;
      if (!this.state.loggedIn) {
        component = (
          <form className="form-horizontal" id="login-form" method="post">
            <div className="form-group">
              <label> Логин: </label>
              <input className="form-control" name="login" type="text" placeholder="Император" />
            </div>
            <div className="form-group">
              <label> Пароль: </label>
                <input className="form-control" name="password" type="password" placeholder="Космонавтика" />
            </div>
            <div className="form-group">
                <button type="button" className="btn btn-primary" onClick={this.handleLoginRequest}>Войти</button>
                <button id="register" className="btn btn-default" data-toggle="modal" data-target="#modalRegister">Регистрация</button>
            </div>
          </form>
        )
      } else {
        component = (
          <div>
          Вы авторизованы как <strong><a href="/login">{ this.state.username }</a></strong>
          <div className="col-sm-12">
            <button className="btn btn-default" style={{'marginTop': '20px'}} onClick={this.handleLogoutRequest}>
              Выйти
            </button>
          </div>
          </div>
        )
      }

      return component;
    }
  }

  ReactDOM.render(
    <div>
    <Alert stack={{limit: 3}} />
    <App />
    </div>,
    document.getElementById('login-app'),
  )
}
