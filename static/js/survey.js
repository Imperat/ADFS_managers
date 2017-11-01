import React from 'react';
import ReactDOM from 'react-dom';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';
const FontAwesome = require('react-fontawesome');

export const renderSurvey = () => {
  class App extends React.Component {

    constructor(props) {
    super(props);
    this.state = {
      firstName: '',
      teamName: '',
      leagueName: '',
      step: 1,
    };

    // This binding is necessary to make `this` work in the callback
    this.handleChangeFirstName = this.handleChangeFirstName.bind(this);
    this.handleChangeTeamName = this.handleChangeTeamName.bind(this);
    this.handleChangeLeagueName = this.handleChangeLeagueName.bind(this);
    this.nextStep = this.nextStep.bind(this);
    this.prevStep = this.prevStep.bind(this);
  }

    handleChangeFirstName (event) {
      event.persist();
      this.setState(prevState => ({ firstName: event.target.value }));
    }

    handleChangeTeamName(event) {
      event.persist();
      this.setState(prevState => Object.assign({}, prevState, { teamName: event.target.value }));
    }

    handleChangeLeagueName(event) {
      event.persist();
      this.setState(prevState => Object.assign({}, prevState, { leagueName: event.target.value }));
    }

    nextStep() {
      this.setState(prevState => Object.assign({}, prevState, { step: prevState.step + 1 }));
    }

    prevStep() {
      this.setState(prevState => Object.assign({}, prevState, { step: prevState.step - 1 }));
    }

    render () {
      const step = this.state.step;
      let form = null;
      if (step === 1) {
        form = (
          <div>
            <div className="form-group col-lg-12">
              <label htmlFor="name" className="col-lg-12">
                Представьтесь, пожалуйста
              </label>

              <div className="col-lg-12">
                <input type="text" onChange={this.handleChangeFirstName} value={this.state.firstName} id="name" placeholder="Джеймс Кук" className="form-control"/>
              </div>
            </div>

            <div className="form-group col-lg-12">
              <label htmlFor="team" className="col-lg-12">
                Название вашей команды
              </label>
              <div className="col-lg-12">
                <input type="text" id="team" onChange={this.handleChangeTeamName} value={this.state.teamName} placeholder="Джандолуп" className="form-control" />
              </div>
            </div>

            <div className="form-group col-lg-12">
              <label htmlFor="league" className="col-lg-12">
                Чемпионат
              </label>
              <div className="col-lg-12">
                <input type="text" id="league" onChange={this.handleChangeLeagueName} value={this.state.leagueName} placeholder="Зимний кубок АДФС" className="form-control" />
              </div>
            </div>
          </div>
        )
      } else if (step === 2) {
        form = (
          <div className="form-group col-lg-12">
            <label htmlFor="player" className="col-lg-12">
              Выберите игроков или создайте новых
            </label>
            <div className="col-lg-12">
              <input type="text" id="player" placeholder="Михаил Лелякин" className="form-control" />
            </div>
            <div className="col-lg-12 player-container">
              <div className="col-lg-12 player-container__inner">
                <div className="col-lg-4">
                  <img src="http://positum.org.ru/wp-content/uploads/2014/09/%D0%B0%D0%B2%D0%B0%D1%82%D0%B0%D1%80%D0%BA%D0%B0-%D0%BF%D1%83%D1%81%D1%82%D0%B0%D1%8F.jpg" width="80" height="80" />
                </div>
                <div className="col-lg-12">
                  <div className="col-lg-12">
                    Михаил Лелякин
                  </div>
                  <div className="col-lg-12">
                    1995 года рождения
                  </div>
                  <div className="col-lg-12">
                    Играл в командах: Оникс
                  </div>
                  <div className="col-lg-12">
                    <button type="button" className="btn btn-survey btn-primary"><FontAwesome name="plus" />Добавить игрока </button>
                    <button type="button" className="btn btn-survey btn-default"><FontAwesome name="minus" />Отменить и создать своего </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      } else if (step === 3) {
        form = (
        <div>
          <div className="form-group col-lg-12">
            <label htmlFor="captain" className="col-lg-12">
              Капитан команды
            </label>
            <div className="col-lg-12">
              <input type="text" id="captain" placeholder="Владимир Путин" className="form-control" />
            </div>
          </div>

          <div className="form-group col-lg-12">
            <label htmlFor="captain2" className="col-lg-12">
              Второй представитель команды
            </label>
            <div className="col-lg-12">
              <input type="text" id="captain2" placeholder="Ксения Собчак" className="form-control" />
            </div>
          </div>

          <div className="form-group col-lg-12">
            <label htmlFor="photo" className="col-lg-12">
              Командное фото
            </label>
            <div className="col-lg-12">
              <a href="#" id="teamPhoto">Выбрать...</a>
            </div>
          </div>
        </div>
        )
      }

      return (
        <div className="col-lg-10 black text-left survey-wrapper" id="root2">
          <h3>Регистрация заявки на участие в турнире</h3>
          <hr/>
          <div className="row survey">
            <div className="col-lg-4 form">
            { this.state.step !== 1 && <button onClick={this.prevStep} className="btn btn-default" style={{float: 'left'}}>
              <FontAwesome name='arrow-circle-left' /> Назад
              </button> }

            { this.state.step !== 3 && <button onClick={this.nextStep} className="btn btn-default" style={{float: 'right'}}>
              Вперёд <FontAwesome name='arrow-circle-right' />
              </button> }

            <ReactCSSTransitionGroup
              transitionName="example"
              transitionEnterTimeout={500}
              transitionLeaveTimeout={300}>
              {form}
            </ReactCSSTransitionGroup>
            </div>

            <div className="col-lg-6 col-lg-offset-1 preview">
              <h4>Заявка на регистрацию в турнире АДФС</h4>
              <ul>
                <li>Заявку подаёт: <span>{this.state.firstName}</span></li>
                <li>Название команды: <span>{this.state.teamName}</span></li>
                <li>Турнир: <span>{this.state.leagueName}</span></li>
                {this.state.step}
              </ul>
            </div>
          </div>
        </div>

      );
    }
  };

  ReactDOM.render(
    <App />,
    document.getElementById('root2'),
  );
};
