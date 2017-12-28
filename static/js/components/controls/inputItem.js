import React from 'react';
import ReactDOM from 'react-dom';

export class InputItem extends React.Component {
  constructor (props) {
    super(props);
  }

  render () {
    return (
      <div className="form-group col-sm-12">
        <label htmlFor={this.props.id}>{this.props.title}</label>
        <input className="form-control" type={this.props.type} name={this.props.id} id={this.props.id} />
      </div>
    )
  }
}
