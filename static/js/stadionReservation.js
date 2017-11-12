import React from 'react';
import ReactDOM from 'react-dom';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';
import { Select } from 'antd';
import { LocaleProvider } from 'antd';
import ruRu from 'antd/lib/locale-provider/ru_RU';

const FontAwesome = require('react-fontawesome');
const moment = require('moment');
const Option = Select.Option;

export const renderStadionForm = () => {
  class App extends React.Component {

    constructor(props) {
      super(props);

      const startDate = moment().startOf('week');
      const endDate = moment().endOf('week');
      const iterator = startDate.clone();
      const dates = {};
      for (let i = startDate.date() + 1; i <= endDate.date(); i+= 1) {
        dates[iterator.format('YYYY-MM-DD')] = [];
        iterator.add(1, 'day');
      }

      this.state = {
        stadions: [],
        currentStadion: null,
        startDate,
        endDate,
        dates,
      };

      this.handleChangeStadion = this.handleChangeStadion.bind(this);

      this.fetchUsers();
    }

    fetchUsers() {
      $.get('/logic/api/v1/stadion', (error, result) => {
        if (result === 'success') {
          this.setState(prevState => Object.assign({}, this.state, { stadions: error }));
        }
      });
    }

    handleChangeStadion(value, label) {
      console.log(this);
      $.get('/logic/api/v1/stadion/' + value + '/times', (error, result) => {
        if (result === 'success') {
          const dates = this.state.dates;
          Object.keys(dates).forEach(key => dates[key] = []);
          console.log('datess', dates);
          console.log('server result', error);
          error.forEach(item => dates[item.date] && dates[item.date].push(item));
          this.setState(prevState => Object.assign({}, this.state, { dates }))
        }
      });
    }

    render () {
      return (
        <LocaleProvider locale={ruRu}>
        <div className="col-lg-12 black text-left survey-wrapper" id="root2">
          <h3>Занять время на стадионе</h3>
          <hr/>
          <div className="row">
            <span className="panelLabel">Стадион:</span>
            <Select
              showSearch
              style={{ width: 200 }}
              placeholder="Выберите площадку"
              onChange={this.handleChangeStadion}
              optionFilterProp="children"
              filterOption={(input, option) => option.props.children.toLowerCase().indexOf(input.toLowerCase()) >= 0}
            >
            {this.state.stadions.map(function (i) {
              return <Option value={i.id}>{i.name}</Option>
            })}
            </Select>
            <span className="panelLabel">Неделя: <a href="#">{this.state.startDate.format('MM-DD-YYYY')}</a> -
                          <a href="#">{this.state.endDate.format('MM-DD-YYYY')}</a>
            </span>
          </div>
          <div className="col-lg-12">
            <div className="row timeBoardHeader">
              { Object.keys(this.state.dates).map(function(i){
                return <div className="col-lg-2 timeBoardHeaderItem">{i}</div>
              }) }
            </div>
            <div className="row timeBoardBody">
              { Object.keys(this.state.dates).map((i) => {
                return (
                  <div className="col-lg-2 timeBoardBodyItem">
                    {this.state.dates[i].map(function(j){
                      return <div className="timeBoardItem" style={{transform: `translateY(${j.time1 / 4}px)`, position: 'absolute', height: `${(j.time2 - j.time1)/4}px`}}>
                      {moment(i,'YYYY-MM-DD').add(j.time1, 'minute').format('hh:mm')} - {moment(i,'YYYY-MM-DD').add(j.time2, 'minute').format('hh:mm')}</div>
                    }) }
                  </div>)
              }) }
            </div>
          </div>
        </div>
        </LocaleProvider>
      )
    }
  };

  ReactDOM.render(
    <App />,
    document.getElementById('root2'),
  );
};
