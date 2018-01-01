const api = {
  getStadions(callback) {
    $.get('/logic/api/v1/stadion', (stadions, result) => {
      if (result === 'success') {
        callback(stadions);
      } else {
        console.log('ERROR: fetch stadions:');
      }
    });
  },

  getStadionTimes(stadionId, callback) {
    $.get(`/logic/api/v1/stadion/${stadionId}/times`, (data, result) => {
      if (result === 'success') {
        callback(data);
      } else {
        console.log('ERROR: fetch stadion times');
      }
    });
  },

  createStadionTime(stadionId, params, callback) {
    let selectedTimeStart = params.selectedTimeStart.split(':');
    let selectedTimeEnd = params.selectedTimeEnd.split(':');

    selectedTimeStart = Number(selectedTimeStart[0]) * 60 + Number(selectedTimeStart[1]);
    selectedTimeEnd = Number(selectedTimeEnd[0]) * 60 + Number(selectedTimeEnd[1]);

    const data = {
      time1: selectedTimeStart,
      time2: selectedTimeEnd,
      date: params.selectedDate,
    };

    $.post(`/logic/api/v1/stadion/${stadionId}/times`, data, (data, result) => {
      callback();
    });
  },
};

export default api;
