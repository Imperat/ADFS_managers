const $ = require('jquery');

import React from 'react';
import ReactDOM from 'react-dom';

window.jQuery = $;
window.$ = $;


$(document).ready(function(){
  start();
});

const MenuItem = React.createClass({
  render: function(title) {
    return (
      <li>
        <a href="#">{this.props.title}</a>
      </li>
    );
  },
})

const Menu = React.createClass({
  render: function() {
    return (
      <div className="container-fluid">
        <div className="row">
          <div className="col-md-12">
            <nav className="navbar navbar-default navbar-inverse" role="navigation">
              <div className="navbar-header">
                <button type="button" className="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                  <span className="sr-only">Toggle navigation</span><span className="icon-bar"></span>
                  <span className="icon-bar"></span><span className="icon-bar"></span>
                </button>
                <a className="navbar-brand" href="{% url 'index' %}"> АДФС </a>
              </div>
              <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul className="nav navbar-nav">
                  <li className="dropdown">
                    <a href="#" className="dropdown-toggle" data-toggle="dropdown">Высшая лига<strong className="caret"></strong></a>
                      <ul className="dropdown-menu">
                        <MenuItem title="Турнирное положение" />
                        <MenuItem title="Календарь" />
                        <MenuItem title="Бомбардиры" />
                        <li className="divider"></li>
                        <MenuItem title="Участники" />
                      </ul>
                    </li>
                  <li className="dropdown">
                    <a href="#" className="dropdown-toggle" data-toggle="dropdown">Первая лига<strong className="caret"></strong></a>
                                  <ul className="dropdown-menu">
                                    <MenuItem title="Турнирное положение" />
                                    <MenuItem title="Календарь" />
                                    <MenuItem title="Бомбардиры" />
                                    <li className="divider"></li>
                                    <MenuItem title="Участники" />
                                    <li className="divider"></li>
                                    <MenuItem title="Подать заявку" />
                                  </ul>
                              </li>
                              <li>
                                  <a href="#">Кубок</a>
                              </li>
                              <li className="dropdown">
                                  <a href="#" className="dropdown-toggle" data-toggle="dropdown">Зимний кубок<strong
                                          className="caret"></strong></a>
                                  <ul className="dropdown-menu">
                                      <li>
                                          <a href="#">Архив</a>
                                      </li>
                                      <li className="divider">
                                      </li>
                                      <li>
                                          <a href="#">Подать заявку</a>
                                      </li>
                                  </ul>
                              </li>
                              <li className="divider-vertical"></li>
                              <li>
                                  <a href="#">Новости</a>
                              </li>
                              <li className="dropdown">
                                  <a href="#" className="dropdown-toggle" data-toggle="dropdown">Помощь<strong
                                          className="caret"></strong></a>
                                  <ul className="dropdown-menu">
                                      <li>
                                          <a href="">Регламент соревнований</a>
                                      </li>
                                      <li className="divider">
                                      </li>
                                      <li>
                                          <a href="#">Матч-центр</a>
                                      </li>
                                      <li>
                                          <a href="#">Участники</a>
                                      </li>
                                  </ul>
                              </li>
                          </ul>
                          <form className="navbar-form navbar-left" role="search">
                              <div className="form-group">
                                  <input type="text" className="form-control" />
                              </div>
                              <button type="submit" className="btn btn-default">
                                  Поиск
                              </button>
                          </form>
                          <ul className="nav navbar-nav navbar-right">
                              <li>
                                  <a href="#">ВК</a>
                              </li>
                              <li className="dropdown">
                                  <a href="#" className="dropdown-toggle" data-toggle="dropdown">О проекте<strong
                                          className="caret"></strong></a>
                                  <ul className="dropdown-menu">
                                      <li>
                                          <a href="#">Разработчик</a>
                                      </li>
                                      <li>
                                          <a href="#">Помощь</a>
                                      </li>
                                      <li>
                                          <a href="#">Администратору</a>
                                      </li>
                                  </ul>
                              </li>
                          </ul>
                      </div>

                  </nav>
              </div>
          </div>
      </div>

    );
  }
});

function start() {
  ReactDOM.render(
  <Menu />,
  document.getElementById('menu'),
  );
};
