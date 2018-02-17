import React from 'react';
import ReactDOM from 'react-dom';
import api from '../../api/root';
import { Spin } from 'antd';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { loading: true, matches: [], cupId: props.cupId };
    this.loadMatches();
  }

  loadMatches() {
    api.getCupMatches(this.state.cupId, (data) => {
      setTimeout(() => this.setState(prevState => Object.assign({}, prevState, { loading: false, matches: data })), 2000);
    });
  }

  render() {
    if (this.state.loading) {
      return (
        <div className="row">
          <div className="example">
            <Spin size="large" />
            <h4 style={{marginTop: '50px'}}> Загружаем матчи специально для вас!</h4>
          </div>
        </div>
      )
    }

    return (
      <div className="row">
        { this.state.matches.map((matchPair) => {
          return (
            <div className="row matchPairItem">
              <div className="MatchItem">
                <div className="TeamName">
                  {matchPair.first_match.home.name}
                </div>
                <div className="TeamName">
                  {matchPair.first_match.away.name}
                </div>
              </div>
            </div>
          )
        }) }
      </div>
    )
  }
}

export const renderCupDetail = (id) => {
  ReactDOM.render(
    <App cupId={id}/>,
    document.getElementById('current_cup'),
  );
};
