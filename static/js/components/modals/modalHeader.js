import React from 'react';
import ReactDOM from 'react-dom';

export class ModalHeader extends React.Component {
  constructor (props) {
    super(props);
  }

  render () {
    return (
      <div className="modal-header">
        <button type="button" className="close" data-dismiss="modal">&times;</button>
        <h4 className="modal-title">{this.props.title}</h4>
      </div>
    )
  }
}
