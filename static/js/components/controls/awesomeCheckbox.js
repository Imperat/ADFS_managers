import React from 'react';

export class AwesomeCheckbox extends React.Component {
  constructor (props) {
    super(props);

    this.state = {
      checked: props.checked,
      onChange: props.onChange,
    }
  }

  switchState() {
    if (this.state.onChange) {
      this.state.onChange(!this.state.checked);
    }

    this.setState(prevState => Object.assign({}, prevState, { checked: !prevState.checked }));
  }

  render () {
    return (
      <div className="form-group col-sm-12 awesome-checkbox">
        <label className="container-checkbox">{this.props.title}
          <input type="checkbox" defaultChecked={this.state.checked} onChange={() => this.switchState()}/>
          <span className="checkmark"></span>
        </label>
      </div>
    )
  }
}
