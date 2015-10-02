'use strict';

angular.module('sbAdminApp')
  .service('trainerservice', function(serverComm) {


    this.startTraining = function(mid, pid, nepochs){

      var query = {
        'type': 'start_training',
        'params': {
          'modelId': mid,
          'paramsId': pid,
          'nepochs': nepochs
        }
      };

      var defer = serverComm.getData(query);
      return defer;
    };



    this.stopTraining = function(mid, pid){

      var query = {
        'type': 'stop_training',
        'params': {
          'modelId': mid,
          'paramsId': pid,
        }
      };

      var defer = serverComm.getData(query);
      return defer;
    };
    this.attachHandler = function(mid, pid, callback){

      var ws = new WebSocket("ws://"+ location.host +"/trainersocket");

      ws.onopen = (function(){

        var query = {
          'type': 'attach_handler',
          'params': {
            'modelId': mid,
            'paramsId': pid,
            }
        };

          ws.send(JSON.stringify(query));
      });

      ws.onmessage = callback ;

    };
  
});
