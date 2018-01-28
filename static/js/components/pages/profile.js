import React from 'react';
import ReactDOM from 'react-dom';

import { InputItem } from '../controls/inputItem';
import { AwesomeCheckbox } from '../controls/awesomeCheckbox';

import toggleMenuTheme from '../../personalisation.js';

export const renderProfileForm = () => {
  class App extends React.Component {
    constructor(props) {
      super(props);
      this.state = {};
    }

    switchMenuTheme(val) {
      if (!val) {
        localStorage.removeItem('light-theme');
      } else {
        localStorage.setItem('light-theme', true);
      }

      toggleMenuTheme(val);
    }

    render() {
      return (
        <div>
          <h4>Настройки профиля</h4>
          <InputItem id="email" title="Электронная почта" type="email" />
          <h4>Настройки сайта</h4>
          <AwesomeCheckbox title="Светлое меню" checked={localStorage.getItem('light-theme')} onChange={this.switchMenuTheme}/>
        </div>
      )
    }
  }

  ReactDOM.render(
    <App />,
    document.getElementById('root2'),
  );
};
