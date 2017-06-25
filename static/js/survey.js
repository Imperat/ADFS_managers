import React from 'react';
import ReactDOM from 'react-dom';

export const renderSurvey = () => {
      var App = React.createClass({
    render: function() {
    return (
    <div className="app">
    Всем привет, я компонент App!
    </div>
    );
    }
    });
    ReactDOM.render(
    <App />,
    document.getElementById('root')
    );
};
