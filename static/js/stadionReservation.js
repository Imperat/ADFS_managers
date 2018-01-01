import React from 'react';
import ReactDOM from 'react-dom';
import { Select, LocaleProvider, Button, TimePicker, DatePicker } from 'antd';
import ruRu from 'antd/lib/locale-provider/ru_RU';
import api from './api/root';

const moment = require('moment');
const Option = Select.Option;

const format = 'HH:mm';

export const renderStadionForm = () => {
  class App extends React.Component {

    constructor(props) {
      super(props);

      const startDate = moment().startOf('week');
      const endDate = moment().endOf('week');

      const dates = {};
      for (let iterator = startDate.clone(); iterator.isSameOrBefore(endDate);) {
        dates[iterator.format('YYYY-MM-DD')] = [];
        iterator.add(1, 'day');
      }

      this.state = {
        stadions: [],
        currentStadion: null,
        startDate,
        endDate,
        dates,
        selectedDate: null,
        selectedTimeStart: '12:00',
        selectedTimeEnd: '13:00',
      };

      this.handleChangeStadion = this.handleChangeStadion.bind(this);
      this.handleChangeNewDate = this.handleChangeNewDate.bind(this);
      this.handleChangeTimeStart = this.handleChangeTimeStart.bind(this);
      this.handleChangeTimeEnd = this.handleChangeTimeEnd.bind(this);
      this.handleTakeTime = this.handleTakeTime.bind(this);
      this.handlePreviousWeek = this.handlePreviousWeek.bind(this);
      this.handleNextWeek = this.handleNextWeek.bind(this);
      this.fetchStadions();
    }

    handlePreviousWeek() {
      this.setState(prevState => Object.assign({}, this.state, {
        startDate: this.state.startDate.clone().subtract(1, 'week'),
        endDate: this.state.endDate.clone().subtract(1, 'week'),
      }));

      setTimeout(() => this.fillDates(), 0);
    }

    handleNextWeek() {
      this.setState(prevState => Object.assign({}, this.state, {
        startDate: this.state.startDate.clone().add(1, 'week'),
        endDate: this.state.endDate.clone().add(1, 'week'),
      }));

      setTimeout(() => this.fillDates(), 0);
    }

    fetchStadions() {
      api.getStadions((stadions) => {
        this.setState(prevState => Object.assign({}, this.state, { stadions }));
      });
    }

    handleChangeStadion(value) {
      api.getStadionTimes(value, (data) => {
        const dates = this.state.dates;
        Object.keys(dates).forEach(key => dates[key] = []);
        console.log('DATAAA:', data);
        data.forEach(item => dates[item.date] && dates[item.date].push(item));
        this.setState(prevState => Object.assign({}, this.state, { dates, currentStadion: value }))
      });
    }

    handleChangeNewDate(value, label) {
      this.setState(prevState => Object.assign({}, this.state, {
        startDate: moment(label, 'YYYY-MM-DD').startOf('week'),
        endDate: moment(label, 'YYYY-MM-DD').endOf('week'),
        selectedDate: label,
      }));

      setTimeout(() => this.fillDates(), 0);
    }

    handleChangeTimeStart(value, label) {
      this.setState(prevState => Object.assign({}, this.state, { selectedTimeStart: label }));
    }

    handleChangeTimeEnd(value, label) {
      this.setState(prevState => Object.assign({}, this.state, { selectedTimeEnd: label }));
    }

    handleTakeTime() {
      const selectedDate = this.state.selectedDate;
      const selectedTimeStart = this.state.selectedTimeStart;
      const selectedTimeEnd = this.state.selectedTimeEnd;
      api.createStadionTime(
        this.state.currentStadion,
        { selectedDate, selectedTimeStart, selectedTimeEnd },
        () => setTimeout(() => this.fillDates(), 0),
      );
    }

    stadionOptions() {
      return this.state.stadions.map((stadion) => {
        return <Option value={stadion.id}>{stadion.name}</Option>
      });
    }

    timeBoardHeaders() {
      return Object.keys(this.state.dates).map((date) => {
        return <div className="timeBoardHeaderItem">{date}</div>
      });
    }

    fillDates() {
      const dates = {};
      const startDate = this.state.startDate;
      const endDate = this.state.endDate;

      for (let iterator = startDate.clone(); iterator.isSameOrBefore(endDate); iterator.add(1, 'day')) {
        dates[iterator.format('YYYY-MM-DD')] = [];
      }

      this.setState(prevState => Object.assign({}, prevState, { dates }));
      setTimeout(() => this.handleChangeStadion(this.state.currentStadion), 0);
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
              {this.stadionOptions()}
            </Select>
            <span className="panelLabel">Неделя:
              <a href="#">{this.state.startDate.format('DD-MM-YYYY')}</a> -
              <a href="#">{this.state.endDate.format('DD-MM-YYYY')}</a>
              <Button onClick={this.handlePreviousWeek}> - </Button>
              <Button onClick={this.handleNextWeek}> + </Button>
            </span>
            <div className="take-time-panel" style={{ float: 'right' }}>
              Занять время:
              <DatePicker onChange={this.handleChangeNewDate} />
              <span>C:</span>
              <TimePicker onChange={this.handleChangeTimeStart} defaultValue={moment('12:10', 'HH:mm')} format={format} />
              <span>По:</span>
              <TimePicker onChange={this.handleChangeTimeEnd} defaultValue={moment('13:10', 'HH:mm')} format={format} />
              <Button onClick={this.handleTakeTime} >OK</Button>
            </div>
          </div>
          <div style={{display: 'flex', flexDirection: 'column'}}>
            <div className="timeBoardHeader">
              {this.timeBoardHeaders()}
            </div>
            <div className="timeBoardBody">
              { Object.keys(this.state.dates).map((i) => {
                return (
                  <div className="timeBoardBodyItem" style={{ width: '100%' }}>
                    {this.state.dates[i].map(function(j){
                      return <div className="timeBoardItem" style={{transform: `translateY(${j.time1 / 4}px)`, height: `${(j.time2 - j.time1)/4}px`}}>
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
