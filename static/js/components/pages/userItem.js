import React from 'react';
import ReactDOM from 'react-dom';

export default class UserItem extends React.Component {
  constructor(props) {
    super(props);
    this.state = { edit: false };
  }

  editUser() {
    this.setState(prevState => Object.assign({}, prevState, { edit: true }));
  }

  editPanel() {
    if (!this.state.edit) {
      return;
    }

    return (
      <div className="user-edit">
        EDIT
      </div>
    )
  }

  render() {
    const user = this.props.user;
    return (
      <div className="user-item">
        <img src={user.avatar} height="64" width="64" />
        <div className="user-description">
          <div className="name">{user.get_username}</div>
          <div className="email">{user.email}</div>
          <div className="actions">
            <a className="btn" onClick={() => this.editUser()}>Edit</a>
          </div>
          { this.editPanel() }
        </div>
      </div>
    )
  }
}
