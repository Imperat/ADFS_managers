import React from 'react';
import ReactDOM from 'react-dom';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';
const FontAwesome = require('react-fontawesome');

export const renderStadionForm = () => {
  class App extends React.Component {

    constructor(props) {
      super(props);
    }

    render () {
      return (
        <div className="col-lg-10 black text-left survey-wrapper" id="root2">
          <h3>Занять время на стадионе</h3>
          <hr/>
        </div>
      )
    }
  };

  ReactDOM.render(
    <App />,
    document.getElementById('root2'),
  );
};
