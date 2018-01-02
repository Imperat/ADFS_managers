import React from 'react';
import ReactDOM from 'react-dom';

import { ModalHeader } from './modals/modalHeader';
import { InputItem } from './controls/inputItem';
import Alert from 'react-s-alert';

import configs from '../config';
const alertDefault = configs.alertConfigs.defaultEffect;

export class RegisterForm extends React.Component {
  constructor (props) {
    super(props);

    this.handleRegister = this.handleRegister.bind(this);
    this.handleAvatarLoading = this.handleAvatarLoading.bind(this);
    this.handleAvatarDrop = this.handleAvatarDrop.bind(this);
    this.uploadAvatar = this.uploadAvatar.bind(this);
    this.switchToWebCam = this.switchToWebCam.bind(this);
    this.takeAnImage = this.takeAnImage.bind(this);

    this.state = {
      avatarUrl: null,
    };
  }

  uploadAvatar(event) {
    event.persist();
    const input = event.target;

    const reader = new FileReader();
    reader.onload = () => {
      const dataURL = reader.result;
      this.state.avatarUrl = dataURL
      this.setState(prevState => Object.assign({}, prevState, { avatarUrl: dataURL }));
    };

    reader.readAsDataURL(input.files[0]);
  }

  takeAnImage(event) {
    event.persist();
    const getImage = function() {
        const canvas = document.createElement("canvas");
        const video = $("video").get(0);
        canvas.getContext('2d')
            .drawImage(video, 0, 0, canvas.width, canvas.height);
        return canvas.toDataURL();
    }
        this.setState(prevState => Object.assign({}, prevState, { avatarUrl: getImage(), webcam: false }));
  }

  switchToWebCam(event) {
    event.persist();
    const vendorUrl = window.URL || window.webkitURL;
    navigator.getMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
    navigator.getMedia({
     audio: false,
     video: { width: 1280, height: 720 },
   }, (stream) => {
     this.setState(prevState => Object.assign({}, prevState, {
       webcam: true,
       videostream: vendorUrl.createObjectURL(stream),
      }));
    }, (error) => {
      Alert.error('Что-то пошло не так!', alertDefault);
      console.error(error);
    });
  }

  handleAvatarDrop(event) {
    event.persist();
    this.setState(prevState => Object.assign({}, prevState, { avatarUrl: null }));
  }

  handleAvatarLoading(event) {
    event.persist();
    $('#avatarupl').val('');
    $('#avatarupl').trigger('click');
  }

  handleRegister(event) {
    event.persist();
    const data = $('#register-form').serializeArray();
    console.log('data:', data);
    const login = data[0].value;
    const [password1, password2] = [data[1].value, data[2].value];
    const email = data[3].value;
    if (password1 !== password2) {
      Alert.error('Введённые пароли не совпадают!', alertDefault);
      return;
    }

    if (!login || !password1 || !password2 || !email) {
      Alert.error('Вы заполнили не все поля!', alertDefault);
      return;
    }

    $.ajax({
      type: 'POST',
      url: '/register/',
      data: {
        login,
        password: password1,
        email,
        avatar: this.state.avatarUrl && this.state.avatarUrl.replace(/^data:image\/(png|jpg);base64,/, "") || undefined,
      },

      success: () => {
        Alert.info('Поздравляем, вы зарегистировались на портале АДФС!\n Авторизуйтесь, пожалуйста!', alertDefault);
        $('#closeRegisterForm').trigger('click');
      },
      error: (data) => {
        data = JSON.parse(data.responseText);
        if (data.error === 'UNIQUE constraint failed: auth_user.username') {
          Alert.error('Пользователь с таким логином уже существует!', alertDefault);
          return;
        }
      },
    });
  }

  render () {
    return (
      <div id="modalRegister" className="modal fade" role="dialog">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-body">
              <form className="form-horizontal" id="register-form">
                <ModalHeader title="Регистрация нового пользователя"/>
                <div className="row">
                  <div className="col-sm-6">
                    <h3>Выберите аватар</h3>
                    { !this.state.webcam &&
                      <img src={this.state.avatarUrl} className="img" style={{width: "220px", height: "220px", borderRadius: "8px"}} id="avatarpreview"></img>
                      || <video style={{width: "220px", height: "220px", borderRadius: "8px"}} src={this.state.videostream} autoPlay="autoplay"></video>
                    }
                    <div className="btn-group">
                      { !this.state.webcam && <button type="button" className="btn btn-default" onClick={this.handleAvatarLoading}>
                        <span className="glyphicon glyphicon-upload"></span>
                      </button>
                      }
                      { !this.state.webcam && <button type="button" className="btn btn-default" onClick={this.switchToWebCam}>
                        <span className="glyphicon glyphicon-camera"></span>
                      </button>
                      }
                      { this.state.webcam &&
                        <button type="button" className="btn btn-default" onClick={this.takeAnImage}>
                          <span className="glyphicon glyphicon-certificate"></span>
                        </button>
                      }
                      { this.state.avatarUrl && !this.state.webcam &&
                        <button className="btn btn-danger" onClick={this.handleAvatarDrop}>
                          <span className="glyphicon glyphicon-remove"></span>
                        </button> }
                    </div>
                  </div>
                  <div className="col-sm-6" style={{borderLeft: "solid 1px", borderColor: "#999999"}}>
                    <InputItem id="login" title="Логин" type="text" />
                    <InputItem id="password" title="Пароль" type="password" />
                    <InputItem id="password2" title="Повторите пароль" type="password" />
                    <InputItem id="email" title="Электронная почта" type="email" />
                    <input type="file" name="avatar" accept=".png" id="avatarupl" onChange={this.uploadAvatar} style={{display: "none"}} />
                  </div>
              </div>
              </form>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-primary" onClick={this.handleRegister}>Регистрация</button>
              <button type="button" className="btn btn-default" data-dismiss="modal" id="closeRegisterForm">Закрыть</button>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
