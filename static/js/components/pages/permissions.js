import React from 'react';
import ReactDOM from 'react-dom';
import { Spin } from 'antd';


import api from '../../api/root';

export const renderPermissions = () => {
  class App extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        users: [],
        filter: '',
        page: 0,
        filters: {
          email: '',
        },
      };

      this.fetchUsers();
    }

    users() {
      return this.state.users;
    }

    changeFilterEmail(event) {
      this.setState((prevState) => Object.assign({}, prevState, { filters: { email: event.target.value } }));
      setTimeout(() => {
        this.fetchUsers();
      }, 1000);
    }

    fetchUsers() {
      api.getUsers(15, this.state.page * 15, this.state.filters, (users) => {
        this.setState((prevState) => Object.assign({}, prevState, { users: users.results }));
      });
    }

    isEmpty() {
      return !this.state.users.length;
    }

    editUser(user) {
      console.log(user);
    }

    usersContent() {
      if (this.isEmpty()) {
        return (
          <div className="spinner">
            <Spin size="large" />
          </div>
        )
      }

      return this.state.users.map((user) => {
        return (
          <div className="user-item">
            <img src={user.avatar} height="64" width="64" />
            <div className="user-description">
              <div className="name">{user.get_username}</div>
              <div className="email">{user.email}</div>
              <div className="actions">
                <a className="btn" onClick={() => this.editUser(user)} >Edit</a>
              </div>
            </div>
          </div>
        )
      });
    }

    render () {
      return (
        <div className="permissions">
          <div className="permissions-panel">
            <input className="form-control" placeholder="Поиск по имени" onChange={event => this.changeFilterEmail(event.target.value)}/>
          </div>
          <div className="permissions-users">
            {this.usersContent()}
          </div>
        </div>
      )
    }
  }

  ReactDOM.render(
    <App />,
    document.getElementById('root2'),
  );
};
