import React from 'react';
import ReactDOM from 'react-dom';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';
import { Select } from 'antd';
import { LocaleProvider } from 'antd';
import ruRu from 'antd/lib/locale-provider/ru_RU';

const FontAwesome = require('react-fontawesome');

const Option = Select.Option;

export const renderStadionForm = () => {
  class App extends React.Component {

    constructor(props) {
      super(props);
      this.state = {
        stadions: [],
      };

      this.fetchUsers();
    }

    fetchUsers() {
      $.get('/logic/api/v1/stadion', (error, result) => {
        if (result === 'success') {
          this.setState(prevState => Object.assign({}, this.state, { stadions: error }));
        }
      });
    }

    render () {
      return (
        <LocaleProvider locale={ruRu}>
        <div className="col-lg-10 black text-left survey-wrapper" id="root2">
          <h3>Занять время на стадионе</h3>
          <hr/>
          <div className="row">
            <span>Стадион:</span>
            <Select
              showSearch
              style={{ width: 200 }}
              placeholder="Выберите площадку"
              optionFilterProp="children"
              filterOption={(input, option) => option.props.children.toLowerCase().indexOf(input.toLowerCase()) >= 0}
            >
            {this.state.stadions.map(function (i) {
              return <Option value={i.id}>{i.name}</Option>
            })}
            </Select>
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
