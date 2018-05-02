import React from 'react';
import ReactDOM from 'react-dom';
import { Spin } from 'antd';


import api from '../../api/root';
import UserItem from './userItem';

export const renderPermissions = () => {
  class App extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        users: [],
        filter: '',
        page: 0,
        loading: true,
        filters: {
          email: '',
        },
      };

      this.fetchUsers();
    }

    users() {
      return this.state.users;
    }

    changeFilterEmail(email) {
      const newStatePart = { filters: { email } };
      this.setState(prevState => Object.assign({}, prevState, newStatePart));
      setTimeout(() => {
        this.fetchUsers();
      }, 1000);
    }

    fetchUsers() {
      this.setState(prevState => Object.assign({}, prevState, { loading: true }));
      api.getUsers(15, this.state.page * 15, this.state.filters, (users) => {
        this.setState(prevState => Object.assign({}, prevState, { users: users.results || [], loading: false }));
      });
    }

    isEmpty() {
      return !this.state.users.length;
    }

    editUser(user) {
      console.log(user);
    }

    usersContent() {
      if (this.state.loading) {
        return (
          <div className="spinner">
            <Spin size="large" />
          </div>
        )
      }

      if (this.isEmpty()) {
        return (
          <div className="nothing">
            Ничего не найдено
          </div>
        )
      }

      return this.state.users.map((user) => {
        return (
          <UserItem user={user} />
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
